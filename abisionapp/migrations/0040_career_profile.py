# Generated by Django 5.1 on 2024-10-18 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0039_profile_summary'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Career_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Current_industry', models.CharField(max_length=100)),
                ('Department', models.CharField(max_length=100)),
                ('Role_category', models.CharField(max_length=100)),
                ('Job_role', models.CharField(max_length=100)),
                ('job_type_project', models.CharField(choices=[('permanent', 'permanent'), ('contractual', 'contractual')], default='permanent', max_length=50)),
                ('employment_type_career', models.CharField(choices=[('fullTime', 'fullTime'), ('partTime', 'partTime')], default='fullTime', max_length=50)),
                ('shift_type_project', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night'), ('Flexible', 'Flexible')], default='Day', max_length=50)),
                ('location', models.CharField(max_length=1000)),
                ('salary', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
