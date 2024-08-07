# Generated by Django 4.2.13 on 2024-07-19 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_farsi', models.CharField(max_length=255)),
                ('title_english', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('product_list_code', models.CharField(default=store.models.random_code_product, max_length=4, unique=True)),
                ('product_model', models.CharField(max_length=255)),
                ('status_originaly', models.CharField(choices=[('o', 'اصل ، اوریجینال')], max_length=10)),
                ('product_warranty', models.BooleanField()),
                ('sending_method', models.CharField(choices=[('pish', 'پیشتاز'), ('tip', 'تیپاکس'), ('bar', 'باربری'), ('peyk', 'پیک موتوری')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='category_images/%Y/%m/%d/')),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code_of_color', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mantaghe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('p', 'Paid'), ('u', 'Unpaid'), ('c', 'Canceled')], default='u', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='store.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory', models.PositiveIntegerField()),
                ('unit', models.CharField(choices=[('p', 'جفت'), ('n', 'عددی')], max_length=3)),
                ('product_code', models.CharField(default=store.models.random_code_product, max_length=4, unique=True)),
                ('slug', models.SlugField()),
                ('price', models.IntegerField()),
                ('price_after_discount', models.IntegerField()),
                ('discount_percent', models.PositiveIntegerField()),
                ('start_discount_datetime', models.DateTimeField()),
                ('end_discount_datetime', models.DateTimeField()),
                ('length_package', models.IntegerField()),
                ('width_package', models.IntegerField()),
                ('height_package', models.IntegerField()),
                ('weight_package', models.IntegerField()),
                ('shenase_kala', models.CharField(max_length=14)),
                ('barcode', models.CharField(max_length=16)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.baseproduct')),
            ],
        ),
        migrations.CreateModel(
            name='ProductProperties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.CharField(max_length=11)),
                ('phone_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(default=store.models.random_code_store, max_length=6, unique=True)),
                ('shomare_shaba', models.CharField(max_length=26)),
                ('mahalle', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=555)),
                ('post_code', models.CharField(max_length=10)),
                ('parvane_kasb', models.FileField(upload_to='parvane_kasb__/%Y/%m/%d/')),
                ('tasvire_personely', models.ImageField(upload_to='tasvire_personely__/%Y/%m/%d/')),
                ('kart_melli', models.ImageField(upload_to='kart_melli__/%Y/%m/%d/')),
                ('shenasname', models.ImageField(upload_to='tasvire_shenasname__/%Y/%m/%d/')),
                ('logo', models.ImageField(upload_to='logo__/%Y/%m/%d/')),
                ('roozname_rasmi_alamat', models.FileField(upload_to='roozname_rasmi_alamat__/%Y/%m/%d/')),
                ('gharardad', models.FileField(upload_to='gharardad__/%Y/%m/%d/')),
                ('store_type', models.CharField(choices=[('ha', 'حقیقی'), ('ho', 'حقوقی')], max_length=2)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.city')),
                ('mantaghe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.mantaghe')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.province')),
            ],
        ),
        migrations.CreateModel(
            name='HaghighyStore',
            fields=[
                ('store_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.store')),
                ('full_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('name_father', models.CharField(max_length=255)),
                ('code_melli', models.CharField(max_length=10, unique=True)),
                ('shomare_shenasname', models.CharField(max_length=255)),
            ],
            bases=('store.store',),
        ),
        migrations.CreateModel(
            name='HoghoughyStore',
            fields=[
                ('store_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.store')),
                ('ceo_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('date_of_registration', models.DateField()),
                ('num_of_registration', models.CharField(max_length=255)),
                ('economic_code', models.CharField(max_length=255)),
            ],
            bases=('store.store',),
        ),
        migrations.CreateModel(
            name='SubCategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='store.categoryproduct')),
            ],
        ),
        migrations.CreateModel(
            name='SetProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='store.product')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productproperties')),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_type', to='store.categoryproduct')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_type', to='store.subcategoryproduct')),
            ],
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_lists', to='store.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_list', to='store.store')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/%Y/%m/%d/')),
                ('is_cover', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.baseproduct')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.size'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.categoryproduct'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.store'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.subcategoryproduct'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.product')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.product')),
            ],
            options={
                'unique_together': {('cart', 'product')},
            },
        ),
    ]
