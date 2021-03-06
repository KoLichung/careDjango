# Generated by Django 4.0.5 on 2022-07-15 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0002_alter_chatroom_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='end_time',
            field=models.FloatField(blank=True, default=24, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='start_time',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_time',
            field=models.FloatField(blank=True, default=24, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='start_time',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userweekdaytime',
            name='end_time',
            field=models.FloatField(blank=True, default=24, null=True),
        ),
        migrations.AlterField(
            model_name='userweekdaytime',
            name='start_time',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
