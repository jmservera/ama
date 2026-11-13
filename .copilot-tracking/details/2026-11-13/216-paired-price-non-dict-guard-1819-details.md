# Details

Existing missing-key messages stay unchanged. Existing "price or usage values not numeric" message is superseded by per-key names; check no test depends on it (grep before change). A present-but-falsy non-Mapping (0, "", []) is reported as missing by the existing COST_INPUTS check and treated as {}; only truthy non-Mapping gets the new message.
