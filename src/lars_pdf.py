# python interface to bash scripts for pdf operations (linux only)

import os
import subprocess
import tempfile
from typing import List


def lars_evince(codes: List[str], root_path: str) -> None:
    """Open PDFs matching provided lars codes using evince.

    Args:
        codes (List[str]): List of lars codes
        root_path (str): absolute path of the base directory of this repo
    """

    script = os.path.join(root_path, "src/bash/lars_evince.sh")

    for c in codes:
        subprocess.check_call(["bash", script, root_path, c])


def lars_extract(codes: List[str], root_path: str, tag: bool) -> None:
    """Copy PDFs matching provided codes to working directory.

    Args:
        codes (List[str]): List of lars codes to extract
        root_path (str): absolute path of the base directory of this repo
        tag (bool): If true, extracted PDF will be tagged with its code
           on the first page
    """

    script = os.path.join(root_path, "src/bash/lars_extract.sh")

    for c in codes:
        subprocess.check_call(["bash", script, root_path, c])

    if tag:
        script = os.path.join(root_path, "src/bash/lars_tag.sh")

        for c in codes:
            filename = c + ".pdf"
            subprocess.check_call(["bash", script, filename, c])


def lars_sum(codes: List[str], root_path: str, tag: bool, outfile: str) -> None:
    """Join the first pages of PDFs matching provided lars codes into a separate
    PDF document.

    Args:
        codes (List[str]): List of lars codes
        root_path (str): Root path of this repo
        tag (bool): If true, extracted PDF will be tagged with its code on the
            first page
        outfile (str): Name/path to output file
    """

    # get WD
    cwd = os.getcwd()

    # create a temporary directory to store extracted PDFs before assembling their
    # first pages
    with tempfile.TemporaryDirectory() as tempdir:
        # copy matching PDFs to tempdir
        os.chdir(tempdir)
        lars_extract(codes, root_path, tag)

        # assemble 1st pages to a single document
        os.chdir(cwd)

        script = os.path.join(root_path, "src/bash/lars_sum.sh")
        subprocess.check_call(["bash", script, tempdir, outfile])
