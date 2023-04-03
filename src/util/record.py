# ---------------------------------------------------------------------------------------------------------------------------
#                                         CLASS RECORD
# ---------------------------------------------------------------------------------------------------------------------------


from typing import List

from src.util import attr


class Record:
    """Class for storing bibliography entries"""

    def __init__(self):
        """constructor - make sure all attributes are assigned to prevent runtime errors"""
        self.last = ""  # memory slot for last modified entry (as entries can span multiple lines)
        for a in attr:
            setattr(self, a, "")

    # set attribute a to s
    def set(self, a: str, s: str) -> None:
        """set attribute a to the value of s

        Args:
            a (str): name of attribute (field)
            s (str): value of field to be set
        """
        s = s.strip()
        setattr(self, a, s)
        self.last = a

    def append(self, a: str, s: str) -> None:
        """append string s to attribute a

        Args:
            a (str): name of attribute (field)
            s (str): value of field to be appended to current value
        """
        s = s.strip()
        orig = getattr(self, a)
        concat = orig + " " + s
        setattr(self, a, concat)
        self.last = a

    def lsrec(self) -> List[str]:
        """list all attributes - for debugging only

        Returns:
            List[str]: List of set attributes
        """
        return [
            a
            for a in dir(self)
            if not a.startswith("__") and not callable(getattr(self, a))
        ]

    def is_empty(self) -> bool:
        """Check if record is empty (i.e. if last was set via set() or append())

        Returns:
            bool: record is empty
        """
        return self.last == ""

    # check if attrib is a "valid" entry
    def valid(self, attrib: str) -> bool:
        """check if attrib field contains a "valid" entry

        Args:
            attrib (str): attribute of this record

        Returns:
            bool: True if value of attrib is valid
        """
        a = getattr(self, attrib)
        return a != "" and a.strip() != "-" and not a.startswith("XXX")
