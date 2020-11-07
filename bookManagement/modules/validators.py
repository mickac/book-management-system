import re


class IsbnValidator:
    def validate_dashes(isbnType, isbnId):
        """Validating if number of dashes is correct for certain ISBN Type."""
        try:
            int(isbnId)
        except ValueError:
            if isbnType == "ISBN-10":
                if len(re.findall("^\d+-\d+-\d+-\d+$", isbnId)) == 0:
                    raise ValueError
            if isbnType == "ISBN-13":
                if len(re.findall("^\d+-\d+-\d+-\d+-\d+$", isbnId)) == 0:
                    raise ValueError

    def validate_isbn_len(isbnType, isbnId):
        """Validating if length of ISBN-10 is 10 and ISBN-13 is 13."""
        isbn_len = len(isbnId.replace("-", ""))
        if isbnType == "ISBN-10":
            if isbn_len != 10:
                raise ValueError
        elif isbnType == "ISBN-13":
            if isbn_len != 13:
                raise ValueError
