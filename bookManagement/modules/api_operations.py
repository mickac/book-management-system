from django.conf import settings


class operationsAPI:
    def createQuery(request):
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
