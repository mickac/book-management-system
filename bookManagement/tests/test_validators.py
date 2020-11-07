import unittest

from ..modules.validators import IsbnValidator


class TestIsbnValidator(unittest.TestCase):
    validIsbnIdType13 = ["123-1-1234-1234-1",
                         "ISBN-13"]
    validIsbnIdType10 = ["2-1234-4321-2",
                         "ISBN-10"]
    invalidIsbnIdType13 = ["123-1-1234-123--",
                           "ISBN-13"]
    invalidIsbnIdType10 = ["2-1234-4321--",
                           "ISBN-10"]
    validNoDashesIsbnId = "1231123412341"
    invalidNoDashesIsbnId = "123!!!39@1"
    validData = [validIsbnIdType13,
                 validIsbnIdType10]
    invalidData = [invalidIsbnIdType13,
                   invalidIsbnIdType10]

    def test_validate_dashes(self):
        for i in TestIsbnValidator.validData:
            for j in i:
                self.assertEqual(IsbnValidator.validate_dashes(i, j), None)
        self.assertEqual(IsbnValidator.validate_dashes(
                         TestIsbnValidator.validNoDashesIsbnId, "ISBN-13"),
                         None)
        """
        for i in TestIsbnValidator.invalidData:
            for j in i:
                with self.assertRaises(ValueError):
                    IsbnValidator.validate_dashes(i, j)

        with self.assertRaises(ValueError):
            IsbnValidator.validate_dashes(invalidNoDashesIsbnId, "ISBN-10")
        """

    def test_validate_isbn_len(self):
        for i in TestIsbnValidator.validData:
            for j in i:
                self.assertEqual(IsbnValidator.validate_isbn_len(i, j), None)
        self.assertEqual(IsbnValidator.validate_isbn_len(
                         TestIsbnValidator.validNoDashesIsbnId, "ISBN-13"),
                         None)
        """
        for i in TestIsbnValidator.invalidData:
            for j in i:
                with self.assertRaises(ValueError):
                    IsbnValidator.validate_dashes(i,j)
        with self.assertRaises(ValueError):
            IsbnValidator.validate_dashes(IsbnValidator.invalidNoDashesIsbnId,
                                          "ISBN-10")
        """
