import datetime
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
    time_spend = models.PositiveIntegerField('time spent')
    time_estimate = models.PositiveIntegerField('time estimate')
    create_at = models.DateTimeField('create at', auto_now_add=True)

    class Meta:
        verbose_name = 'work log'
        verbose_name_plural = 'work logs'

    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    def display_time_estimate(self, granularity=2):
        result = []

        for name, count in self.intervals:
            value = self.time_estimate // count
            if value:
                self.time_estimate -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))

        return ', '.join(result[:granularity])

    def display_time_spend(self, granularity=2):
        result = []

        for name, count in self.intervals:
            value = self.time_spend // count
            if value:
                self.time_spend -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))

        return ', '.join(result[:granularity])

    @property
    def get_create_at(self):
        create_at = str(self.create_at)[:10]
        year, month, day = str(create_at).split('-')
        date = datetime.datetime(int(year), int(month), int(day))
        second = int(date.timestamp())

        return second

    @property
    def get_time_spend(self):
        return self.time_spend

    def __str__(self):
        return self.title

