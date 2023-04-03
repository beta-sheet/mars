import re
from typing import List


def get_lars_codes_from_file(infilestr: str) -> List[str]:
    """Read file infilestr and search for anything that looks like a lars code.

    Args:
        infilestr (str): Name of file to parse for codes

    Returns:
        List[str]: List of unique lars codes
    """

    with open(infilestr[0], "r") as infile:
        data = infile.read()

    matches = re.findall("[A-Z][A-Z][0-9][0-9][.][0-9][0-9]?", data)
    matches = list(set(matches))

    return matches
