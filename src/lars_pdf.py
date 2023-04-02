# python interface to bash scripts for pdf operations (linux only)

import os
import subprocess
import tempfile
from typing import List


def lars_evince(codes: List[str], srcpath: str) -> None:
    """Open PDFs matching provided lars codes using evince.

    Args:
        codes (List[str]): List of lars codes
        srcpath (str): absolute path of src directory
    """

    script = srcpath + "/lars_evince.sh"

    for c in codes:
        subprocess.check_call(["bash", script, c])


def lars_extract(codes: List[str], srcpath: str, tag: bool) -> None:
    """Copy PDFs matching provided codes to working directory.

    Args:
        codes (List[str]): List of lars codes to extract
        srcpath (str): Absolute path of src directory
        tag (bool): If true, extracted PDF will be tagged with its code
           on the first page
    """

    script = srcpath + "/lars_extract.sh"

    for c in codes:
        subprocess.check_call(["bash", script, c])

    if tag:
        script = srcpath + "/lars_tag.sh"

        for c in codes:
            filename = c + ".pdf"
            subprocess.check_call(["bash", script, filename, c])


def lars_sum(codes: List[str], path: str, tag: bool, outfile: str) -> None:
    """Join the first pages of PDFs matching provided lars codes into a separate
    PDF document.

    Args:
        codes (List[str]): List of lars codes
        path (str): Root path of this package
        tag (bool): If true, extracted PDF will be tagged with its code on the
            first page
        outfile (str): Name/path to output file
    """

    # get WD
    cwd = os.getcwd()

    srcpath = path + "/src"

    # create a temporary directory to store extracted PDFs before assembling their
    # first pages
    with tempfile.TemporaryDirectory() as tempdir:
        # copy matching PDFs to tempdir
        os.chdir(tempdir)
        lars_extract(codes, srcpath, tag)

        # assemble 1st pages to a single document
        os.chdir(cwd)

        script = srcpath + "/lars_sum.sh"
        subprocess.check_call(["bash", script, tempdir, outfile])
