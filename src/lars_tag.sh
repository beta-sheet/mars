#!/usr/bin/env bash

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
TMP="$(mktemp -d)"

# input
pdf=$1
pdfname=$(basename $1)
pdfname="${pdfname%.*}"
pdfname=${pdfname}_$$
lars_code=$2
stamp_tex="$TMP/stamp.tex"

# check if PDF file exists - otherwise do nothing
if [ ! -f "$pdf" ]; then
   exit
fi

# prepare tex file with lars code stamp
echo "\documentclass[paper=a4, fontsize=12pt]{scrartcl}" > "$stamp_tex"
echo "\usepackage[T1]{fontenc}" >> "$stamp_tex"
echo "\usepackage[margin={0in,0.2in}]{geometry}" >> "$stamp_tex"
echo "\usepackage[utf8]{inputenc}" >> "$stamp_tex"
echo "\usepackage[english]{babel}" >> "$stamp_tex"														
echo "\begin{document}" >> "$stamp_tex"
echo "\hfill \texttt{${lars_code}}" >> "$stamp_tex"
echo "\end{document}" >> "$stamp_tex"

# make blank PDF page with lars code in top right corner
cd $TMP
pdflatex "${stamp_tex}" >/dev/null
cd "$wd"

# separate 1st page from document and stamp it
num_pages=$(pdftk "$pdf" dump_data|grep NumberOfPages| awk '{print $2}')

pdftk $pdf cat 1 output $TMP/${pdfname}_1.pdf
if [[ $num_pages -ne 1 ]]; then
   pdftk $pdf cat 2-end output $TMP/${pdfname}_2.pdf
fi
pdftk $TMP/${pdfname}_1.pdf stamp $TMP/stamp.pdf output $TMP/${pdfname}_1stamp.pdf

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
rm -rf $TMP
