# Generated by Django 4.0.5 on 2023-09-07 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0032_case_needername_alter_case_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_data_change',
            field=models.BooleanField(default=False),
        ),
    ]
