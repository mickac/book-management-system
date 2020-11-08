from django.test import Client, TestCase


class TestViews(TestCase):
    def test_book_add(self):
        client = Client()
        response = client.post('/book_add', {})
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_book_edit(self):
        client = Client()
        response = client.get('/book_add')
        resp = client.get(response)
        self.assertEqual(resp.status_code, 404)
