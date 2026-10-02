# Program Workbench Canvas

The Program Workbench is a project-scoped Copilot canvas for program managers
who need to work with the repository documentation without using Git or a code
editor.

## Capabilities

* Browse the programme spine and the complete documentation library.
* Search Markdown titles, descriptions, paths and content.
* Render and edit Markdown with explicit save status and `Ctrl+S`.
* Inspect outgoing links and backlinks.
* Protect the original case study, regulatory snapshots and owner-controlled
  memory from accidental edits.
* Discover presentation and visual files as read-only version-one records.

The extension has no external runtime dependencies. It binds one ephemeral
HTTP server per open canvas instance to `127.0.0.1` and restricts API calls with
an instance token.

## Canvas Identity

* Canvas ID: `program-workbench`
* Display name: `Program Workbench`
* Optional open input: `{ "initialPath": "docs/.../file.md" }`
* Actions: `refresh_index`, `get_document`
