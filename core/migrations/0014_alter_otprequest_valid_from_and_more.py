# Generated by Django 4.2.13 on 2024-07-19 15:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_otprequest_valid_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='valid_from',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 19, 15, 4, 47, 342571, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='otprequest',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 19, 15, 7, 47, 342571, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
