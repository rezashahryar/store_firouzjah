# Generated by Django 4.2.13 on 2024-07-19 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_productlist_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategoryproduct',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='store.categoryproduct'),
        ),
    ]
