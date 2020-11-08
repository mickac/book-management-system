import unittest

from django.urls import resolve, reverse

from ..models import Book


class TestModels(unittest.TestCase):
    def test_model(self):
        """Testing adding object into DB, then removing it."""
        data_dict = {
            'title': 'test',
            'authors': 'test',
            'publishedDate': '2020-10-30',
            'isbnType': 'ISBN-10',
            'isbnId': '1337',
            'pageCount': '10',
            'image': 'http://google.com',
            'language': 'test'
        }
        response = Book(**data_dict)
        response.save()
        self.assertNotEqual(response, None)
        Book.objects.filter(isbnId='1337').delete()
