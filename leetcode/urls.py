from django.urls import path

from leetcode.views import TournamentView, MakeLeetSubmission

urlpatterns = [
    path('leet_tournaments/<int:id>/', TournamentView.as_view()),
    path('leet_submission/', MakeLeetSubmission.as_view())
]
