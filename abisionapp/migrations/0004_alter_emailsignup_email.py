# Generated by Django 5.1 on 2024-08-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0003_alter_emailsignup_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsignup',
            name='Email',
            field=models.TextField(blank=True, verbose_name='Email Address'),
        ),
    ]
