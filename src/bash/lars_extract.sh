#!/usr/bin/env bash

# arg: lars code of pdf to be extracted
repo_dir="$1"
file="${repo_dir}/PDF/${2}.pdf"

# copy pdf in question to current dir
if [ -f "$file" ]; then
   cp "$file" .
else
   echo "File ${2}.pdf not found in LARS"
fi
