from django.shortcuts import render
from django.views.generic import ListView

from .models import Employee, WorkLog


class UserListView(ListView):
    model = Employee

    def get(self, request, *args, **kwargs):
        users = Employee.objects.all()
        return render(request, 'issues_parse/index.html', {'users': users})


class TimeTrackList(ListView):

    def get(self, request, gitlab_username, *args, **kwargs):
        work_logs = WorkLog.objects.all().filter(
                                        assignee_gitlab_name=gitlab_username)
        return render(request, 'issues_parse/work_log.html',
                                                    {'work_logs': work_logs})

