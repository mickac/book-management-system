from django.test import Client, TestCase
from django.urls import reverse

from ..models import Book


class TestViews(TestCase):
    def test_book_add(self):
        client = Client()
        response = client.post('/book_add', {})
        self.assertFormError(response, 'form', 'title',
                             'This field is required.')

    def test_book_edit(self):
        client = Client()
        response = client.get('/book_edit')
        resp = client.get(response)
        self.assertEqual(resp.status_code, 404)

    def test_book_remove(self):
        client = Client()
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
        book = Book(**data_dict)
        book.save()
        pk = Book.objects.values_list('pk', flat=True).get(**data_dict)
        response = client.post(reverse('book_remove', kwargs={'pk': pk}))
        client.get(response)
        self.assertFalse(Book.objects.filter(pk=pk).exists())
