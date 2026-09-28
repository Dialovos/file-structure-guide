#!/usr/bin/env bash
# Back up the paths in backup-paths.txt with restic.
# Configure the repository through the environment (never store secrets here):
#   RESTIC_REPOSITORY     where the backup repository is
#   RESTIC_PASSWORD_FILE  file containing the repository passphrase
set -euo pipefail

: "${RESTIC_REPOSITORY:?set RESTIC_REPOSITORY}"
: "${RESTIC_PASSWORD_FILE:?set RESTIC_PASSWORD_FILE}"

here="$(cd "$(dirname "$0")" && pwd)"
mapfile -t paths < <(grep -vE '^[[:space:]]*(#|$)' "$here/backup-paths.txt")

cd "$HOME"
restic backup --exclude-file "$here/backup-excludes.txt" --tag scheduled "${paths[@]}"
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
restic check --read-data-subset=5%
