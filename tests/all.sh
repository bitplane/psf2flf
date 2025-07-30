#!/bin/sh
psf2flf --all /usr/share/consolefonts fonts/console

for f in fonts/console/*.flf; do
    echo $(basename $f); echo $(basename $f) | figlet -f $f -w 157 | lolcat
    sleep 0.1;
done
