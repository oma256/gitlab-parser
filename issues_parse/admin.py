from django.contrib import admin

from .models import WorkLog, Repository, Employee


class IssueAdmin(admin.ModelAdmin):
    list_display = ('work_log_id', 'title', 'description', 'author_name',
                    'assignee_name', 'assignee_gitlab_name', 'issue_id',
                    'project_id', 'state', 'time_spend', 'time_estimate',
                    'updated_at', 'due_date', 'web_url')


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('repository_id', 'name', 'description')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gitlab_username')


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(WorkLog, IssueAdmin)
admin.site.register(Employee, EmployeeAdmin)
