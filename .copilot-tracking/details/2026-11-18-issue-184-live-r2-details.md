# Details: issue 184 live simulator stream, run 2

Driver kept in /tmp, passed as an env var; deleted afterwards. Sink: HTTPS device send with a per-device SAS token (`/devices/{id}/messages/events`, `iothub-messageid` = reading_id). Reader: `azure.eventhub.aio` consumer, starting at run start, managed identity. Output printed: ids, HTTP codes, counts, booleans; keys checked absent (full and 16-character prefix).
Failure injection is out of scope (not requested); wrong-key send gives a 401 contrast.
