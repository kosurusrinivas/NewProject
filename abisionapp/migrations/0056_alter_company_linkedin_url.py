# Generated by Django 5.1 on 2024-11-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0055_company_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='linkedin_url',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
