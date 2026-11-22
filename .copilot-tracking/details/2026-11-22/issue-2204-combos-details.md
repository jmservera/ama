# Details: issue 2204 combinations live (2026-11-22)

Probes: `/api/me`, `/api/cases`, `/api/workorders`, `/api/stats`, `/api/finance`, `/api/admin/simulator-control`; capability probes `GET /api/chat/regulatory/status`, `POST /api/law/cards` and `POST /api/law/cards/X/1/approve` with an invalid body (403 without capability, 400 with), `POST /api/continuity/restart-decide` with `{}` (non-discriminating). Screenshots at 1366x900 with email addresses masked. Credentials read at run time, never printed.
