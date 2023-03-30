#!/bin/bash

wd=$(pwd)

# mount Phil's home if not mounted yet
cd ~phil
cd "${wd}"

file="/home/phil/lars/PDF/${1}.pdf"

# copy pdf in question to current dir
if [ -f "$file" ]; then
   cp /home/phil/lars/PDF/${1}.pdf .
else
   echo "File ${1}.pdf not found in LARS"
fi
