# Generated by Django 4.0.5 on 2022-06-23 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0016_alter_recipient_user_alter_servant_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.category'),
        ),
    ]