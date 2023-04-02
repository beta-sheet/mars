#!/usr/bin/env bash

# --------------------------------------------------------------------------------------
#                                   LARS SUMMARY
# --------------------------------------------------------------------------------------
#
# this script takes dir with (tagged) pdfs as input and assembles their 1st pages to
# summary PDF file

# create temporary directory
TMP="$(mktemp -d)"

PDFDIR=$1   # we pass dir with tagged pdfs as arg
OUTFILE=$2

# extract 1st pages
for file in $(ls $PDFDIR); do
   pdftk $PDFDIR/$file cat 1 output $TMP/$file
done

# assemble 1st pages to summary
pdftk $TMP/* output $2

# delete temp directory
rm -rf $TMP
