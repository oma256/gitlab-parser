from django.contrib import admin

from .models import WorkLog, Repository


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author_name',
                    'assignee_name', 'issue_id', 'project_id', 'state',
                    'time_spent', 'updated_at', 'due_date', 'web_url')


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('repository_id', 'name', 'description')


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(WorkLog, IssueAdmin)
