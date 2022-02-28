from rest_framework.views import APIView
from rest_framework.response import Response

from leetcode.models import LeetTournament, LeetUser, LeetSubmission


class TournamentView(APIView):
    def get(self, request, id, *args, **kwargs):
        tournament = LeetTournament.objects.get(pk=id)
        tasks = []
        leet_tasks = tournament.leettask_set.all()
        for task in leet_tasks:
            tasks.append({
                'name': task.name,
                'points': task.points,
                'url': task.url,
                'id': task.id
            })
        users = []
        leet_users = LeetUser.objects.all()
        for leet_user in leet_users:
            user = {
                'username': leet_user.username,
                'url': leet_user.url,
                'id': leet_user.id
            }
            submissions = []
            for task in leet_tasks:
                submission = LeetSubmission.objects.filter(user=leet_user, task=task).order_by('timestamp').first()
                submissions.append({
                    'task': task.id,
                    'submission': {'timestamp': submission.timestamp} if submission else None
                })
            user['submissions'] = submissions
            users.append(user)

        return Response({
            'start': tournament.start,
            'end': tournament.end,
            'tasks': tasks,
            'users': users,
            'id': tournament.id
        })


class MakeLeetSubmission(APIView):
    def post(self, request):
        data = request.data
        try:
            submission = LeetSubmission(
                timestamp=data['timestamp'],
                task_id=data['task_id'],
                user_id=data['user_id']
            )
            submission.save()
            return Response({'status': 'ok'})
        except Exception as e:
            print(e)
            return Response(status=422)
