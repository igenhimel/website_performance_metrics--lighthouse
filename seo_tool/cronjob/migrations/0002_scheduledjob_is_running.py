# Generated by Django 4.2.5 on 2023-09-26 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronjob', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledjob',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
    ]