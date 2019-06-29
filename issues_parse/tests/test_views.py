from datetime import datetime

from django.shortcuts import reverse
from django.test import TestCase

from issues_parse.models import WorkLog


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
                                  'end-time': '2019-06-30'})
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