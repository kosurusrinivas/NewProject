# Generated by Django 5.1 on 2024-09-25 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0021_resume_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='name',
        ),
    ]
