# Generated by Django 4.0.5 on 2023-03-20 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0029_order_is_sent_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='conditions_remark',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='disease_remark',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]