# Details

Pager state: `sync = () => { prev.disabled = offset <= 0; next.disabled = offset + items.length >= total; }` called at build and after a successful page load. Buttons are native `disabled` (not aria-only). Row link page = floor((offset+index)/screenPageSize); the table opens on the 50-row page holding the row. Mypy: annotate any new test helpers; do not touch chat.js.
