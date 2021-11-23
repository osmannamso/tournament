from django.contrib.auth.models import User
from django.db import models


class Tournament(models.Model):
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.starts_at.strftime('%d %B, %H:%M:%S')


class Task(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task.title} {self.input}'


class TaskSubmission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.RESTRICT)
    code = models.TextField(default='')
    correct_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} at {self.created.strftime("%d %B, %H:%M:%S")} {self.task.title}'
