import re
import sys
from typing import List

from src.util.record import Record


# operand-based case-insensitive search (AND, OR, NOT), no regex
def lars_find(
    records: List[Record], key: str, search_attr: List[str], case: bool
) -> List[Record]:
    """Filter list of records based on given key. The key can contain the operands 
    AND, OR, and NOT.

    Args:
        records (List[record]): List of records read in from LARS file
        key (str): Search key which may contain AND, OR and NOT operands
        search_attr (List[str]): List of attibutes to include in search (e.g. auth, titl)
        case (bool): Switch for case-sensitive search

    Returns:
        List[Record]: Subset of records which contain key
    """ """"""

    # split key string based on parentheses and spaces
    keys = filter(None, re.split(r"([()]|AND|OR|NOT)", key))
    keys = [k for k in keys if not k.isspace()]

    special_chars = ["AND", "OR", "NOT", ")", "("]

    # this is where the matches go
    found = []

    keywords = []
    statement = ""

    # This loop constructs an expression for filtering the input records which is then
    # directly processed with exec()
    for k in keys:
        if not k in special_chars:
            # loop over lars attributes
            statement_list = []
            for a in search_attr:
                # got new keyword
                keywords.append(k.rstrip().lstrip())
                if case:
                    statement_list.append(
                        '''"''' + k.lstrip().rstrip() + """" in r.""" + a + " "
                    )
                else:
                    statement_list.append(
                        '''"'''
                        + k.lstrip().rstrip().lower()
                        + """" in r."""
                        + a
                        + ".lower() "
                    )

            sub_statement = "(" + " or ".join(statement_list) + ")"
            statement = statement + sub_statement

        else:  # connector
            if case:
                statement = statement + " " + k + " "
            else:
                statement = statement + " " + k.lower() + " "

    # THIS IS WHERE THE MAGIC HAPPENS!
    # copy locals dictionary as Python 3 is no longer able to update locals directly through exec()
    locals_dict = locals()
    # + some fool-proofery around to save the user from reading tracebacks
    try:
        exec(
            "found = found + [r for r in records if " + statement + "]",
            globals(),
            locals_dict,
        )
    except SyntaxError:
        print("find: invalid statement")

    # retrieve result from exec
    found = locals_dict["found"]

    # if the output gets written to a terminal (rather than being redirected to a text file),
    # matching patterns will be colored in red
    if sys.stdout.isatty():
        found = color_matches(found, "|".join(keywords), search_attr)

    return found


# case-insensitive regex search
def lars_find_regex(
    records: List[Record], key: str, search_attr: List[str], case: bool
) -> List[Record]:
    """Filter list of records based on a regex key (used with find -r)

    Args:
        records (List[Record]): List of records read in from LARS file
        key (str): Search key as a regex expression
        search_attr (List[str]): List of attibutes to include in search (e.g. auth, titl)
        case (bool): Switch for case-sensitive search

    Returns:
        List[Record]: Subset of records which match the given regex
    """
    # here we'll store our matches
    found = []

    # loop over lars attributes
    for a in search_attr:
        if case:  # case-sensitive
            found = found + [
                r for r in records if re.search(key, getattr(r, a)) != None
            ]
        else:  # case-insensitive
            found = found + [
                r
                for r in records
                if re.search(key.lower(), getattr(r, a).lower()) != None
            ]

    # if the output gets written to a terminal (rather than being redirected to a text file),
    # matching patterns will be colored in red
    if sys.stdout.isatty():
        found = color_matches(found, key, search_attr)

    return found


def color_matches(found: List[Record], kw: str, search_attr: List[str]) -> List[Record]:
    """surround matching substrings with color codes for stdout printing

    Args:
        found (List[Record]): Records matching a given filter
        kw (str): regex to be matched for coloring
        search_attr (List[str]): Attributes which were considered in the filtering

    Returns:
        List[Record]: Records with matches surrounded by color codes
    """

    for i, f in enumerate(found):
        for a in search_attr:
            attrstr = getattr(found[i], a)
            key_regex = re.compile(kw, re.IGNORECASE)
            # find all matches of key regex in attribute string
            it = key_regex.finditer(attrstr)
            newattrstr = ""
            pos = 0

            for match in it:
                first = match.span()[0]
                second = match.span()[1]
                newattrstr = (
                    newattrstr
                    + attrstr[pos:first]
                    + "\033[1;31m"
                    + attrstr[first:second]
                    + "\033[0m"
                )
                pos = second

            newattrstr = newattrstr + attrstr[pos:]

            setattr(found[i], a, newattrstr)

    return found
