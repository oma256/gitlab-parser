# Generated by Django 2.2.2 on 2019-06-27 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues_parse', '0002_auto_20190626_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='dua date'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated at'),
        ),
    ]
