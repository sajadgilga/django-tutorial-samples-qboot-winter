from django.urls import path

from football.views import FetchTeamHomeFixtures, FetchTeamAwayFixtures, TeamNameView, TeamsView, TeamInfoView, \
    TeamCreateView, TeamCreateViewV2

urlpatterns = [
    path('home-games', FetchTeamHomeFixtures.as_view()),
    path('away-games', FetchTeamAwayFixtures.as_view(message='away teams retrieved')),
    path('see-team', TeamNameView.as_view()),
    path('team-list', TeamsView.as_view()),
    path('teams/<int:pk>', TeamInfoView.as_view()),
    path('teams/create/', TeamCreateView.as_view(), name='create_team'),
    path('teams/create/v2/', TeamCreateViewV2.as_view(), name='create_team_v2'),
]
