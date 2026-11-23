# Details
Phase 1: handler `_reject_unsupported` returns `self._json(401, {"error": "Please sign in."})` when path starts with /api/ and `self._user()` is falsy, else `self.send_error(501, f"Unsupported method ({self.command!r})")`. Phase 2: test loops PUT/PATCH/DELETE over /api/me, /api/cases, unknown; asserts 401, no Location; authenticated principal still gets 501.
