import unittest

from django.urls import resolve, reverse


class TestUrls(unittest.TestCase):
    def test_index(self):
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'index')

    def test_book_add(self):
        resolver = resolve('/book_add')
        self.assertEqual(resolver.view_name, 'book_add')

    def test_book_list(self):
        resolver = resolve('/book_list')
        self.assertEqual(resolver.view_name, 'book_list')

    def test_book_remove(self):
        url = reverse('book_remove', args=[1])
        self.assertEqual(url, '/book_remove_1')

    def test_book_search(self):
        resolver = resolve('/book_search')
        self.assertEqual(resolver.view_name, 'book_search')

    def test_book_edit(self):
        url = reverse('book_edit', args=[1])
        self.assertEqual(url, '/book_edit_1')

    def test_book_advanced_searching(self):
        resolver = resolve('/book_advanced_searching')
        self.assertEqual(resolver.view_name, 'book_advanced_searching')

    def test_feed_from_google(self):
        resolver = resolve('/feed_from_google')
        self.assertEqual(resolver.view_name, 'feed_from_google')

    def test_book_api(self):
        resolver = resolve('/api/books/')
        self.assertEqual(resolver.view_name, 'book_api')
