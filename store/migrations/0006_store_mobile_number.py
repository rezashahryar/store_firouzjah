# Generated by Django 4.2.13 on 2024-07-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_sending_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='mobile_number',
            field=models.CharField(default=1, max_length=11),
            preserve_default=False,
        ),
    ]