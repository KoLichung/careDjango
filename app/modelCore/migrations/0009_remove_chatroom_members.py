# Generated by Django 4.0.5 on 2022-07-20 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0008_chatroomusership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='members',
        ),
    ]
