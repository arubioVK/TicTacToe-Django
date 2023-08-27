from django.test import TestCase
import json
from rest_framework.test import APIClient
from rest_framework import status

from users_app.models import User


class MatchCreateTestCase(TestCase):

    def setUp(self):

        user = User(
            email='player@example.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )
        user.set_password('example1234')
        user.save()

        client = APIClient()
        response = client.post(
                '/users_app/login/', {
                'username': 'testing_login',
                'password': 'example1234',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.token = result['token']
        self.user = user


    def test_create_match(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = client.post('/tictactoe_app/match-create/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)


    def test_create_match_no_login(self):

        client = APIClient()

        response = client.post('/tictactoe_app/match-create/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(result['detail'], "Authentication credentials were not provided.")

