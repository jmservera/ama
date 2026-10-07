FROM node:24.18.0-bookworm-slim@sha256:6f7b03f7c2c8e2e784dcf9295400527b9b1270fd37b7e9a7285cf83b6951452d

ENV NODE_ENV=production HOST=0.0.0.0 PORT=3410 DB_PATH=/data/proper-warm.db
WORKDIR /app
RUN mkdir /data && chown node:node /data /app
COPY --chown=node:node package.json manifest.json ./
COPY --chown=node:node src ./src
COPY --chown=node:node public ./public
USER node
EXPOSE 3410
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:3410/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "src/server.mjs"]
