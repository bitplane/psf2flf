#!/bin/sh
psf2flf --all /usr/share/consolefonts fonts/console

for f in $(ls -1 fonts/console/*.flf | grep flf); do
    echo $(basename $f); echo $(basename $f) | figlet -f $f;
    sleep 0.2;
done
