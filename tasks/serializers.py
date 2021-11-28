from django.contrib.auth.models import User
from django.db.models import Count, F
from rest_framework import serializers


class TaskSubmissionSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    code = serializers.CharField()
    correct_count = serializers.IntegerField()


class TestCaseSerializer(serializers.Serializer):
    input = serializers.CharField()


class PureTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class TaskSerializer(PureTaskSerializer):
    testcase_set = TestCaseSerializer(many=True)
    tasksubmission_set = TaskSubmissionSerializer(many=True)


class TaskModelSerializer(PureTaskSerializer):
    acceptance_by_users = serializers.SerializerMethodField()

    def get_acceptance_by_users(self, obj):
        users = User.objects.all()
        res = []
        for user in users:
            res.append({
                'user': {
                    'username': user.username,
                    'id': user.id
                },
                'accepted': user.tasksubmission_set.annotate(overall=Count('task__testcase'))
                    .filter(task_id=obj.id, correct_count=F('overall')).exists()
            })

        return res


class TournamentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
    created = serializers.DateTimeField()
    task_set = TaskModelSerializer(many=True, required=False)


class TaskSubmitSerializer(serializers.Serializer):
    code = serializers.CharField()
    language = serializers.CharField()
