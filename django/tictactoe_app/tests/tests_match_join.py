from django.test import TestCase
import json
from rest_framework.test import APIClient
from rest_framework import status

from users_app.models import User
from tictactoe_app.factories import MatchFactory
from tictactoe_app.models import Match


class MatchJoinTestCase(TestCase):

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

        self.match = MatchFactory(player2=None) 


    def test_join_match(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post('/tictactoe_app/match-join/{}/'.format(self.match.id), format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['player2_username'],self.user.username)
        self.assertEqual(Match.objects.get(id=self.match.id).player2,self.user)


    def test_join_match_no_login(self):

        client = APIClient()

        response = client.post('/tictactoe_app/match-join/{}/'.format(self.match.id), format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(result['detail'], "Authentication credentials were not provided.")


    def test_join_match_not_empty(self):
        self.match.player2 = self.user
        self.match.save()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post('/tictactoe_app/match-join/{}/'.format(self.match.id), format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['non_field_errors'][0], "Can not Join to this Match")
