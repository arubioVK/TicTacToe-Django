from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from tictactoe_app.models import Match
from tictactoe_app.api.serializers import MatchCreateSerializer, MatchJoinSerializer, MatchDetailSerializer, MatchPlaySerializer

 
class MatchCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = MatchCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchJoinAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        match = Match.objects.get(id=pk)
        serializer = MatchJoinSerializer(match, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        try:
            match = Match.objects.get(id=pk)
        except Match.DoesNotExist:
            return Response({'Error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MatchDetailSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MatchPlayAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk, format=None):
        match = Match.objects.get(id=pk)
        serializer = MatchPlaySerializer(match, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchesStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        matches = Match.objects.filter(Q(player1=request.user)|Q(player2=request.user))
        matches_finish = matches.filter(finish=True)
        list_matches_finish = list(matches_finish.values_list('id', flat=True))
        matches_unfinish = matches.filter(finish=False)
        list_matches_unfinish = list(matches_unfinish.values_list('id', flat=True))
        wins = matches_finish.filter(winner=request.user)
        draws = matches_finish.filter(winner__isnull=True)
        loses = matches_finish.exclude(winner=request.user).exclude(winner__isnull=True)
        return Response({'wins': wins.count(), 'draws':draws.count(), 'loses':loses.count(),'total_matches_finish':matches_finish.count(),'list_matches_finish': list_matches_finish, 'total_matches_unfinish':matches_unfinish.count(),'list_matches_unfinish': list_matches_unfinish,}, status=status.HTTP_200_OK)

