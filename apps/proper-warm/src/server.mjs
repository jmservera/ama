import { createServer } from 'node:http';
import { randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve } from 'node:path';
import { AppError, config, filterCases, portfolio, validateRole } from './domain.mjs';
import { createStore } from './store.mjs';
import { runAssistant } from './assistant.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const limit = 64 * 1024;
const assets = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/index.html', ['index.html', 'text/html; charset=utf-8']],
  ['/styles.css', ['styles.css', 'text/css; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
]);
async function jsonBody(request) {
  if ((request.headers['content-type'] ?? '').split(';')[0].trim().toLowerCase() !== 'application/json') throw new AppError(400, 'INVALID_PAYLOAD', 'JSON Content-Type is required.');
  if (Number(request.headers['content-length']) > limit) {
    request.resume();
    throw new AppError(413, 'BODY_TOO_LARGE', 'Request body exceeds 64 KiB.');
  }
  const data = await new Promise((resolveBody, reject) => {
    const chunks = [];
    let size = 0;
    let oversized = false;
    request.on('data', chunk => {
      size += chunk.length;
      if (size > limit) {
        if (!oversized) {
          oversized = true;
          chunks.length = 0;
          reject(new AppError(413, 'BODY_TOO_LARGE', 'Request body exceeds 64 KiB.'));
        }
      } else if (!oversized) chunks.push(chunk);
    });
    request.on('end', () => { if (!oversized) resolveBody(Buffer.concat(chunks)); });
    request.on('error', reject);
  });
  try { return JSON.parse(data.toString('utf8')); }
  catch { throw new AppError(400, 'INVALID_PAYLOAD', 'Malformed JSON body.'); }
}

export function createApplication({
  dbPath = process.env.DB_PATH ?? resolve(root, 'data', 'proper-warm.db'),
  host = process.env.HOST ?? '127.0.0.1',
  port = Number(process.env.PORT ?? 3410),
  threshold = Number(process.env.NO_ACCESS_THRESHOLD ?? 5),
  publicDirectory = resolve(root, 'public'),
  log = record => console.log(JSON.stringify(record)),
  fault,
  assistantGenerator,
} = {}) {
  const store = createStore({ dbPath, threshold, fault, log });
  const metrics = { requests: 0, errors: 0, totalDurationMs: 0 };
  const server = createServer(async (request, response) => {
    const requestId = randomUUID();
    const started = performance.now();
    let route = 'unresolved';
    response.setHeader('X-Request-Id', requestId);
    response.setHeader('X-Content-Type-Options', 'nosniff');
    response.setHeader('Referrer-Policy', 'no-referrer');
    response.setHeader('Content-Security-Policy', "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; font-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'");
    response.setHeader('Cache-Control', 'no-store');
    const send = (status, value, contentType = 'application/json; charset=utf-8') => {
      response.statusCode = status;
      response.setHeader('Content-Type', contentType);
      response.end(contentType.startsWith('application/json') ? JSON.stringify(value) : value);
    };
    try {
      // Host must match the actual local listener port and a literal loopback name.
      const actualPort = server.address()?.port;
      const allowed = new Set([`127.0.0.1:${actualPort}`, `localhost:${actualPort}`, `[::1]:${actualPort}`]);
      const authority = request.headers.host;
      if (typeof authority !== 'string' || !allowed.has(authority.toLowerCase())) throw new AppError(403, 'INVALID_HOST', 'Only the configured local origin is allowed.');
      const origin = `http://${authority.toLowerCase()}`;
      if (request.headers.origin !== undefined && request.headers.origin !== origin) throw new AppError(403, 'INVALID_ORIGIN', 'Foreign origins are not permitted.');
      if (request.method === 'POST' && request.headers.origin === undefined && request.headers['x-proper-warm-request'] !== '1') {
        throw new AppError(403, 'INVALID_ORIGIN', 'POST requires same-origin Origin or X-Proper-Warm-Request: 1 for local automation.');
      }
      if (request.method === 'POST' && request.headers['sec-fetch-site'] && !['same-origin', 'none'].includes(request.headers['sec-fetch-site'])) throw new AppError(403, 'INVALID_ORIGIN', 'Cross-site writes are not permitted.');
      const url = new URL(request.url, origin);
      route = url.pathname.startsWith('/api/cases/') ? '/api/cases/:id' : url.pathname;
      const role = request.headers['x-demo-role'] ?? 'viewer';
      validateRole(role);
      if (request.method === 'GET' && url.pathname === '/health') {
        const ready = store.readiness();
        send(ready ? 200 : 503, { status: ready ? 'ready' : 'unavailable', store: ready ? 'writable' : 'unavailable', synthetic: true });
      } else if (request.method === 'GET' && url.pathname === '/metrics') {
        send(200, { ...metrics, synthetic: true, assistant: 'simulator', externalCalls: 0 });
      } else if (request.method === 'GET' && url.pathname === '/api/config') {
        send(200, config);
      } else if (request.method === 'GET' && ['/api/cases', '/api/portfolio', '/api/export'].includes(url.pathname)) {
        const scope = { workflow: url.searchParams.get('workflow') ?? '', q: url.searchParams.get('q') ?? '' };
        const cases = filterCases(store.list(role), scope.workflow, scope.q);
        const asOf = new Date().toISOString();
        if (url.pathname === '/api/portfolio') send(200, portfolio(cases, scope, asOf));
        else {
          if (url.pathname === '/api/export') response.setHeader('Content-Disposition', 'attachment; filename="proper-warm-synthetic.json"');
          send(200, { cases, scope, asOf, ...(url.pathname === '/api/export' ? { version: 'poc-1', synthetic: true } : {}) });
        }
      } else if (url.pathname.startsWith('/api/cases/')) {
        const match = /^\/api\/cases\/([^/]+)(?:\/(commands|assistant))?$/.exec(url.pathname);
        if (!match) throw new AppError(404, 'NOT_FOUND', 'Endpoint not found.');
        let id;
        try { id = decodeURIComponent(match[1]); } catch { throw new AppError(400, 'INVALID_PAYLOAD', 'Invalid case identifier.'); }
        if (request.method === 'GET' && !match[2]) send(200, store.detail(id, role));
        else if (request.method === 'POST' && match[2]) {
          if (!request.headers['x-demo-role']) throw new AppError(403, 'FORBIDDEN', 'Write requires an explicit demo role.');
          const body = await jsonBody(request);
          if (match[2] === 'commands') send(200, store.execute(id, role, body));
          else send(200, runAssistant(store, id, role, body, assistantGenerator));
        } else throw new AppError(405, 'METHOD_NOT_ALLOWED', 'Endpoint method is not supported.');
      } else if (request.method === 'GET' && assets.has(url.pathname)) {
        const [filename, mime] = assets.get(url.pathname);
        let data;
        try { data = await readFile(resolve(publicDirectory, filename)); }
        catch (error) {
          if (error.code === 'ENOENT') throw new AppError(404, 'NOT_FOUND', 'Static asset unavailable.');
          throw error;
        }
        send(200, data, mime);
      } else throw new AppError(404, 'NOT_FOUND', 'Endpoint not found.');
    } catch (error) {
      const known = error instanceof AppError;
      if (!known) log({ level: 'error', event: 'request_failed', requestId, route, code: String(error.code ?? 'UNEXPECTED_FAILURE') });
      if (!response.headersSent) send(known ? error.status : 503, {
        error: { code: known ? error.code : 'STORE_UNAVAILABLE',
          message: known ? error.message : 'Local service unavailable. No successful mutation is reported.',
          owner: known ? error.owner : 'programme_manager', details: known ? error.details : [] }, requestId,
      });
    } finally {
      const durationMs = Number((performance.now() - started).toFixed(3));
      metrics.requests++;
      metrics.totalDurationMs += durationMs;
      if (response.statusCode >= 400) metrics.errors++;
      log({ level: 'info', event: 'request', requestId, method: request.method, route, status: response.statusCode, durationMs });
    }
  });
  server.requestTimeout = 15000;
  server.headersTimeout = 10000;
  server.keepAliveTimeout = 5000;
  return {
    server, store,
    listen() {
      return new Promise((resolvePromise, reject) => {
        server.once('error', reject);
        server.listen(port, host, () => {
          server.off('error', reject);
          resolvePromise(server.address());
        });
      });
    },
    async close() {
      if (server.listening) await new Promise((resolvePromise, reject) => server.close(error => error ? reject(error) : resolvePromise()));
      store.close();
    },
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  let application;
  try {
    application = createApplication();
    const address = await application.listen();
    console.log(JSON.stringify({ level: 'info', event: 'listening', host: address.address, port: address.port, synthetic: true, assistant: 'simulator' }));
    const stop = async () => { await application.close(); process.exitCode = 0; };
    process.once('SIGINT', stop);
    process.once('SIGTERM', stop);
  } catch (error) {
    console.error(JSON.stringify({ level: 'error', event: 'startup_failed', code: String(error.code ?? 'STARTUP_FAILURE'), message: 'Failed to initialize local application; existing store was not reset.' }));
    if (application) await application.close();
    process.exitCode = 1;
  }
}
