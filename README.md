<h1 align="center"> Book management system </h1>

Simple system for managing collection of books.

---

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [API](#API)

---

## Features
- View book list of books in the system
- Simple search by title, author(s), language, specific date or date range
- Advanced search with contain all fields or contain any field options
- Adding and editing books
- Feeding system's datebase from [Google Book API](https://developers.google.com/books/docs/v1/using#WorkingVolumes)
- Django REST Framework for simple GET API operations

---

## Setup

Use pip to install dependencies from requirements.txt:

  ```
  $ pip install -r requirements.txt
  ````

or pipenv to install dependencies from Pipfile:

  ```
   $ pipenv install
   $ pipenv shell
  ```

Run Django tests to check if everything is all right:

  ```
  $ python manage.py bookManagement/tests
  ```

Run Django server:

  ```
  $ python manage.py runserver
  ```

or:

  ```
  $ python manage.py runserver 0:8000
  ```

---

## API
For getting all books in the system use:

  ```
  /api/books
  ```

API has ability to search books by query string, for example:

  ```
  /api/books?title=Dziady&author=Adam+Mickiewicz
  ```

You can use same fields like in datebase:

  ```
  title
  authors
  publishedDate
  isbnType
  isbnId
  pageCount
  language
  ```

JSON response contains following fields:

  ```
  'count' - number of found books
  'next' - if response have next page, if so contains link to next page
  'previous' - if response have previous page, if so contains link to previous page
  'result' - found books
  ```

Default items per page is 10, you can paginate through results by adding '&page=':

  ```
  /api/books/?language=Polish&page=2
  ```
