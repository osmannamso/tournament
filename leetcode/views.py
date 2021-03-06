from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateformat import format

from leetcode.models import LeetTournament, LeetUser, LeetSubmission, LeetTask


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
            points = 0
            last_submission = -1
            submissions = []
            for task in leet_tasks:
                submission = LeetSubmission.objects.filter(user=leet_user, task=task).order_by('timestamp').first()
                submissions.append({
                    'task': task.id,
                    'submission': {'timestamp': submission.timestamp} if submission else None
                })
                if submission:
                    points += task.points
                    last_submission = max(last_submission, submission.timestamp)
            user['submissions'] = submissions
            user['points'] = points
            user['last_submission'] = last_submission
            users.append(user)
        users.sort(reverse=True, key=lambda x: (x['points'], 9999999999 - x['last_submission']))
        just_users = []
        for user in users:
            just_users.append(user['username'])

        return Response({
            'just_users': just_users,
            'start': tournament.start,
            'end': tournament.end,
            'tasks': tasks,
            'users': users,
            'id': tournament.id
        })


class MakeLeetSubmission(APIView):
    def post(self, request, id, username):
        tournament = LeetTournament.objects.get(pk=id)
        start = format(tournament.start, 'U')
        end = format(tournament.end, 'U')
        user = LeetUser.objects.get(username=username)
        data = request.data
        try:
            submissions = data['data']['recentSubmissionList']
            for submission in submissions:
                if submission['statusDisplay'] != 'Accepted':
                    continue
                task = LeetTask.objects.filter(name=submission['title'], tournament=tournament).first()
                if not task:
                    continue
                timestamp = int(submission['timestamp'])
                if timestamp < start or timestamp > end:
                    continue
                submission = LeetSubmission(timestamp=timestamp, task=task, user=user)
                submission.save()
            return Response({'status': 'ok'})
        except Exception as e:
            print(e)
            return Response(status=422)
