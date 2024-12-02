# Generated by Django 5.1 on 2024-11-20 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abisionapp', '0053_qualification_ideal_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('linkedin_url', models.URLField()),
                ('website', models.URLField()),
                ('industry', models.CharField(max_length=255)),
                ('organization_size', models.CharField(max_length=50)),
                ('organization_type', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('tagline', models.TextField()),
            ],
        ),
    ]
