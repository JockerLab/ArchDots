#!/bin/bash

if [ -z "$(hyprctl activewindow -j | jq -r '.title')" ]; then
    echo '{"class": "empty"}';
else
    echo '{}';
fi
