# Details

Commands: `docker build -f src/api/Dockerfile -t crcutovertestrzsrg.azurecr.io/zava-forward-api:main-b0080d4e1 src`; same for `src/api/Dockerfile.resident-demo` -> `zava-resident-demo`. Window: `az acr update --allow-exports true`; `--public-network-enabled true --default-action Deny`; `az acr network-rule add --ip-address <operator IP>`; push; then remove rule by bare IP, disable public, disable exports.
Digests: API `sha256:15cf2f3d0b2a34c6a9b5e1b64bc7063c88173153ccbdba722a1b033e575e3ad6`; resident `sha256:ca80afe69aaaa484a334b3ae9197912896d1cf703e329eb3d5a9945ce6ef2cab`.
