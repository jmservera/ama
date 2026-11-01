#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

set -euo pipefail

main() {
  local repo_root
  repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
  local base="${repo_root}/docs/capstone/thought-leadership/everything-but-the-software"
  local paper="${base}/main.tex"

  if ! command -v tectonic >/dev/null; then
    printf '%s\n' 'Error: tectonic must be available on PATH.' >&2
    return 127
  fi

  mkdir -p "${base}"
  tectonic --untrusted --keep-logs --keep-intermediates \
    --outdir "${base}" "${paper}"
}

main "$@"
