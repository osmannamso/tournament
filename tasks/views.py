from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Tournament, Task, TaskSubmission
from tasks.serializers import TournamentSerializer, TaskSerializer


class TournamentsView(APIView):
    def get(self, request, *args, **kwargs):
        tournaments = Tournament.objects.all()

        return Response(TournamentSerializer(tournaments, many=True).data)


class SingleTournamentView(APIView):
    def get(self, request, tournament_id, *args, **kwargs):
        tasks = Task.objects.filter(tournament_id=tournament_id).prefetch_related(
            'testcase_set', Prefetch('tasksubmission_set', TaskSubmission.objects.filter(user=request.user))
        )

        return Response(TaskSerializer(tasks, many=True).data)
