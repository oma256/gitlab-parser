# Generated by Django 2.2.2 on 2019-06-26 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues_parse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create at'),
        ),
    ]
