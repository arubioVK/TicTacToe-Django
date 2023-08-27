from django.test import TestCase
import json
from rest_framework.test import APIClient
from rest_framework import status

from users_app.models import User
from tictactoe_app.factories import MatchFactory
from tictactoe_app.models import Match


class MatchDetailTestCase(TestCase):

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
        self.match = MatchFactory() 


    def test_detail_match(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.get('/tictactoe_app/match-detail/{}/'.format(self.match.id), format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['X'],self.match.player1.username)
        self.assertEqual(result['O'],self.match.player2.username)
        self.assertEqual(result['turn'],self.match.turn)


    def test_detail_match_draw(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.match.winner=None
        self.match.save()
        response = client.get('/tictactoe_app/match-detail/{}/'.format(self.match.id), format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['winner'],'Draw')


