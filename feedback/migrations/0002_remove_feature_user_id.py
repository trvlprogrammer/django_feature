# Generated by Django 3.2.9 on 2022-10-25 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='user_id',
        ),
    ]
