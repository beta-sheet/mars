# -----------------------------------------------------------------------------------------------
#                               LARS PRINTING FUNCTIONS (to text)
# -----------------------------------------------------------------------------------------------

import re
from typing import List

from src.lars_globals import attr, Record

# delimiter for printing records
delim = "---------------------------------------------------------------------------"


def lars_print(
    reclist: List[Record],
    record: bool,
    code: bool,
    author: bool,
    journal: bool,
    title: bool,
    titauth: bool,
    date: bool,
) -> None:
    """Print selected attributes of entries in reclist

    Args:
        reclist (List[Record]): List of (filtered) records read from lars.txt
        record (bool): print everything contained in record (print -r)
        code (bool): Print codes
        author (bool): Print authors
        journal (bool): Print JRNL entry (journal, volume, pages)
        title (bool): Print document title
        titauth (bool): Print first+last author and title
        date (bool): Print year
    """

    # decide on what to print
    # record and code override everything else
    if record:
        print_records(reclist)
    elif code:
        print_codes(reclist)
    else:
        print_attr = []
        if author:
            print_attr.append("authNoLatex")
        if journal:
            print_attr.append("jrnl")
        if title:
            print_attr.append("titl")
        if titauth:
            print_attr.append("titauth")
        if date:
            print_attr.append("date")

        # default: title
        if len(print_attr) == 0:
            print_attr = ["titl"]

        # get the job done
        print_attrib(reclist, print_attr)


def print_codes(reclist: List[Record]) -> None:
    """Print codes only (print -c)

    Args:
        reclist (List[Record]): List of records
    """

    for r in reclist:
        print(r.code)


def print_records(reclist: List[Record]) -> None:
    """Print all attributes of records in reclist (print -r)

    Args:
        reclist (List[Record]): List of records to print
    """

    for r in reclist:
        print(delim)
        print("CODE: [" + r.code + "]" + r.ctgr)

        attrslice = attr[2:]  # remove code ant ctgr (already printed)

        for a in attrslice:
            if a == "auth":
                s = getattr(r, "authNoLatex")
            else:
                s = getattr(r, a)
            if s != "":
                # take some care of nice formatting
                slist = split_string(s, len(delim) - 6)
                print(a.upper() + ": " + slist.pop(0))
                for sl in slist:
                    print("      " + sl)

    print(delim)


def print_attrib(reclist: List[Record], attrib: List[str]) -> None:
    """Print selected attributes only

    Args:
        reclist (List[Record]): List of records to print
        attrib (List[str]): List of attributes to print
    """

    # in case of stacked arguments to print (e.g. print -atj) use delimiter
    # to improve readability
    if len(attrib) > 1:
        print(delim)

    # iterate over records to be printed
    for r in reclist:
        # print the correct title for books
        if not r.valid("titl") and r.valid("bkti"):
            title = r.bkti
        else:
            title = r.titl

        # loop over attributes to print
        for a in attrib:
            if (
                a == "titauth"
            ):  # this one is special - codes, first+last author and titles
                auth = auth_last_names(r.authNoLatex)
                if len(auth) == 1:
                    print("{0: <9}".format(r.code + ":") + "[" + auth[0] + "] " + title)
                elif len(auth) > 1:
                    print(
                        "{0: <9}".format(r.code + ":")
                        + "["
                        + auth[0]
                        + "/"
                        + auth[-1]
                        + "] "
                        + title
                    )
            elif a == "titl":  # print correct title for books
                print("{0: <9}".format(r.code + ":") + title)
            else:
                print("{0: <9}".format(r.code + ":") + getattr(r, a))

        # improve readability
        if len(attrib) > 1:
            print(delim)


# -----------------------------------------------------------------------------------------------
#                                      aux functions
# -----------------------------------------------------------------------------------------------


def auth_last_names(authstr: str) -> List[str]:
    """Make list of last names of authors based on auth entry

    Args:
        authstr (str): Raw auth entry of a given record

    Returns:
        List[str]: List containing last names only
    """

    authlist = re.split(r",|\&", authstr)

    # last names = odd entries
    last = authlist[0::2]

    # remove annoying leading spaces
    last = [l.lstrip().rstrip() for l in last]

    return last


def split_string(s: str, width: int) -> List[str]:
    """Splits string s in chunks of max width and returns them as list.

    Args:
        s (str): String to split
        width (int): Maximum width of chunks as number of characters

    Returns:
        List[str]: String s split into chunks
    """

    # split by whitespaces
    slist = s.split()

    # result
    res = []

    left = ""

    for w in slist:
        if len(left + w) > width:
            res.append(left.lstrip())
            left = w + " "
        else:
            left = left + w + " "

    res.append(left.lstrip())

    return res
