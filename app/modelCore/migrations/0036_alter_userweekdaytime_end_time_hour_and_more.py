# Generated by Django 4.0.5 on 2022-09-10 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0035_remove_userweekdaytime_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userweekdaytime',
            name='end_time_hour',
            field=models.IntegerField(blank=True, default=17, null=True),
        ),
        migrations.AlterField(
            model_name='userweekdaytime',
            name='start_time_hour',
            field=models.IntegerField(blank=True, default=8, null=True),
        ),
    ]
