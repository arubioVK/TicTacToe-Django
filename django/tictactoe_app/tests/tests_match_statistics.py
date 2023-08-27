from django.test import TestCase
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.db.models import Q


from users_app.models import User
from tictactoe_app.factories import MatchFactory
from tictactoe_app.models import Match


class MatchStatisticsTestCase(TestCase):

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

        for i in range(5):
            MatchFactory(player1=self.user, winner=self.user)
        for i in range(10):
            MatchFactory(player1=self.user)


    def test_statistics_match(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.get('/tictactoe_app/matches-statistics/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        matches_finish = Match.objects.filter(Q(player1=self.user)|Q(player2=self.user)).filter(finish=True)
        self.assertEqual(matches_finish.count(), result['total_matches_finish'])
        self.assertEqual(matches_finish.filter(winner=self.user).count(), result['wins'])
        self.assertEqual(matches_finish.filter(winner__isnull=True).count(), result['draws'])
        self.assertEqual(matches_finish.exclude(winner=self.user).exclude(winner__isnull=True).count(), result['loses'])


    def test_statistics_match_no_login(self):

        client = APIClient()

        response = client.post('/tictactoe_app/matches-statistics/', format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(result['detail'], "Authentication credentials were not provided.")


