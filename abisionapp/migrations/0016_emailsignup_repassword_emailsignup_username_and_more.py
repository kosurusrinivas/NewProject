# Generated by Django 5.1 on 2024-09-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0015_rename_signupfinish_profile_signupfinish'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsignup',
            name='Repassword',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='emailsignup',
            name='Username',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='emailsignup',
            name='password',
            field=models.CharField(default='', max_length=50),
        ),
    ]
