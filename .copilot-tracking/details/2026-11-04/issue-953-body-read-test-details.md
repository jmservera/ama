# Details: issue 953 slice 2

Test sends a POST to `/api/bulk-edits/preview` with a partial body, resets the connection, and asserts exactly one WARNING record containing `client-disconnect exc=ConnectionResetError phase=request-read` and no `status=500`.
