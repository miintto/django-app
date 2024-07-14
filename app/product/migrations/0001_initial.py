# Generated by Django 4.2.14 on 2024-07-14 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='상품명')),
                ('is_displayed', models.BooleanField(default=True, verbose_name='노출 여부')),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('updated_dtm', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tb_product',
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='품목명')),
                ('cost', models.PositiveBigIntegerField(verbose_name='원가')),
                ('price', models.PositiveBigIntegerField(verbose_name='판매가')),
                ('is_active', models.BooleanField(default=True)),
                ('sale_start_dtm', models.DateTimeField(null=True, verbose_name='판매 시작일')),
                ('sale_close_dtm', models.DateTimeField(null=True, verbose_name='판매 종료일')),
                ('item_quantity', models.PositiveIntegerField(verbose_name='재고')),
                ('sold_quantity', models.PositiveIntegerField(default=0, verbose_name='판매 수량')),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('updated_dtm', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'tb_product_item',
            },
        ),
    ]
