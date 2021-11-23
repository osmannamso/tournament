from django.urls import path

from tasks.views import TournamentsView, SingleTournamentView

urlpatterns = [
    path('tournaments/', TournamentsView.as_view()),
    path('tournaments/<int:tournament_id>/', SingleTournamentView.as_view())
]
