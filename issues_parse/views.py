from django.shortcuts import render
from django.views.generic import ListView

from .models import Employee, WorkLog
from .utils import (
    convert_date_to_second, sum_working_hours
)


class UserListView(ListView):
    model = Employee

    def get(self, request, *args, **kwargs):
        users = self.model.objects.all()
        return render(request, 'issues_parse/index.html', {'users': users})


class WorkLogList(ListView):
    model = WorkLog

    def get(self, request, *args, **kwargs):
        work_logs = self.model.objects.filter(
            assignee_gitlab_name=kwargs.get('gitlab_username'))
        start_time, end_time = convert_date_to_second(request)
        total_time = sum_working_hours(work_logs, start_time, end_time)

        if not total_time:
            total_time = 'no working time'
            work_logs = []

        context = {
            'work_logs': work_logs,
            'total_time': total_time,
            'start_time': request.GET['start-time'],
            'end_time': request.GET['end-time'],
        }

        return render(request, 'issues_parse/work_log.html', context)
