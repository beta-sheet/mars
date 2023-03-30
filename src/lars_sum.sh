#!/bin/bash

# --------------------------------------------------------------------------------------
#                                   LARS SUMMARY
# --------------------------------------------------------------------------------------
#
# this script takes dir with (tagged) pdfs as input and assembles their 1st pages to
# summary file

# get the absolute paths
wd=$(pwd)
SRC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"  # where this script is located
PYLARS="$(dirname "$SRC")"  # parent directory
TMP="${PYLARS}/tmp"

PDFDIR=$1   # we pass dir with tagged pdfs as arg
OUTFILE=$2
PID=$$

# here we'll put the 1st pages of each pdf
mkdir $TMP/sum_$PID

# extract 1st pages
for file in $(ls $PDFDIR); do
   pdftk $PDFDIR/$file cat 1 output $TMP/sum_$PID/$file
done

# assemble 1st pages to summary
pdftk $TMP/sum_$PID/* output $2

# clean up
rm -rf $TMP/sum_$PID
