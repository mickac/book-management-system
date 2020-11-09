import unittest

from ..modules.validators import IsbnValidator


class TestIsbnValidator(unittest.TestCase):
    validIsbnType13 = ["ISBN-13",
                       "123-1-1234-1234-1"]
    validIsbnType10 = ["ISBN-10",
                       "2-1234-4321-2"]
    invalidIsbnType13 = ["ISBN-13",
                         "123-1-1234-12---"]
    invalidIsbnType10 = ["ISBN-10",
                         "2-1234-43----"]
    validNoDashIsbn = "1231123412341"
    invalidNoDashIsbn = "123!!!39@1"
    validData = [validIsbnType13,
                 validIsbnType10]
    invalidData = [invalidIsbnType13,
                   invalidIsbnType10]

    def test_validate_dashes(self):
        """Testing if dashes validator validates places of dashesh well."""
        for i in TestIsbnValidator.validData:
            self.assertEqual(IsbnValidator(i[0], i[1]).validate_dashes(), None)
        for i in TestIsbnValidator.invalidData:
            with self.assertRaises(ValueError):
                IsbnValidator(i[0], i[1]).validate_dashes()
        self.assertEqual(IsbnValidator("ISBN-13",
                         TestIsbnValidator.validNoDashIsbn).validate_dashes(),
                         None)
        with self.assertRaises(ValueError):
            IsbnValidator("ISBN-10",
                          TestIsbnValidator.
                          invalidNoDashIsbn).validate_dashes()

    def test_validate_isbn_len(self):
        """Testing if len validator validates length of isbn well."""
        for i in TestIsbnValidator.validData:
            self.assertEqual(IsbnValidator(i[0], i[1]).validate_isbn_len(),
                             None)
        self.assertEqual(IsbnValidator("ISBN-13",
                         TestIsbnValidator.validNoDashIsbn).
                         validate_isbn_len(),
                         None)
        for i in TestIsbnValidator.invalidData:
            with self.assertRaises(ValueError):
                IsbnValidator(i[0], i[1]).validate_dashes()
        with self.assertRaises(ValueError):
            IsbnValidator("ISBN-10",
                          TestIsbnValidator.
                          invalidNoDashIsbn).validate_dashes()
