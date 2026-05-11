#!/bin/sh
# xdg-desktop-portal-termfilechooser wrapper for yazi
# Args: multiple directory save path out
multiple="$1"
directory="$2"
save="$3"
path="$4"
out="$5"

term="kitty --class=filechooser"

if [ "$save" = "1" ]; then
    dir=$(dirname "$path")
    mkdir -p "$dir"
    # Pre-create the suggested file so user can press Enter to confirm
    touch "$path"
    $term -- yazi --chooser-file="$out" "$dir"
    if [ ! -s "$out" ]; then
        rm -f "$path"
    fi
else
    $term -- yazi --chooser-file="$out"
fi
