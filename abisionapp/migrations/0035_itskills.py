# Generated by Django 5.1 on 2024-10-12 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0034_alter_education_course_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Itskills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_software_name', models.CharField(max_length=100)),
                ('software_version', models.CharField(max_length=100)),
                ('last_used', models.CharField(max_length=100)),
                ('years_of_experiences', models.CharField(max_length=100)),
                ('months_of_experiences', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
