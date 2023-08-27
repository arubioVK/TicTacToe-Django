from django.urls import path
from tictactoe_app.api.views import MatchCreateAPIView, MatchJoinAPIView, MatchDetailAPIView, MatchPlayAPIView, MatchesStatisticsAPIView


urlpatterns = [
    path('match-create/', MatchCreateAPIView.as_view(), name='match_create'),
    path('match-join/<int:pk>/', MatchJoinAPIView.as_view(), name='match_join'),
    path('match-detail/<int:pk>/', MatchDetailAPIView.as_view(), name='match_detail'),
    path('match-play/<int:pk>/', MatchPlayAPIView.as_view(), name='match_play'),
    path('matches-statistics/', MatchesStatisticsAPIView.as_view(), name='matches_statistics'),
]

