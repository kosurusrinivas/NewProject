# Generated by Django 5.1 on 2024-10-14 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0035_itskills'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=100)),
                ('client', models.CharField(max_length=100)),
                ('project_type', models.CharField(choices=[('In progress', 'In progress'), ('Finished', 'Finished')], default='In progress', max_length=50)),
                ('year_of_working', models.CharField(max_length=50)),
                ('month_of_working', models.CharField(max_length=50)),
                ('details_of_project', models.CharField(max_length=1000)),
                ('project_location', models.CharField(max_length=100)),
                ('project_site_choices', models.CharField(choices=[('Offsite', 'Offsite'), ('Onsite', 'Onsite')], default='Offsite', max_length=50)),
                ('employment_type', models.CharField(choices=[('FULL_TIME', 'Full time'), ('PART_TIME', 'Part time'), ('CONTRACTUAL', 'Contractual')], default='FULL_TIME', max_length=50)),
                ('team_size', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=100)),
                ('role_decription', models.CharField(max_length=250)),
                ('skill_used', models.CharField(max_length=100)),
            ],
        ),
    ]
