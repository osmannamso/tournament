from django.contrib import admin

from tasks.models import Tournament, Task, TestCase, TaskSubmission

admin.site.register(Tournament)
admin.site.register(Task)
admin.site.register(TestCase)
admin.site.register(TaskSubmission)
