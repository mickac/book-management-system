import unittest
import json

from django.test import RequestFactory
from django.conf import settings

from ..modules.api_operations import operationsAPI
from ..models import Book


class TestApiOperations(unittest.TestCase):
    def test_create_query(self):
        """Testing creating query for Google Books API."""
        factory = RequestFactory()
        validString = {
            "q": "query",
            "intitle": "title",
            "inauthor": "author",
            "inpublisher": "publisher",
            "subject": "subject",
            "isbn": "isbn",
            "lccn": "lccn",
            "oclc": "oclc",
            "resultNumbers": "5"
        }
        validRequest = factory.get('/feed_from_google', validString)
        validQuery = """https://www.googleapis.com/books/v1/volumes?q=query
                        +intitle:title
                        +inauthor:author
                        +inpublisher:publisher
                        +subject:subject
                        +isbn:isbn
                        +lccn:lccn
                        +oclc:oclc
                        &maxResults=5
                        &key=
                    """ + settings.GOOGLE_API_KEY
        validQuery = validQuery.replace("\n", "").replace(" ", "")
        self.assertEqual(operationsAPI.create_query(validRequest), validQuery)

    def test_unpack_and_add(self):
        """Testing if Google Books API response is parsed properly."""
        validDataJSON = json.loads("""{
                        "kind": "books#volumes",
                        "totalItems": 479,
                        "items": [
                            {
                                "kind": "books#volume",
                                "id": "RmmiCtcOIQEC",
                                "etag": "84IvMEmWCTg",
                                "selfLink": "https://www.googleapis.com/books/v1/volumes/RmmiCtcOIQEC",
                                "volumeInfo": {
                                    "title": "Dzieła Adama Mickiewicza",
                                    "subtitle": "Tom szósty",
                                    "authors": [
                                        "Adam Mickiewicz"
                                    ],
                                    "publishedDate": "1880",
                                    "industryIdentifiers": [
                                        {
                                            "type": "ISBN_13",
                                            "identifier": "NKP:3186292203"
                                        }
                                    ],
                                    "readingModes": {
                                        "text": false,
                                        "image": true
                                    },
                                    "pageCount": 353,
                                    "printType": "BOOK",
                                    "maturityRating": "NOT_MATURE",
                                    "allowAnonLogging": false,
                                    "contentVersion": "1.0.1.0.full.1",
                                    "panelizationSummary": {
                                        "containsEpubBubbles": false,
                                        "containsImageBubbles": false
                                    },
                                    "imageLinks": {
                                        "smallThumbnail": "http://books.google.com/books/content?id=RmmiCtcOIQEC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                                        "thumbnail": "http://books.google.com/books/content?id=RmmiCtcOIQEC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
                                    },
                                    "language": "pl",
                                    "previewLink": "http://books.google.pl/books?id=RmmiCtcOIQEC&printsec=frontcover&dq=inauthor:Adam-Mickiewicz&hl=&cd=1&source=gbs_api",
                                    "infoLink": "https://play.google.com/store/books/details?id=RmmiCtcOIQEC&source=gbs_api",
                                    "canonicalVolumeLink": "https://play.google.com/store/books/details?id=RmmiCtcOIQEC"
                                },
                                "saleInfo": {
                                    "country": "PL",
                                    "saleability": "FREE",
                                    "isEbook": true,
                                    "buyLink": "https://play.google.com/store/books/details?id=RmmiCtcOIQEC&rdid=book-RmmiCtcOIQEC&rdot=1&source=gbs_api"
                                },
                                "accessInfo": {
                                    "country": "PL",
                                    "viewability": "ALL_PAGES",
                                    "embeddable": true,
                                    "publicDomain": true,
                                    "textToSpeechPermission": "ALLOWED",
                                    "epub": {
                                        "isAvailable": false,
                                        "downloadLink": "http://books.google.pl/books/download/Dzie%C5%82a_Adama_Mickiewicza.epub?id=RmmiCtcOIQEC&hl=&output=epub&source=gbs_api"
                                    },
                                    "pdf": {
                                        "isAvailable": false
                                    },
                                    "webReaderLink": "http://play.google.com/books/reader?id=RmmiCtcOIQEC&hl=&printsec=frontcover&source=gbs_api",
                                    "accessViewStatus": "FULL_PUBLIC_DOMAIN",
                                    "quoteSharingAllowed": false
                                }
                            }
                        ]
                    }""")
        self.assertFalse(operationsAPI.unpack_and_add(validDataJSON)[1])
        Book.objects.filter(isbnId='NKP:3186292203').delete()
