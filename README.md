<h1 align="center"> Book management system </h1>

## Table of Contents

- [Features](#features)
- [Setup](#setup)

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
