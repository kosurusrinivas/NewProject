# Generated by Django 5.1 on 2024-08-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emailsignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=200)),
            ],
        ),
    ]
