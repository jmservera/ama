"""Own-user Microsoft Graph photo. Tokens and upstream bodies never leave here."""
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

PHOTO_URL = "https://graph.microsoft.com/v1.0/me/photo/$value"
MAX_PHOTO = 2 * 1024 * 1024


class PhotoError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def own_photo(token, opener=None):
    if not token:
        raise PhotoError(503, "Microsoft photo access is not available. Sign in again after token-store setup.")
    request = Request(PHOTO_URL, headers={"Authorization": "Bearer " + token, "Accept": "image/jpeg, image/png"})
    try:
        with (opener or build_opener(NoRedirect())).open(request, timeout=10) as response:
            kind = response.headers.get_content_type()
            raw = response.read(MAX_PHOTO + 1)
    except HTTPError as error:
        messages = {
            404: "No Microsoft profile photo has been set.",
            401: "Microsoft photo access has expired. Sign in again.",
            403: "Microsoft has not authorised photo access. Check User.Read consent.",
        }
        status = error.code if error.code in messages else 502
        raise PhotoError(status, messages.get(status, "Microsoft profile photo service is unavailable.")) from None
    except (URLError, TimeoutError, OSError):
        raise PhotoError(502, "Microsoft profile photo service could not be reached.") from None
    valid = (kind == "image/png" and raw.startswith(b"\x89PNG\r\n\x1a\n")) or (
        kind == "image/jpeg" and raw.startswith(b"\xff\xd8\xff"))
    if not valid or len(raw) > MAX_PHOTO:
        raise PhotoError(502, "Microsoft returned an unsupported profile photo.")
    return raw, kind
