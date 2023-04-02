#!/usr/bin/env bash

# arg: lars code of pdf to be evince'd
repo_dir=$(dirname $(dirname ${BASH_SOURCE[0]}))
file="${repo_dir}/PDF/${1}.pdf"

# evince the file
if [ -f "$file" ]; then
   evince "$file" >&/dev/null &
else
   echo "File ${1}.pdf not found in LARS"
fi
