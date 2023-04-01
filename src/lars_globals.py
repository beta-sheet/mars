import re

# --------------------------------------------------------------------------------------------------------------------------
#                           GLOBAL VARS
# --------------------------------------------------------------------------------------------------------------------------
# some globals we have to keep up to date with the evolution of the format of lars.txt

# ALL possible entries that might appear in lars.txt (a not recognized entry will be appended to the previous entry!)
attr = [
    "code",
    "ctgr",
    "auth",
    "date",
    "titl",
    "bkti",
    "jrnl",
    "volu",
    "edit",
    "edtn",
    "publ",
    "page",
    "webp",
    "type",
    "comm",
    "xcls",
]

# some latexery which might appear in author entries (as regexes)
latexInAuth = ["\\\\v", "\\\\'", '\\\\"', "{", "}", "\\\\~", "\\\\`"]


# ---------------------------------------------------------------------------------------------------------------------------
#                                         CLASS RECORD
# ---------------------------------------------------------------------------------------------------------------------------
# this is how we store the individual records
class record:
    # constructor - make sure all attributes are assigned to prevent runtime errors
    def __init__(self):
        self.last = ""  # memory slot for last modified entry
        for a in attr:
            setattr(self, a, "")

    # set attribute a to s
    def set(self, a, s):
        s = s.lstrip().rstrip()
        setattr(self, a, s)
        self.last = a

    # append string s to attribute a
    def append(self, a, s):
        s = s.rstrip().lstrip()
        orig = getattr(self, a)
        concat = orig + " " + s
        setattr(self, a, concat)
        self.last = a

    def lsrec(self):  # list all current attributes (not needed at the moment)
        return [
            a
            for a in dir(self)
            if not a.startswith("__") and not callable(getattr(self, a))
        ]

    def isEmpty(self):
        return self.last == ""

    # check if attrib is a "valid" entry
    def valid(self, attrib):
        a = getattr(self, attrib)
        return a != "" and a.lstrip().rstrip() != "-" and not a.startswith("XXX")


# ---------------------------------------------------------------------------------------------------------------------------
#                                            FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------------


# function for reading in lars textfile to records array
def read_in(infile):
    # this is what we'll return
    records = []

    # open lars file for reading
    larsfile = open(infile, "r")

    # temporary variables for parsing lars file
    in_records = False
    r = record()

    # loop over lines
    for line in larsfile:
        # remove comments
        line = line.split("#")[0]

        if in_records and not line == "" and not line.isspace():
            if line.startswith("----"):
                if r.code != "":
                    c = r.code
                    r.set("code", c[c.find("[") + 1 : c.find("]")])
                    r.set("ctgr", c[c.find("]") + 1 :])

                records.append(r)
                r = record()

            elif "_END_RECORDS_" in line:
                in_records = False
                break

            else:
                found = False
                lline = line.lower()
                for a in attr:
                    if lline.startswith(a):
                        r.set(a, line[6:])
                        found = True

                if not found:
                    r.append(r.last, line)

        else:
            if "_BEGIN_RECORDS_" in line:
                in_records = True

    # remove empty records
    records = [rec for rec in records if not rec.isEmpty() and not rec.type == "KILL"]

    # make search-friendly rep of auths
    for i, rec in enumerate(records):
        rec.authNoLatex = rec.auth
        for s in latexInAuth:
            records[i].authNoLatex = re.sub(s, "", rec.authNoLatex)

    larsfile.close()

    return records


# read file infilestr and search for anything that looks like a lars code
def get_lars_codes_file(infilestr):
    infile = open(infilestr[0], "r")

    # read in whole file as a string
    data = infile.read().replace("\n", "")

    matches = re.findall("[A-Z][A-Z][0-9][0-9][.][0-9][0-9]?", data)

    infile.close()

    matches = list(set(matches))

    return matches


# read latex file infilestr and search for anything that looks like \cite{larscode}
def get_lars_codes_latex(infilestr):
    infile = open(infilestr, "r")

    # read in whole file as a string
    data = infile.read().replace("\n", "")

    matches = re.findall("\\\\cite\{.*?\}|\\\\citenum\{.*?\}", data)

    matches = get_lars_codes_str(matches)

    infile.close()

    return matches


# parse input string for lars codes
def get_lars_codes_str(codestr):
    codes = []

    for c in codestr:
        matches = re.findall("[A-Z][A-Z][0-9][0-9][.][0-9][0-9]?", c)

        for m in matches:
            codes.append(m)

        codes = list(set(codes))

    return codes
