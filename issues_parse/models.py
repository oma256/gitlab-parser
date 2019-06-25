import uuid

from django.db import models


class Repository(models.Model):
    repository_id = models.PositiveIntegerField('repository id')
    name = models.CharField('name', max_length=500)
    description = models.CharField('description', max_length=1000)

    class Meta:
        verbose_name = 'repository'
        verbose_name_plural = 'repositories'

    def __str__(self):
        return self.name


class Employee(models.Model):
    full_name = models.CharField('full name', max_length=100)
    gitlab_username = models.CharField('gitlab username', max_length=200)

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employee'

    def __str__(self):
        return self.gitlab_username


class WorkLog(models.Model):
    work_log_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)
    title = models.TextField('title')
    description = models.TextField('description')
    author_name = models.CharField('author name', max_length=100)
    assignee_name = models.CharField('assignee name', max_length=100)
    assignee_gitlab_name = models.CharField('assignee gitlab username',
                                            max_length=100)
    state = models.CharField('state', max_length=20)
    issue_id = models.PositiveIntegerField('issue_id')
    project_id = models.PositiveIntegerField('project_id')
    web_url = models.URLField('web url')
    due_date = models.DateTimeField('dua date')
    updated_at = models.DateTimeField('updated at')
    time_spend = models.CharField('time spent', max_length=50)
    time_estimate = models.CharField('time estimate', max_length=50)

    class Meta:
        verbose_name = 'work log'
        verbose_name_plural = 'work logs'

    def __str__(self):
        return self.title

