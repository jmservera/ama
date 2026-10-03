# Program Workbench Canvas

The Program Workbench is a project-scoped Copilot canvas for program managers
who need to work with the repository documentation without using Git or a code
editor.

## Capabilities

* Browse the programme spine and the complete documentation library.
* Search Markdown titles, descriptions, paths and content.
* Render Markdown and edit it with TOAST UI Editor's built-in Markdown/WYSIWYG
  mode switch, explicit save status and `Ctrl+S`.
* Keep YAML frontmatter outside the visual editor in an expandable source field.
  Opening a document or toggling modes without editing preserves the original
  source, including line endings. Visual edits can normalize Markdown formatting.
* Use TOAST's Markdown source mode for detected callouts, diagrams, raw HTML,
  reference definitions, images and other guarded syntax; visual conversion is
  blocked to avoid losing it. Detection is conservative, not a guarantee of
  lossless round-tripping for every Markdown extension. Adding guarded syntax in
  Markdown mode blocks switching into WYSIWYG.
* Fill the remaining visible page height in Edit mode. The editor scrolls
  internally; metadata and linked-record context have separate bounded scrolling.
* Start a standalone chat with the selected saved Markdown file attached.
  The button asks the current agent to stage a file copy, create a detached
  chat and navigate to it. It requires an agent turn, not a direct host API.
  Product Manager Advisor is selected by its stable ID when present in the
  selectable agent list; otherwise the UI reports use of the default agent.
  Read-only documents can be discussed without relaxing their edit protections.
  Save or discard pending canvas edits first. The attachment is a snapshot,
  not a live repository connection.
* Refresh the index and selected viewer document on focus or visibility return,
  without overwriting unsaved canvas edits. Only saved disk changes are visible.
* Inspect outgoing links and backlinks.
* Protect the original case study, regulatory snapshots and owner-controlled
  memory from accidental edits.
* Discover presentation and visual files as read-only version-one records.

The extension needs no runtime package installation: pinned editor assets are
bundled locally under `assets/vendor/`, with license notices. Usage telemetry is
disabled, and rendering uses a separately maintained DOMPurify sanitizer.
The canvas does not load scripts, images or styles from external hosts.
It binds one ephemeral
HTTP server per open canvas instance to `127.0.0.1` and restricts API calls with
an instance token.

## Building and Checking Editor Assets

From `tools/program-workbench-assets/` at the repository root, run
`npm ci --ignore-scripts` and `npm run build` after changing dependencies.
Build dependencies must stay outside `.github/extensions/`: the app's 8 MiB
project-extension trust limit includes local files such as `node_modules`,
even when Git ignores them. Only the generated runtime assets and notices
belong in this extension. The build checks the extension size after generation
and uses a portable WebAssembly bundler.
The Copilot SDK remains supplied by the runtime and is not an npm dependency.

Run `python tests/test_editor.py` with Python Playwright and its Chromium browser
installed. The tests use a temporary repository, never modify project documents,
and cover mode switching, frontmatter, tables, relative links, source fallback,
protected documents, saves and refresh while edits are pending.
Run `node --test tests/conversation.test.mjs` to check advisor selection,
standalone-chat request construction and conversation endpoint validation.

## Canvas Identity

* Canvas ID: `program-workbench`
* Display name: `Program Workbench`
* Optional open input: `{ "initialPath": "docs/.../file.md" }`
* Actions: `refresh_index`, `get_document`
