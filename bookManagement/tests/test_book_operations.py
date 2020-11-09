import unittest

from django.test import RequestFactory
from django.db.models import Q

from ..forms import BookForm
from ..models import Book
from ..modules.book_operations import BookOperations


class TestBookOperations(unittest.TestCase):
    factory = RequestFactory()
    testQ = Q()

    def test_book_add_or_edit(self):
        """Scenarios for valid form and invalid form
           in adding or editing book.
        """
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
        validKeywordDict = {
            "keyword": ["title", "authors", "language"],
            "parameter": ["parameter", "parameter", "parameter"]
        }
        validKeywordQ = [
            Book.objects.filter(Q(title__icontains='title')),
            Book.objects.filter(Q(authors__icontains='authors')),
            Book.objects.filter(Q(language__icontains='language'))
        ]
        validDateExact = Book.objects.filter(
            Q(publishedDate__exact='2020-10-31'))
        validDateRange = Book.objects.filter(
            Q(publishedDate__range=['2020-10-10', '2020-10-30']))
        validDateExactRequest = TestBookOperations.factory.get(
                                                   '/simple_search', {
                                                        'parameter':
                                                        'publishedDate',
                                                        'dateExact':
                                                        '2020-10-31'})
        validDateRangeRequest = TestBookOperations.factory.get(
                                                   '/simple_search', {
                                                        'parameter':
                                                        'dateRange',
                                                        'dateFrom':
                                                        '2020-10-10',
                                                        'dateTo':
                                                        '2020-10-30'})
        """ Scenario for any keyword exluding dates."""
        for i in range(3):
            keyword = {
                    "keyword": validKeywordDict["keyword"][i],
                    "parameter": validKeywordDict["keyword"][i]
                      }
            validKeywordRequest = TestBookOperations.factory.get(
                                            '/simple_search', keyword)
            testKeyword = BookOperations(validKeywordRequest).simple_search()
            self.assertEqual(list(testKeyword), list(validKeywordQ[i]))
        """Scenario for date range."""
        self.assertEqual(list(validDateExact),
                         list(BookOperations(
                              validDateExactRequest).simple_search()))
        """Scenario for date exact."""
        self.assertEqual(list(validDateRange),
                         list(BookOperations(
                              validDateRangeRequest).simple_search()))

    def test_advanced_search(self):
        searchdict = {
            "title": "title",
            "authors": "authors",
            "language": "language",
            "isbnId": "1234567891",
            "pageCount": "0",
            "exactDate": "",
            "dateStart": "",
            "dateEnd": "",
            "parameter": "",
            "dateParameter": ""
        }
        """Scenario with include any of fields."""
        validSearchAny = searchdict.copy()
        validSearchAny["parameter"] = "1"
        validSearchAny["exactDate"] = "2020-10-30"
        validSearchAny["dateStart"] = "2020-10-01"
        validSearchAny["dateEnd"] = "2020-10-30"
        validSearchAny["publishedDate"] = validSearchAny["exactDate"]
        validSearchFAny = TestBookOperations.factory.get(
                                        '/advanced_search', validSearchAny)
        validSearchTestAny = BookOperations(validSearchFAny).advanced_search()
        validSearchAny["publishedDate__range"] = [validSearchAny["dateStart"],
                                                  validSearchAny["dateEnd"]]
        validSearchAny.pop("dateStart")
        validSearchAny.pop("dateEnd")
        validSearchAny.pop("exactDate")
        validSearchAny.pop("dateParameter")
        validSearchAny.pop("parameter")
        for searchword in validSearchAny:
                TestBookOperations.testQ |= Q(**{searchword:
                                              validSearchAny[searchword]})
        validSearchFilterAny = Book.objects.filter(
                               TestBookOperations.testQ)
        self.assertEqual(list(validSearchFilterAny),
                         list(validSearchTestAny))
        """Scenario with include all of fields with data range."""
        validSearchAllParam1 = searchdict.copy()
        validSearchAllParam1["parameter"] = "2"
        validSearchAllParam1["dateParameter"] = "1"
        validSearchAllParam1["dateStart"] = "2020-10-01"
        validSearchAllParam1["dateEnd"] = "2020-10-30"
        validSearchFAllParam1 = TestBookOperations.factory.get(
                                        '/advanced_search',
                                        validSearchAllParam1)
        validSearchTestAllParam1 = BookOperations(
                                   validSearchFAllParam1).advanced_search()
        validSearchAllParam1["publishedDate__range"] = [
                                                validSearchAllParam1[
                                                    "dateStart"],
                                                validSearchAllParam1[
                                                    "dateEnd"]]
        validSearchAllParam1.pop("parameter")
        validSearchAllParam1.pop("dateParameter")
        validSearchAllParam1.pop("dateStart")
        validSearchAllParam1.pop("dateEnd")
        validSearchAllParam1.pop("exactDate")
        for searchword in validSearchAllParam1:
                TestBookOperations.testQ &= Q(**{searchword:
                                              validSearchAllParam1[
                                                         searchword]})
        validSearchFilterAllParam1 = Book.objects.filter(
                                     TestBookOperations.testQ)
        self.assertEqual(list(validSearchFilterAllParam1),
                         list(validSearchTestAllParam1))
        """Scenario with include all of fields with data exact."""
        validSearchAllParam2 = searchdict.copy()
        validSearchAllParam2["parameter"] = "2"
        validSearchAllParam2["dateParameter"] = "2"
        validSearchAllParam2["exactDate"] = "2020-10-30"
        validSearchAllParam2["publishedDate"] = validSearchAllParam2[
                                                           "exactDate"]
        validSearchFAllParam2 = TestBookOperations.factory.get(
                                        '/advanced_search',
                                        validSearchAllParam2)
        validSearchTestAllParam2 = BookOperations(
                                   validSearchFAllParam2).advanced_search()
        validSearchAllParam2.pop("parameter")
        validSearchAllParam2.pop("dateParameter")
        validSearchAllParam2.pop("dateStart")
        validSearchAllParam2.pop("dateEnd")
        validSearchAllParam2.pop("exactDate")
        for searchword in validSearchAllParam2:
                TestBookOperations.testQ &= Q(**{searchword:
                                              validSearchAllParam2[
                                                        searchword]})
        validSearchFilterAllParam2 = Book.objects.filter(
                                     TestBookOperations.testQ)
        self.assertEqual(list(validSearchFilterAllParam2),
                         list(validSearchTestAllParam2))
