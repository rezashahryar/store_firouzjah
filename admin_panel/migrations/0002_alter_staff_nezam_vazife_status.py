# Generated by Django 4.2.13 on 2024-07-21 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='nezam_vazife_status',
            field=models.CharField(choices=[('mo', 'معاف'), ('et', 'اتمام خدمت')], max_length=3),
        ),
    ]
