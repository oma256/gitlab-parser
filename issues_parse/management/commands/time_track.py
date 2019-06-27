import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from issues_parse.models import WorkLog, Repository


def create_work_log(response):
    if response.status_code == requests.codes['ok']:
        issue_list = []
        for issue in response.json():
            if issue['state'] == 'opened':
                issue = {
                    'issue_id': issue.get('id'),
                    'title': issue.get('title'),
                    'description': issue.get('description'),
                    'author_name': issue.get('author').get('name'),
                    'assignee_name': issue.get('assignee').get('name'),
                    'assignee_gitlab_name': issue.get('assignee').get(
                        'username'),
                    'state': issue.get('state'),
                    'time_estimate': issue.get('time_stats').get(
                        'time_estimate'),
                    'time_spend': issue.get('time_stats').get(
                        'total_time_spent'),
                    'updated_at': issue.get('updated_at'),
                    'due_date': issue.get('due_date'),
                    'project_id': issue.get('project_id'),
                    'web_url': issue.get('web_url'),
                }
                issue_list.append(issue)
        for issue in issue_list:
            WorkLog.objects.update_or_create(**issue)


def get_issues(repositories):
    for repository in repositories:
        url = f'https://gitlab.com/api/v4/projects/' \
            f'{repository.repository_id}/issues'
        headers = {'PRIVATE-TOKEN': settings.PRIVATE_GITLAB_TOKEN}
        params = {'state': 'opened'}

        r = requests.get(url, headers=headers, params=params)
        return r


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.repositories = Repository.objects.all()

    def handle(self, *args, **options):
        r = get_issues(self.repositories)
        create_work_log(r)
