# Generated by Django 4.0.5 on 2022-07-19 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0007_rename_atminfobankinstitutioncode_user_atminfobranchbankcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatroomUserShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
