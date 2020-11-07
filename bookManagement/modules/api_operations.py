import re

from django.conf import settings
from ..models import Book

class operationsAPI:
    def create_query(request):
        searchdict = request.GET.copy()
        resultNumbers = request.GET.get("resultNumbers")
        API_url = "https://www.googleapis.com/books/v1/volumes?q="
        q = request.GET.get("q")
        if("q" in searchdict):
            searchdict.pop("q")
        searchdict.pop("resultNumbers")
        query = ""
        for x, y in searchdict.items():
            if x and y:
                query = query + "+" + x + ":" + y
        query = q + query + "&maxResults=" + resultNumbers + "&key=" + settings.GOOGLE_API_KEY
        if query:
            API_url = API_url + query
        if (q == ""):
            API_url = API_url.replace("+", "", 1)
        API_url = API_url.replace(" ", "-")
        return API_url

    def unpack_and_add(data):
        addIter = 0
        noItems = True
        isbn = isbnType = ""
        if data.get("items"):
            for i in data.get("items"):
                title = i["volumeInfo"].get("title")
                authors = i["volumeInfo"].get("authors")
                publishedDate = i["volumeInfo"].get("publishedDate")
                regex = "^\d\d\d\d[- /.]\d\d[- /.]\d\d$"
                if (publishedDate and not re.findall(regex, publishedDate)):
                    publishedDate = publishedDate + '-01-01'
                isbnId = i["volumeInfo"].get("industryIdentifiers")
                pageCount = i["volumeInfo"].get("pageCount")
                image = i["volumeInfo"].get("imageLinks")
                language = i["volumeInfo"].get("language")
                if (title and authors and image and publishedDate and
                   isbnId and pageCount and image and language):
                    if len(authors) > 1:
                        authors = ', '.join(authors)
                    else:
                        authors = authors[0]
                    image = image.get("thumbnail")
                    for j in isbnId:
                        if j["type"] == "ISBN_13":
                            isbn = j.get("identifier")
                            isbnType = "ISBN-13"
                        if j["type"] == "ISBN_10" and isbnType != "ISBN-13":
                            isbn = j.get("identifier")
                            isbnType = "ISBN-10"
                    if isbn:
                        noItems = False
                        book = Book(
                            title=title,
                            authors=authors,
                            publishedDate=publishedDate,
                            isbnType=isbnType,
                            isbnId=isbn,
                            pageCount=pageCount,
                            image=image,
                            language=language
                        )
                        try:
                            book.save()
                            addIter += 1
                        except:
                            pass
        return [addIter, noItems]
