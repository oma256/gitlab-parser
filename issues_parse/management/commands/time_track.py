import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from issues_parse.models import WorkLog, Repository


class Command(BaseCommand):

    def handle(self, *args, **options):

        repositories = Repository.objects.all()

        for repository in repositories:
            url = f'https://gitlab.com/api/v4/projects/' \
                f'{repository.repository_id}/issues'
            headers = {'PRIVATE-TOKEN': settings.PRIVATE_GITLAB_TOKEN}
            params = {'state': 'opened'}

            r = requests.get(url, headers=headers, params=params)

            issue_list = []
            if r.status_code == requests.codes['ok']:
                for issue in r.json():
                    if issue['state'] == 'opened':
                        issue = {
                            'issue_id': issue.get('id'),
                            'title': issue.get('title'),
                            'description': issue.get('description'),
                            'author_name': issue.get('author').get('name'),
                            'assignee_name': issue.get('assignee').get('name'),
                            'state': issue.get('state'),
                            'updated_at': issue.get('updated_at'),
                            'due_date': issue.get('due_date'),
                            'project_id': issue.get('project_id'),
                            'web_url': issue.get('web_url'),
                            'time_spent': issue.get('time_stats').get(
                                'human_total_time_spent')
                        }
                        issue_list.append(issue)
                for issue in issue_list:
                    WorkLog.objects.create(**issue)
