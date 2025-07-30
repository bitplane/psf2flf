#!/bin/sh
psf2flf --all /usr/share/consolefonts fonts/console

WIDTH=$(tput cols)

for f in fonts/console/*.flf; do
    basename "$f"
    basename "$f" | figlet -f "$f" -w "$WIDTH" | lolcat
    sleep 0.1
done
