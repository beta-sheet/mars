#!/bin/bash

# arg: lars code of pdf to be evince'd

wd=$(pwd)

# mount Phil's home if not mounted yet
cd ~phil
cd $wd

file="/home/phil/lars/PDF/${1}.pdf"

# evince the file
if [ -f "$file" ]; then
   evince /home/phil/lars/PDF/${1}.pdf >&/dev/null &
else
   echo "File ${1}.pdf not found in LARS"
fi
