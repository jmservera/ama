import { CanvasError, createCanvas, joinSession } from "@github/copilot-sdk/extension";
import { getIndexedDocument, refreshDocumentIndex, startProgramWorkbenchServer } from "./server.mjs";

const servers = new Map();

const canvas = createCanvas({
  id: "program-workbench",
  displayName: "Program Workbench",
  description: "Browse, connect, search, and edit the repository's program documentation without Git or a code editor.",
  inputSchema: {
    type: "object",
    additionalProperties: false,
    properties: { initialPath: { type: "string", description: "Repository-relative Markdown path to open initially." } },
  },
  actions: [
    {
      name: "refresh_index",
      description: "Refresh the program document index after repository files change.",
      handler: async () => ({ documentCount: (await refreshDocumentIndex()).length, refreshedAt: new Date().toISOString() }),
    },
    {
      name: "get_document",
      description: "Read one Markdown document and its linked-document context.",
      inputSchema: {
        type: "object",
        additionalProperties: false,
        required: ["path"],
        properties: { path: { type: "string" } },
      },
      handler: async (ctx) => {
        try { return await getIndexedDocument(ctx.input.path); }
        catch (error) { throw new CanvasError("document_read_failed", error.message); }
      },
    },
  ],
  open: async (ctx) => {
    let entry = servers.get(ctx.instanceId);
    if (!entry) {
      entry = await startProgramWorkbenchServer({ initialPath: ctx.input?.initialPath });
      servers.set(ctx.instanceId, entry);
    }
    return { title: "Proper Warm - Program Workbench", status: "Repository documentation", url: entry.url };
  },
  onClose: async (ctx) => {
    const entry = servers.get(ctx.instanceId);
    if (!entry) return;
    servers.delete(ctx.instanceId);
    await new Promise((resolve) => entry.server.close(resolve));
  },
});

await joinSession({ canvases: [canvas] });
