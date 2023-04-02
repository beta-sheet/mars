# -----------------------------------------------------------------------------------------------
#                               LARS FILE TO BIBTEX CONVERSION
# -----------------------------------------------------------------------------------------------
#
# This function takes the records list as input (read-in lars.txt) and writes the bibtex .bib
# file outfile. Currently supported doc types are PAPR (@article), BOOK (@book), CHAP
# (@incollection) and SFTW (@misc). Other entries will not be included in the bib file
# Other than that, if the generated bib file doesn't compile, it is most likely caused by bugs
# and format inconsistencies in the lars file


# -----------------------------------------------------------------------------------------------
#                                      imports
# -----------------------------------------------------------------------------------------------

import datetime
import re
import os
from typing import List

from src.lars_globals import Record


# -----------------------------------------------------------------------------------------------
#                                      main function
# -----------------------------------------------------------------------------------------------


def lars_bibtex(records: List[Record], outfile: str, options: List[str]) -> None:
    """Write bibtex file containing entries for the given records

    Args:
        records (List[Record]): List of bibliography entries as records
        outfile (str): Name of bib file to write
        options (List[str]): Extra options, currently only used for reverse author format
    """

    # create or overwrite bib file
    bibfile = open(outfile, "w")

    timestamp = datetime.datetime.now().strftime("%a %b %d %Y %H:%M")

    bibfile.write("% LARS file in bibtex format\n")
    bibfile.write("% converted by lars bibtex on " + timestamp + "\n\n\n")

    # set function for generating the author entries depending on whether -r flag is set
    if "r" in options:
        auth_func = bibtex_reverse_auth
    else:
        auth_func = bibtex_compat_auth

    for r in records:
        # make entries bibtex-compatible
        auth = auth_func(r.auth)
        jrnl, vol, page = bibtex_compat_jrnl(r.jrnl)
        titl = bibtex_compat_str(r.titl)

        # -------------------------- paper -----------------------------
        if r.type == "PAPR":
            bibfile.write("@article{" + r.code + ",\n")

            # required fields: author, title, journal, year, volume
            # title = {{title}} to prevent decapitalization
            bibfile.write('''author\t  = "''' + auth + """",\n""")
            bibfile.write("""title\t  = {{""" + titl + """}},\n""")
            bibfile.write('''journal\t  = "''' + jrnl + """",\n""")
            bibfile.write('''volume\t  = "''' + vol + """",\n""")
            bibfile.write('''year\t  = "''' + r.date + '''"''')

            # optional fields: pages
            if page != "":
                bibfile.write(''',\npages\t  = "''' + page + '''"''')

            bibfile.write("\n}\n\n\n")

        # -------------------------- book ------------------------------
        elif r.type == "BOOK":
            bibfile.write("@book{" + r.code + ",\n")

            bkti = bibtex_compat_str(r.bkti)
            publ = bibtex_compat_str(r.publ)

            # required fields: author/editor, title, publisher, year
            bibfile.write('''author\t  = "''' + auth + """",\n""")
            bibfile.write("""title\t  = {{""" + bkti + """}},\n""")
            bibfile.write('''publisher = "''' + publ + """",\n""")
            bibfile.write('''year\t  = "''' + r.date + '''"''')

            # optional fields: volume, edition, ...
            if r.valid("volu"):
                bibfile.write(''',\nvolume\t  = "''' + r.volu + '''"''')

            if r.valid("edtn"):
                edtn = bibtex_compat_str(r.edtn)
                bibfile.write(''',\nedition\t  = "''' + edtn + '''"''')

            bibfile.write("\n}\n\n\n")

        # -------------------------- chapter ----------------------------
        elif r.type == "CHAP":
            bibfile.write("@incollection{" + r.code + ",\n")

            bkti = bibtex_compat_str(r.bkti)

            # required fields: author/editor, title, booktitle,  year
            bibfile.write('''author\t  = "''' + auth + """",\n""")
            bibfile.write("""title\t  = {{""" + titl + """}},\n""")
            bibfile.write("""booktitle = {{""" + bkti + """}},\n""")
            bibfile.write('''year\t  = "''' + r.date + '''"''')

            # optional fields: editor, volume, pages, publisher
            if r.valid("publ"):
                publ = bibtex_compat_str(r.publ)
                bibfile.write(""",\npublisher = {{""" + publ + """}}""")

            if r.valid("edit"):
                edit = auth_func(r.edit)
                bibfile.write(''',\neditor\t  = "''' + edit + '''"''')

            if r.valid("volu"):
                bibfile.write(''',\nvolume\t  = "''' + r.volu + '''"''')

            if page != "":
                bibfile.write(''',\npages\t  = "''' + page + '''"''')

            bibfile.write("\n}\n\n\n")

        # -------------------------- software ----------------------------
        elif r.type == "SFTW":
            bibfile.write("@misc{" + r.code + ",\n")

            # some entries are formated url, access date - we only want url
            webp = r.webp.split(",")[0]

            # no required fields
            # but all sftw lars entries should have: author, title, webp and date
            if r.valid("auth"):
                bibfile.write('''author\t  = "''' + auth + """",\n""")
            if r.valid("titl"):
                bibfile.write("""title\t  = {{""" + titl + """}},\n""")
            if r.valid("webp"):
                bibfile.write("""howpublished = {\\texttt{""" + webp + """}},\n""")
            if r.valid("date"):
                bibfile.write('''year\t  = "''' + r.date + '''"''')

            bibfile.write("\n}\n\n\n")

        # -------------------------- other ----------------------------------
        else:
            bibfile.write(
                "% " + r.code + ": I don't know how to handle type " + r.type + "\n"
            )

    bibfile.close()


# -----------------------------------------------------------------------------------------------
#                                      aux functions
# -----------------------------------------------------------------------------------------------


def auth_names(name: str) -> str:
    """if more than one last name, put {} around it

    Args:
        name (str): String with author name(s)

    Returns:
        str: Names wrapped in braces if multiple
    """
    if len(name.split()) > 1:
        return "{" + name.strip() + "}"
    else:
        return name


def bibtex_compat_auth(authstr: str) -> str:
    """make bibtex-compatible author entry ("and"-separated) in the format Lastname, First.

    Args:
        authstr (str): author entry read from the lars file

    Returns:
        str: bibtex-compatible author entry
    """

    # substitute double quotes indise auth entries (annoying Student)
    authstr = re.sub(r'"(.*?)"', r"''\1``", authstr)

    # bibtex requires space between abbr of multiple 1st names
    authstr = re.sub("\.", ". ", authstr)

    # split in [last1, first1, last2, first2, ...]
    # and make iterable object (iterate with next(authIter)
    authlist = re.split(r",|\&", authstr)
    authIter = iter(authlist)

    # make list of authors, with first+last name concatenated
    if len(authlist) > 1:
        authlist = [auth_names(a) + "," + next(authIter, "") for a in authIter]

    # readability enhancement
    authlist = [a.strip() for a in authlist]

    # ... and make string out of it again
    res = " and ".join(authlist)

    res = bibtex_compat_str(res)

    return res


def bibtex_reverse_auth(authstr: str) -> str:
    """make bibtex-compatible author entry ("and"-separated) in REVERSE format (First. Lastname)

    Args:
        authstr (str): author entry read from the lars file

    Returns:
        str: bibtex-compatible author entry
    """

    # substitute double quotes indise auth entries (annoying Student)
    authstr = re.sub(r'"(.*?)"', r"''\1``", authstr)

    # bibtex requires space between abbr of multiple 1st names
    authstr = re.sub("\.", ". ", authstr)

    # split in [last1, first1, last2, first2, ...]
    # and make iterable object (iterate with next(authIter)
    authIter = iter(re.split(r",|\&", authstr))

    # make list of authors, with first+last name concatenated
    authlist = [next(authIter, "") + auth_names(a) for a in authIter]

    # readability enhancement
    authlist = [a.strip() for a in authlist]

    # ... and make string out of it again
    res = " and ".join(authlist)

    res = bibtex_compat_str(res)

    return res


def bibtex_compat_jrnl(jrnlstr: str) -> List[str]:
    """plit jrnl record in journal, volume and page

    Args:
        jrnlstr (str): raw JRNL entry in bibfile

    Returns:
        List[str]: [journal, volume, pages]
    """

    jrnlstr = bibtex_compat_str(jrnlstr)

    # separate in journal name+vol, page
    jrnllist = jrnlstr.split(",")

    if len(jrnllist) < 2:
        jrnl = jrnlstr
        vol = ""
        page = ""

    else:
        # last entry is the page
        page = jrnllist.pop().strip().split("/")[0]
        jrnlvol = "".join(jrnllist)

        # now the volume is the last element in the remaining jrnllist
        jrnllist = jrnlvol.split()
        vol = jrnllist.pop()

        jrnl = " ".join(jrnllist)

    return [jrnl, vol, page]


def bibtex_compat_str(s: str) -> str:
    """make the string compilable inside quotes

    Args:
        s (str): raw string from lars file

    Returns:
        str: Adapted string which can be enclosed by ""
    """

    # who the hell wrote those {\i} entries...
    s = re.sub(r"\{\\i\}", "i", s)

    # surround \" and \"{} in braces
    s = re.sub(r'(\\"[a-zA-Z])', r"{\1}", s)
    s = re.sub(r'(\\"\{[a-zA-Z]\})', r"{\1}", s)

    # surround \' and \'{} in braces
    s = re.sub(r"(\\'[a-zA-Z])", r"{\1}", s)
    s = re.sub(r"(\\'\{[a-zA-Z]\})", r"{\1}", s)
    s = re.sub(r"\\''([a-zA-Z])", r"{\"\1}", s)
    s = re.sub(r"\\``([a-zA-Z])", r"{\"\1}", s)

    # surround \~
    s = re.sub(r"(\\~[a-zA-Z])", r"{\1}", s)
    s = re.sub(r"(\\~\{[a-zA-Z]\})", r"{\1}", s)

    # common bug in lars file
    s = re.sub(" &", " \\&", s)

    return s
