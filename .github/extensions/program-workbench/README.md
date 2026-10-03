# Program Workbench Canvas

The Program Workbench is a project-scoped Copilot canvas for program managers
who need to work with the repository documentation without using Git or a code
editor.

## Capabilities

* Browse the programme spine and the complete documentation library.
* Search Markdown titles, descriptions, paths and content.
* Render and edit Markdown with explicit save status and `Ctrl+S`.
* Test an experimental "Open editor via agent" handoff to the app's native
  editor. The button sends a navigation-only request to the current agent;
  it is not a direct Files-tab API and requires an agent turn. Protected
  documents cannot use the handoff, and unsaved canvas edits must be saved
  or discarded first.
* Refresh the index and selected viewer document on focus or visibility return,
  without overwriting unsaved canvas edits. Only saved disk changes are visible.
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
