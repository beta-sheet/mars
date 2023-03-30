#!/bin/bash

# --------------------------------------------------------------------------------------
#                                   LARS TAG FUNCTION
# --------------------------------------------------------------------------------------
#
# this script takes the pdf to be tagged and the tag string as arguments, and will out-
# put a tagged pdf in the WD. If the source pdf is in WD as well, it will be overwrit-
# ten.
#
# Needs: pdftk and (very basic) pdflatex

# get the absolute paths
wd="$(pwd)"
SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # where this script is located
PYLARS="$(dirname "$SRC")"  # parent directory
TAG="${PYLARS}/tag"
TMP="${PYLARS}/tmp"

# input
pdf=$1
pdfname=$(basename $1)
pdfname="${pdfname%.*}"
pdfname=${pdfname}_$$
lars_code=$2
stamp_tex="$TAG/stamp.tex"

# check if PDF found - otherwise do nothing
if [ ! -f "$pdf" ]; then
   exit
fi

# make blank PDF page with lars code in top right corner
sed "s/LARSCODE/$lars_code/g" $stamp_tex > $TMP/${pdfname}_overlay.tex
cd $TMP
pdflatex ${pdfname}_overlay.tex >/dev/null
cd "$wd"

# separate 1st page from document and stamp it

num_pages=$(pdftk "$pdf" dump_data|grep NumberOfPages| awk '{print $2}')

pdftk $pdf cat 1 output $TMP/${pdfname}_1.pdf
if [[ $num_pages -ne 1 ]]; then
   pdftk $pdf cat 2-end output $TMP/${pdfname}_2.pdf
fi
pdftk $TMP/${pdfname}_1.pdf stamp $TMP/${pdfname}_overlay.pdf output $TMP/${pdfname}_1stamp.pdf

# if file in wd, overwrite it (pdftk won't overwrite)
if [ -f "${pdf}" ]; then
   rm $pdf
fi

# make the file
if [[ $num_pages -eq 1 ]]; then
   cp $TMP/${pdfname}_1stamp.pdf $pdf
else
   pdftk $TMP/${pdfname}_1stamp.pdf $TMP/${pdfname}_2.pdf output $pdf
fi
#
# clean up
cd $TMP
rm  -f ${pdfname}_1.pdf ${pdfname}_1stamp.pdf ${pdfname}_2.pdf ${pdfname}_overlay.*
cd "$wd"
