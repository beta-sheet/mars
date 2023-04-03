import re
from typing import List

from src.util.lars_attr import attr
from src.util.record import Record


def read_lars_file(infile: str) -> List[Record]:
    """function for reading in lars textfile to records array

    Args:
        infile (str): Name of lars file (lars.txt)

    Returns:
        List[Record]: List of bibliography entries
    """

    # this is what we'll return
    records = []

    # read in content of larsfile as lines
    with open(infile, "r") as larsfile:
        content = larsfile.readlines()

    # trim off everything between _BEGIN_RECORDS_ and _END_RECORDS_
    content = [c.strip() for c in content]
    start = content.index("_BEGIN_RECORDS_")
    end = content.index("_END_RECORDS_")
    content = content[start + 1 : end]

    r = Record()

    # loop over lines
    for line in content:
        # remove comments
        line = line.split("#")[0]

        if not line == "" and not line.isspace():
            if line.startswith("----"):  # end of record
                if r.code != "":
                    c = r.code
                    r.set("code", c[c.find("[") + 1 : c.find("]")])
                    r.set("ctgr", c[c.find("]") + 1 :])

                records.append(r)
                r = Record()

            else:  # continuation of current record
                found = False
                lline = line.lower()
                for a in attr:
                    if lline.startswith(a):
                        r.set(a, line[6:])
                        found = True

                if not found:
                    r.append(r.last, line)

    # remove empty records
    records = [rec for rec in records if not rec.is_empty() and not rec.type == "KILL"]

    # make search-friendly rep of auths
    # These strings may appear in author entries of the lars file, which make searching difficult
    latexInAuth = ["\\\\v", "\\\\'", '\\\\"', "{", "}", "\\\\~", "\\\\`"]

    for i, rec in enumerate(records):
        rec.authNoLatex = rec.auth
        for s in latexInAuth:
            records[i].authNoLatex = re.sub(s, "", rec.authNoLatex)

        # also make copy of codes in case they get colored by "find", as this messes up PDF operations.
        rec.safe_code = rec.code

    return records
