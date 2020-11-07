import unittest

from django.test import RequestFactory
from django.db.models import Q

from ..forms import BookForm
from ..models import Book
from ..modules.book_operations import BookOperations

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

    def test_simple_search(self):
        factory = RequestFactory()
        validKeywordDict = {
            "keyword": "title",
            "keyword": "author",
            "keyword": "language"
        }
        validKeywordQ = [
            Book.objects.filter(Q(title__icontains='title')),
            Book.objects.filter(Q(authors__icontains='authors')),
            Book.objects.filter(Q(language__icontains='language'))
        ]
        validDateExact = Book.objects.filter(Q(publishedDate__exact="2020-10-31"))
        validDateRange = Book.objects.filter(Q(publishedDate__range=["2020-10-10","2020-10-30"]))
        validDateExactRequest = factory.get('/simple_search', {'parameter': 'publishedDate',
                                                               'dateExact': '2020-10-31'})
        validDateRangeRequest = factory.get('/simple_search', {'parameter': 'dateRange',
                                                               'dateFrom': '2020-10-10',
                                                               'dateTo': "2020-10-30"})       
        iter = 0
        for i, j in validKeywordDict.items():
            iter += iter
            keyword = {i: j, "parameter": j}
            validKeywordRequest = factory.get('/simple_search', keyword)
            testKeyword = BookOperations.simple_search(validKeywordRequest)
            self.assertEqual(list(testKeyword), list(validKeywordQ[iter]))
        self.assertEqual(list(validDateExact), 
                         list(BookOperations.simple_search(validDateExactRequest)))
        self.assertEqual(list(validDateRange), 
                         list(BookOperations.simple_search(validDateRangeRequest)))

