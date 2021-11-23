from rest_framework import serializers


class TaskSubmissionSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    code = serializers.CharField()
    correct_count = serializers.IntegerField()


class TestCaseSerializer(serializers.Serializer):
    input = serializers.CharField()


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    testcase_set = TestCaseSerializer(many=True)
    tasksubmission_set = TaskSubmissionSerializer(many=True)


class TournamentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
    created = serializers.DateTimeField()
    tasks = TaskSerializer(many=True, required=False)
