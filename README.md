# MARS

Command-line tool to search the LARS citation database and bibtex generation.

## Installation

None needed on the lab workstations. On other computers you may need to make an environment with Python 2.7:

```
conda install -n <env_name> requirements.txt
```

Add mars script to your path:
```
PATH=$PATH:`pwd`
```

## Use

MARS uses argparse to process the input, and help messages are provided. Type `mars -h` to see the available functions (subparsers), and e.g. `mars find -h` for the args required for each subparser.
