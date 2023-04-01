# -----------------------------------------------------------------------------------------------
#                               LARS PRINTING FUNCTIONS (to text)
# -----------------------------------------------------------------------------------------------

import re

from src.lars_globals import attr

delim = "---------------------------------------------------------------------------"


# global function we send it to
def lars_print(reclist, record, code, author, journal, title, titauth, date):
    # decide on what to print
    # record overrides code overrides everything else
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


# print -c
def print_codes(reclist):
    for r in reclist:
        print(r.code)


# print -r
def print_records(reclist):
    for r in reclist:
        print(delim)
        print("CODE: [" + r.code + "]" + r.ctgr)

        attrslice = attr[2:]

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


# everything else
def print_attrib(reclist, attrib):
    if len(attrib) > 1:
        print("")

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
            print("")


# -----------------------------------------------------------------------------------------------
#                                      aux functions
# -----------------------------------------------------------------------------------------------


# makes list of last names of authors based on auth entry
def auth_last_names(authstr):
    authlist = re.split(r",|\&", authstr)

    # last names = odd entries
    last = authlist[0::2]

    # remove annoying leading spaces
    last = [l.lstrip().rstrip() for l in last]

    return last


# splits string s in chunks of max width and returns them as list
def split_string(s, width):
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
