import requests as lib_requests

from django.db.models import Prefetch
from django.forms import model_to_dict
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Tournament, Task, TaskSubmission
from tasks.serializers import TournamentSerializer, TaskSerializer, TaskSubmitSerializer


class TournamentsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        tournaments = Tournament.objects.all()

        return Response(TournamentSerializer(tournaments, many=True).data)


class SingleTournamentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, tournament_id, *args, **kwargs):
        tournament = Tournament.objects.get(pk=tournament_id)

        return Response(TournamentSerializer(tournament).data)


class TournamentTasksView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, tournament_id, *args, **kwargs):
        tasks = Task.objects.filter(tournament_id=tournament_id).prefetch_related(
            'testcase_set', Prefetch('tasksubmission_set', TaskSubmission.objects.filter(user=request.user))
        )

        return Response(TaskSerializer(tasks, many=True).data)


class TaskSubmissionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, task_id, *args, **kwargs):
        obj = TaskSubmitSerializer(data=request.data)
        obj.is_valid(raise_exception=True)
        data = obj.data
        task = Task.objects.get(pk=task_id)
        correct_count = 0
        test_cases = task.testcase_set.all()
        for test_case in test_cases:
            link = ''
            if data['language'] == TaskSubmission.JS:
                link = 'https://fight-js-compiler.herokuapp.com/compile/'
            elif data['language'] == TaskSubmission.PYTHON:
                link = 'https://fight-python-compiler.herokuapp.com/compile/'
            params = []
            inputs = test_case.input.replace('\r', '').split('\n')
            input_types = test_case.input_types.replace('\r', '').split('\n')
            for i in range(0, len(inputs)):
                params.append({
                    'value': inputs[i],
                    'type': input_types[i]
                })
            r = lib_requests.post(link, json={
                'code': data['code'],
                'type': test_case.return_type,
                'params': params
            })
            if str(r.json()['value']) == test_case.output:
                correct_count += 1
        task_submission = TaskSubmission(
            code=data['code'], language=data['language'], task_id=task_id, user=request.user,
            correct_count=correct_count
        )
        task_submission.save()
        res = model_to_dict(task_submission)
        res['accepted'] = correct_count == len(test_cases)

        return Response(res)
