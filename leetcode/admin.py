from django.contrib import admin

from leetcode.models import LeetTournament, LeetTask, LeetUser, LeetSubmission

admin.site.register(LeetTournament)
admin.site.register(LeetTask)
admin.site.register(LeetUser)
admin.site.register(LeetSubmission)
