# MARS

Command-line tool for bibliography management

## Background

In my PhD lab we had a citation database ("lars") with more than 20k entries, which has been manually curated over the last 20 years. A small sample of this database with 22 entries is included in `assets/lars.txt`. The main goal of this tool is convert it to bibtex format to make
paper writing easier. Furthermore, it also provides functionality for doing keyword searches on the bibliography entries.

The citation keys therein, also referred to as "lars codes", are made up by the first two letters of the first author's last name, the last 2 digits of the publication year, followed by a dot and a sequential index.

Most of these references used to be backed up by a PDF of the paper in a shared folder. Here, some of the PDFs (open access papers) are included in
the `PDF` directory as a sample. The tool includes some functions for opening / extracting / combining PDFs matching a search, although these rely
on bash scripts (unfortunately) and are limited to a Linux environment.

## Installation

The script requires Python >= 3.7, but no further packages. No pip/conda environments needed, as long as `python3` can be found in `PATH`.

The PDF operations are Linux-specific and require `pdftk`, `pdflatex` and `evince`. E.g. on Ubuntu, these can be installed (if not already available) using

```
sudo apt install pdftk pdflatex evince
```

Functionality for searching the lars file and bibliography generation isn't affected by this limitation though.

## Use

MARS uses argparse to process the input, and help messages are provided. Type `./mars -h` to see the available functions (subparsers), and e.g. `./mars find -h` for the use are arguments required for each subparser.

### Example use cases

- Converting `lars.txt` to bibtex: `./mars bibtex`
- List all entries containing the keyword "energy" but not "hydration": `./mars find "energy AND NOT hydration"`
- Print the entry matching the lars code KU20.1: `./mars print -r KU20.1`
- (Linux only) Open PDFs of documents where "Krishnan" is a (co-)author: `./mars find -a krishnan evince`
