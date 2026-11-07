# Details: issue 144 queue adapter

* Receive: GET messages, numofmessages 1, visibilitytimeout 60. Text is base64 or plain JSON, validated by `TaskMessage.from_json`.
* Ack: DELETE with popreceipt. Release: PUT visibilitytimeout 0. Receipt is "id\npopreceipt".
* Poison: POST to `agent-tasks-poison`, then delete; a failed poison write leaves the message for redelivery.
* No inference, no database, no approval path added. AI-unavailable behaviour is unchanged (provider failure yields a failed envelope and manual review).
