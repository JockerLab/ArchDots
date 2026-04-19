#!/usr/bin/env python3
"""
Listens to Hyprland activelayout events and signals Waybar (SIGRTMIN+4)
to refresh the custom/language module instantly.

Layout is extracted directly from the IPC event — this avoids the issue
where different physical keyboards have independent XKB states, making
per-device hyprctl queries unreliable.
"""
import socket
import os
import subprocess
import json

SOCKET_PATH = (
    f"{os.environ['XDG_RUNTIME_DIR']}/hypr"
    f"/{os.environ['HYPRLAND_INSTANCE_SIGNATURE']}/.socket2.sock"
)
CACHE_FILE = "/tmp/hypr_lang"


def layout_to_code(layout: str) -> str:
    if "English" in layout or "US" in layout:
        return "EN"
    if "Russian" in layout:
        return "RU"
    return layout[:2].upper()


def write_cache(text: str) -> None:
    with open(CACHE_FILE, "w") as f:
        f.write(text)


# Initialize cache from current device state on startup
try:
    result = subprocess.run(["hyprctl", "devices", "-j"], capture_output=True, text=True)
    for kb in json.loads(result.stdout).get("keyboards", []):
        if "," in kb.get("layout", ""):
            write_cache(layout_to_code(kb.get("active_keymap", "")))
            break
except Exception:
    pass

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(SOCKET_PATH)

buf = b""
while True:
    data = s.recv(4096)
    if not data:
        break
    buf += data
    while b"\n" in buf:
        line, buf = buf.split(b"\n", 1)
        if line.startswith(b"activelayout>>"):
            # Format: activelayout>>keyboard_name,Layout Name
            try:
                layout = line.split(b",", 1)[1].decode().strip()
            except IndexError:
                continue
            write_cache(layout_to_code(layout))
            subprocess.run(["pkill", "-RTMIN+4", "waybar"])
