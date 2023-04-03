#!/usr/bin/env bash

# arg: lars code of pdf to be evince'd
repo_dir="$1"
file="${repo_dir}/PDF/${2}.pdf"

# evince the file
if [ -f "$file" ]; then
   evince "$file" >&/dev/null &
else
   echo "File ${2}.pdf not found in LARS"
fi
