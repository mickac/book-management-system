import unittest

from ..forms import BookForm


class TestBookOperations(unittest.TestCase):
    def test_book_add_or_edit(self):
        validData = {
                    "title": "test title",
                    "authors": "test author",
                    "publishedDate": "2020-12-21",
                    "isbnType": "ISBN-13",
                    "isbnId": "1234567891234",
                    "pageCount": "10",
                    "image": "https://google.com/",
                    "language": "polish"}
        invalidData = {
                    "title": "test title",
                    "authors": "test author",
                    "publishedDate": "2020-121",
                    "isbnType": "ISBN-13",
                    "isbnId": "1234567891234",
                    "pageCount": "10",
                    "image": "https://google.com/",
                    "language": "polish"}
        validForm = BookForm(validData)
        invalidForm = BookForm(invalidData)
        self.assertTrue(validForm.is_valid())
        self.assertFalse(invalidForm.is_valid())