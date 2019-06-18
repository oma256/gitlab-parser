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


class Issue(models.Model):
    issue_id = models.PositiveIntegerField('issue id', unique=True)
    title = models.TextField('title')
    description = models.TextField('description')
    author_name = models.CharField('author name', max_length=100)
    assignee_name = models.CharField('assignee name', max_length=100)
    state = models.CharField('state', max_length=20)
    updated_at = models.DateTimeField('updated at')
    project_id = models.PositiveIntegerField('project_id')
    web_url = models.URLField('web url')
    due_date = models.DateTimeField('dua date')
    time_spent = models.CharField('time spent', max_length=50)

    class Meta:
        verbose_name = 'issue',
        verbose_name_plural = 'issues'

    def __str__(self):
        return self.title

