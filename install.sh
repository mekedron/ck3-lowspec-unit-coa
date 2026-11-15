#!/usr/bin/env bash
# Копирует мод в папку модов CK3 внутри Proton-префикса.
# Игра под Proton читает Documents из префикса, а не из ~/.local/share/Paradox Interactive.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="$HOME/.local/share/Steam/steamapps/compatdata/1158310/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Crusader Kings III"
NAME="lowspec_unit_coa"

[ -d "$DST" ] || { echo "Папка префикса не найдена: $DST" >&2; exit 1; }
pgrep -f "Paradox Launcher.exe" >/dev/null && echo "Внимание: лаунчер запущен, закрой его перед установкой." >&2

mkdir -p "$DST/mod/$NAME"
rm -rf "$DST/mod/$NAME/gfx"
cp -r "$SRC/gfx" "$DST/mod/$NAME/gfx"
cp "$SRC/descriptor.mod" "$DST/mod/$NAME/descriptor.mod"
if [ -f "$SRC/thumbnail.png" ]; then cp "$SRC/thumbnail.png" "$DST/mod/$NAME/thumbnail.png"; fi
{ cat "$SRC/descriptor.mod"; printf 'path="mod/%s"\r\n' "$NAME"; } > "$DST/mod/$NAME.mod"

echo "Установлено в $DST/mod/$NAME"
echo "Дальше: включи 'Unit Coats of Arms Without Advanced Shaders' в плейсете лаунчера."
