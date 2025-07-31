#!/bin/sh
psf2flf /usr/share/consolefonts/*.psf.gz fonts/console/
psf2flf --tall /usr/share/consolefonts/*.psf.gz fonts/console/

WIDTH=$(tput cols)

for f in fonts/console/*.flf; do
    basename "$f"
    basename "$f" | figlet -f "$f" -w "$WIDTH" | lolcat
    sleep 0.1
done
