#!/usr/bin/env bash
# Pane entrypoint. Textual draws the UI on stderr, so stderr must stay on the
# terminal; only the exit is logged, and a failure pauses so its message is visible.
root=${HERDR_PLUGIN_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)}
log=${XDG_STATE_HOME:-$HOME/.local/state}/desk/ui.log; mkdir -p "$(dirname "$log")"
export TERM=${TERM:-xterm-256color}
"$root/.venv/bin/python" "$root/desk.py"
rc=$?; echo "$(date +%FT%T) desk.py exited rc=$rc" >>"$log"
[[ $rc -ne 0 ]] && { echo "desk exited with $rc"; sleep 8; }
exit $rc
