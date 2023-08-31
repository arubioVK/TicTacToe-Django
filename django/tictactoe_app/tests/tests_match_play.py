from django.test import TestCase
import json
from rest_framework.test import APIClient
from rest_framework import status

from users_app.models import User
from tictactoe_app.factories import MatchFactory
from tictactoe_app.models import Match
from users_app.factories import UserFactory

class MatchPlayTestCase(TestCase):

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
        self.player =  UserFactory()

        self.match = MatchFactory(player1=user, player2=self.player,  finish=False) 


    def test_play_match(self):
        match = MatchFactory(player1=self.user, player2=self.player, finish=False, winner=None, turn=1, row0column0=None, row0column1=None, row0column2=None, row1column0=None, row1column1=None, row1column2= None, row2column0= None, row2column1= None, row2column2=None)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post('/tictactoe_app/match-play/{}/'.format(match.id), {"row":0,"column":0}, format='json')


        result = json.loads(response.content)
        match = Match.objects.get(id=match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(match.row0column0,self.user)
        self.assertEqual(match.turn, 2)


    def test_play_match_win_horizontal(self):
        match = MatchFactory(player1=self.user, finish=False, winner=None, turn=1, row0column0=None, row0column1=self.user, row0column2=self.user, row1column0=None, row1column1=None, row1column2= None, row2column0= None, row2column1= None, row2column2=None)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post('/tictactoe_app/match-play/{}/'.format(match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        match = Match.objects.get(id=match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(match.row0column0,self.user)
        self.assertEqual(match.turn, 2)
        self.assertEqual(match.finish, True)
        self.assertEqual(match.winner, self.user)


    def test_play_match_vertical(self):
        match = MatchFactory(player1=self.user, player2=self.player, finish=False, winner=None, turn=1, row0column0=None, row0column1=None, row0column2=None, row1column0=self.user, row1column1=None, row1column2= None, row2column0= self.user, row2column1= None, row2column2=None)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post('/tictactoe_app/match-play/{}/'.format(match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        match = Match.objects.get(id=match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(match.row0column0,self.user)
        self.assertEqual(match.turn, 2)
        self.assertEqual(match.finish, True)
        self.assertEqual(match.winner, self.user)


    def test_play_match_diagonal(self):
        match = MatchFactory(player1=self.user, player2=self.player, finish=False, winner=None, turn=1, row0column0=None, row0column1=None, row0column2=None, row1column0=None, row1column1=self.user, row1column2= None, row2column0= None, row2column1= None, row2column2=self.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post('/tictactoe_app/match-play/{}/'.format(match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        match = Match.objects.get(id=match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(match.row0column0,self.user)
        self.assertEqual(match.turn, 2)
        self.assertEqual(match.finish, True)
        self.assertEqual(match.winner, self.user)


    def test_play_match_no_login(self):
       
        client = APIClient()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(result['detail'], "Authentication credentials were not provided.")


    def test_play_match_no_user(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.player1 = self.player
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['non_field_errors'][0], 'Can not play')


    def test_play_match_no_finish(self):
        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.finish = True
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['non_field_errors'][0], "Can not move, the match is over")


    def test_play_match_player1_turn(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.turn = 1
        self.match.row0column0 = None
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Match.objects.get(id=self.match.id).row0column0,self.user)


    def test_play_match_player1_no_turn(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.turn = 2
        self.match.row0column0 = None
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['non_field_errors'][0], "Can not move, it´s not your turn")


    def test_play_match_player2_turn(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.player1 = self.player
        self.match.player2 = self.user
        self.match.turn = 2
        self.match.row0column0 = None
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Match.objects.get(id=self.match.id).row0column0,self.user)


    def test_play_match_player2_no_turn(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.player1 = self.player
        self.match.player2 = self.user
        self.match.turn = 1
        self.match.row0column0 = None
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['non_field_errors'][0], "Can not move, it´s not your turn")


    def test_play_match_no_turn(self):

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.match.turn = 1
        self.match.save()

        response = client.post('/tictactoe_app/match-play/{}/'.format(self.match.id), {"row":0,"column":0}, format='json')

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['non_field_errors'][0], "Can not move, the position is occupied")