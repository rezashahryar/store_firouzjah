# Generated by Django 4.2.13 on 2024-07-23 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_dateorder_time_dateorder_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_time_order',
            new_name='date_order',
        ),
        migrations.AddField(
            model_name='order',
            name='time_order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.timeorder'),
            preserve_default=False,
        ),
    ]
