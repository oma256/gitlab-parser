from datetime import datetime

import requests
import responses
from django.shortcuts import reverse
from django.test import TestCase

from issues_parse.management.commands.gitlab_issues_parse import (
    get_issues, create_work_log
)
from issues_parse.models import WorkLog, Repository


class UserListViewTest(TestCase):

    def test_user_list(self):
        url = reverse('issues_parse:index')

        r = self.client.get(url)

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Issues parse')
        self.assertContains(r, 'gitlab username')
        self.assertContains(r, 'full name')


class WorkLogListViewTest(TestCase):

    def setUp(self):
        self.worklog = WorkLog.objects.create(
            title='title',
            description='description',
            author_name='Omurbek Dulatov',
            assignee_name='Omurbek Dulatov',
            assignee_gitlab_name='oma256',
            state='opened',
            issue_id=22157728,
            project_id=10466882,
            web_url='https://gitlab.example.com/eileen.lowe',
            due_date=None,
            updated_at=None,
            time_spend='10800',
            time_estimate='21600',
            create_at=datetime.now()
        )

    def tearDown(self):
        WorkLog.objects.all().delete()

    def test_worklog_list(self):
        url = reverse('issues_parse:get_time_track', kwargs={
            'gitlab_username': 'oma256'})

        r = self.client.get(url, {'start-time': '2019-06-24',
                                  'end-time': '2019-06-29'})

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '3 hours')
        self.assertContains(r, self.worklog.assignee_name)
        self.assertContains(r, self.worklog.title)
        self.assertContains(r, self.worklog.description)

    def test_not_total_time(self):
        url = reverse('issues_parse:get_time_track', kwargs={
            'gitlab_username': 'oma256'})

        r = self.client.get(url, {'start-time': '2019-06-20',
                                  'end-time': '2019-06-23'})

        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'no working time')


class TestGitlabAPIParse(TestCase):

    def setUp(self):
        self.repository = Repository.objects.create(
            repository_id=10466882,
            name='django rest framework',
            description='description'
        )

        self.worklog = WorkLog.objects.create(
            title='title',
            description='description',
            author_name='Omurbek Dulatov',
            assignee_name='Omurbek Dulatov',
            assignee_gitlab_name='oma256',
            state='opened',
            issue_id=22157728,
            project_id=10466882,
            web_url='https://gitlab.example.com/eileen.lowe',
            due_date=None,
            updated_at=None,
            time_spend=0,
            time_estimate=0,
            create_at=datetime.now()
        )

    @responses.activate
    def test_get_issues(self):
        url = f'https://gitlab.com/api/v4/' \
            f'projects/{self.repository.repository_id}/issues?state=opened'
        json_data = {
            'id': 22332038,
            'title': 'tests view',
            'description': 'description',
            'author_name': 'Omurbek Dulatov',
            'assignee_name': 'Omurbek Dulatov',
            'assignee_username': 'oma256',
            'state': 'opened',
            'time_estimate': 14400,
            'total_time_spend': 10800,
            'updated_at': '2019-06-27T20:48:37.572Z',
            'due_date': '2019-06-29',
            'project_id': 10466882,
            'web_url': 'https://gitlab.com/oma256/django_rest_framework/issues/2',
        }
        responses.add(responses.GET, url,
                      json=json_data,
                      headers={'PRIVATE-TOKEN': 'private-token'},
                      status=200,
                      content_type='application/json'
                      )

        resp = get_issues([self.repository])

        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, json_data)

    @responses.activate
    def test_create_work_log(self):
        url = f'https://gitlab.com/api/v4/' \
            f'projects/{self.repository.repository_id}/issues?state=opened'
        json_data = [
            {
                'id': 1233432,
                'title': 'test to admin',
                'description': 'test description',
                'author': {'name': 'Gatiev Stepan'},
                'assignee': {'name': 'Omurbek Dulatov', 'username': 'oma256'},
                'state': 'opened',
                'time_stats': {
                    'time_estimate': 14400,
                    'total_time_spent': 10800
                },
                'updated_at': '2019-06-27T20:48:37.572Z',
                'due_date': '2019-06-29T20:48:37.572Z',
                'project_id': 10466885,
                'web_url': 'https://gitlab.com/oma256/django_rest_framework/issues/7',
            }
        ]
        responses.add(responses.GET, url,
                      json=json_data,
                      headers={'PRIVATE-TOKEN': 'private-token'},
                      status=200,
                      content_type='application/json'
                      )

        resp = requests.get(url)

        create_work_log(resp)
        worklog = WorkLog.objects.get(issue_id=1233432)

        self.assertEqual(worklog.issue_id, 1233432)
        self.assertEqual(worklog.title, 'test to admin')
        self.assertEqual(worklog.description, 'test description')
        self.assertEqual(worklog.author_name, 'Gatiev Stepan')
        self.assertEqual(worklog.assignee_name, 'Omurbek Dulatov')
        self.assertEqual(worklog.assignee_gitlab_name, 'oma256')
        self.assertEqual(worklog.state, 'opened')
        self.assertEqual(worklog.time_estimate, 14400)
        self.assertEqual(
            worklog.due_date.strftime(
                '%Y-%m-%d %H:%M:%S'), '2019-06-29 20:48:37')
        self.assertEqual(worklog.time_spend, 10800)
        self.assertEqual(worklog.project_id, 10466885)
        self.assertEqual(worklog.web_url, 'https://gitlab.com/oma256/django_rest_framework/issues/7')

    # @responses.activate
    # def test_create_work_log_not_time_estimate_or_not_time_spend(self):
    #     url = f'https://gitlab.com/api/v4/' \
    #         f'projects/{self.repository.repository_id}/issues?state=opened'
    #     json_data = [
    #         {
    #             'id': 4234534,
    #             'title': 'test to admin',
    #             'description': 'test description',
    #             'author': {'name': 'Gatiev Stepan'},
    #             'assignee': {'name': 'Omurbek Dulatov',
    #                          'username': 'oma256'},
    #             'state': 'opened',
    #             'time_stats': {
    #                 'time_estimate': 0,
    #                 'total_time_spent': 0
    #             },
    #             'updated_at': '2019-06-27T20:48:37.572Z',
    #             'due_date': None,
    #             'project_id': 10466885,
    #             'web_url': 'https://gitlab.com/oma256/django_rest_framework/issues/7',
    #         }
    #     ]
    #     responses.add(responses.GET, url,
    #                   json=json_data,
    #                   headers={'PRIVATE-TOKEN': 'private-token'},
    #                   status=200,
    #                   content_type='application/json'
    #                   )
    #
    #     resp = requests.get(url)
    #
    #     create_work_log(resp)
    #     worklog = WorkLog.objects.get(issue_id=4234534)
    #
    #     self.assertEqual(worklog.issue_id, 4234534)
    #     self.assertEqual(worklog.title, 'test to admin')
    #     self.assertEqual(worklog.description, 'test description')
    #     self.assertEqual(worklog.author_name, 'Gatiev Stepan')
    #     self.assertEqual(worklog.assignee_name, 'Omurbek Dulatov')
    #     self.assertEqual(worklog.assignee_gitlab_name, 'oma256')
    #     self.assertEqual(worklog.state, 'opened')
    #     self.assertEqual(worklog.time_estimate, 0)
    #     self.assertEqual(worklog.due_date, None)
    #     self.assertEqual(worklog.time_spend, 0)
    #     self.assertEqual(worklog.project_id, 10466885)
    #     self.assertEqual(worklog.web_url,
    #                      'https://gitlab.com/oma256/django_rest_framework/issues/7')





