from django.shortcuts import render
from django.views.generic import ListView

from .models import Employee, WorkLog
from .utils import convert_date_to_second, convert_second_to_datetime


class UserListView(ListView):
    model = Employee

    def get(self, request, *args, **kwargs):
        users = self.model.objects.all()
        return render(request, 'issues_parse/index.html', {'users': users})


class WorkLogList(ListView):
    model = WorkLog

    def get(self, request, *args, **kwargs):
        start_time, end_time = convert_date_to_second(request)
        sum_second = 0

        print(start_time, end_time)

        work_logs = self.model.objects.all().filter(
            assignee_gitlab_name=kwargs.get('gitlab_username'))
        for i in work_logs:
            if i.get_create_at in range(start_time, end_time):
                sum_second += i.get_time_spend

        total_time = convert_second_to_datetime(sum_second)
        print(total_time)
        context = {
            'work_logs': work_logs,
            'total_time': total_time,
            'start_time': request.GET['start-time'],
            'end_time': request.GET['end-time'],
        }
        return render(request, 'issues_parse/work_log.html', context)
