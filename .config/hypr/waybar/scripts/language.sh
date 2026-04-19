#!/bin/bash
# Reads keyboard layout from cache written by language_listener.py.
# Falls back to hyprctl query on first run (before any layout change event).

CACHE="/tmp/hypr_lang"

if [ -f "$CACHE" ]; then
    text=$(cat "$CACHE")
else
    layout=$(hyprctl devices -j | python3 -c "
import json, sys
for kb in json.load(sys.stdin).get('keyboards', []):
    if ',' in kb.get('layout', ''):
        print(kb.get('active_keymap', ''))
        break
")
    case "$layout" in
        *English*|*US*) text="EN" ;;
        *Russian*)       text="RU" ;;
        *)               text="${layout:0:2}" ;;
    esac
fi

echo "{\"text\": \"$text\"}"
