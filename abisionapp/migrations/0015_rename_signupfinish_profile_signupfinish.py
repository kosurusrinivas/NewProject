# Generated by Django 5.1 on 2024-09-23 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0014_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='SignupFinish',
            new_name='signupFinish',
        ),
    ]
