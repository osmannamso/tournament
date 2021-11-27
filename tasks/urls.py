from django.urls import path

from tasks.views import TournamentsView, SingleTournamentView, TaskSubmissionView, TournamentTasksView

urlpatterns = [
    path('tournaments/', TournamentsView.as_view()),
    path('tournaments/<int:tournament_id>/', SingleTournamentView.as_view()),
    path('tournaments/<int:tournament_id>/tasks/', TournamentTasksView.as_view()),
    path('tasks/<int:task_id>/submit/', TaskSubmissionView.as_view())
]
