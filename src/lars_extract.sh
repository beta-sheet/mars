#!/usr/bin/env bash

# arg: lars code of pdf to be extracted
repo_dir=$(dirname $(dirname ${BASH_SOURCE[0]}))
file="${repo_dir}/PDF/${1}.pdf"

# copy pdf in question to current dir
if [ -f "$file" ]; then
   cp "$file" .
else
   echo "File ${1}.pdf not found in LARS"
fi
