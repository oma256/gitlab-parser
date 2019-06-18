from pprint import pprint
import os
import requests
from django.core.management.base import BaseCommand

from issues_parse.models import Issue, Repository


env = os.environ

PRIVATE_GITLAB_TOKEN = env.get('PRIVATE_GITLAB_TOKEN', 'token')


class Command(BaseCommand):

    def handle(self, *args, **options):

        repositories = Repository.objects.all()

        for repository in repositories:
            url = f'https://gitlab.com/api/v4/projects/' \
                f'{repository.repository_id}/issues'
            headers = {'PRIVATE-TOKEN': PRIVATE_GITLAB_TOKEN}
            params = {'state': 'opened'}

            r = requests.get(url, headers=headers, params=params)

            issue_list = []
            if r.status_code == requests.codes['ok']:
                for i in r.json():
                    if i['state'] == 'opened':
                        issue = {
                            'issue_id': i.get('id'),
                            'title': i.get('title'),
                            'description': i.get('description'),
                            'author_name': i.get('author').get('name'),
                            'assignee_name': i.get('assignee').get('name'),
                            'state': i.get('state'),
                            'updated_at': i.get('updated_at'),
                            'due_date': i.get('due_date'),
                            'project_id': i.get('project_id'),
                            'web_url': i.get('web_url'),
                            'time_spent': i.get('time_stats').get(
                                'human_total_time_spent')
                        }
                        issue_list.append(issue)
            pprint(issue_list)

            for issue in issue_list:
                Issue.objects.create(**issue)
