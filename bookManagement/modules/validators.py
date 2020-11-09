import re


class IsbnValidator:
    def __init__(self, isbnType, isbnId):
        self.isbnType = isbnType
        self.isbnId = isbnId

    def validate_dashes(self):
        """Validating if number of dashes is correct for certain ISBN Type."""
        try:
            int(self.isbnId)
        except ValueError:
            if self.isbnType == "ISBN-10":
                if len(re.findall("^\d+-\d+-\d+-\d+$", self.isbnId)) == 0:
                    raise ValueError
            if self.isbnType == "ISBN-13":
                if len(re.findall("^\d+-\d+-\d+-\d+-\d+$", self.isbnId)) == 0:
                    raise ValueError

    def validate_isbn_len(self):
        """Validating if length of ISBN-10 is 10 and ISBN-13 is 13."""
        isbn_len = len(self.isbnId.replace("-", ""))
        if self.isbnType == "ISBN-10":
            if isbn_len != 10:
                raise ValueError
        elif self.isbnType == "ISBN-13":
            if isbn_len != 13:
                raise ValueError
        else:
            raise ValueError
