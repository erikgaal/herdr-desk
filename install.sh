#!/usr/bin/env bash
# herdr `[[build]]` step: create the plugin's Python venv with its pinned dependencies.
# Build commands may not receive the runtime HERDR_* env, so the root comes from this script's path.
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
python=${DESK_PYTHON:-python3}
"$python" -c 'import sys; sys.exit(sys.version_info < (3, 11))' \
  || { echo "desk needs Python 3.11 or newer (tomllib); set DESK_PYTHON to one" >&2; exit 1; }
[[ -x $root/.venv/bin/python ]] || "$python" -m venv "$root/.venv"
"$root/.venv/bin/python" -m pip install --quiet --disable-pip-version-check -r "$root/requirements.txt"
