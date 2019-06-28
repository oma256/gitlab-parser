import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from issues_parse.models import WorkLog, Repository


def create_work_log(response):
    """
    The parameter gets a list of all tasks, creates a new list of dictionaries,
    checks if 0 is contained in (time_estimate, time_spend, due_date)
    it will not create a record in the database if the record exists
    updates it if not then creates a record.
    :param response:
    :return: None
    """
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
            times = (issue.get('time_estimate'), issue.get('time_spend'),
                     issue.get('due_date'))
            if 0 in times:
                continue
            worklog = WorkLog.objects.filter(
                    issue_id=issue.get('issue_id')).update(**issue)
            if not worklog:
                WorkLog.objects.create(**issue)


def get_issues(repositories):
    """
    The parameter gets a list of all repositories that are in advance
    data base. A request is made to the GITLAB API to get issues.
    :param repositories:
    :return: dict
    """
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
        response = get_issues(self.repositories)
        create_work_log(response)
