from django.db import models


class LeetTournament(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class LeetTask(models.Model):
    points = models.IntegerField()
    name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)
    tournament = models.ForeignKey(LeetTournament, on_delete=models.CASCADE)


class LeetUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, unique=True)


class LeetSubmission(models.Model):
    timestamp = models.IntegerField()
    task = models.ForeignKey(LeetTask, on_delete=models.CASCADE)
    user = models.ForeignKey(LeetUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('timestamp', 'task', 'user')
