# Generated by Django 4.2 on 2024-07-12 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100, unique=True, verbose_name='주문번호')),
                ('status', models.CharField(choices=[('PENDING', '주문 대기'), ('COMPLETED', '주문 완료'), ('CONFIRMED', '주문 확정'), ('CANCELLED', '주문 취소')], default='PENDING', max_length=10, verbose_name='주문 상태')),
                ('canceled_dtm', models.DateTimeField(null=True, verbose_name='주문 취소 일시')),
                ('confirmed_dtm', models.DateTimeField(null=True, verbose_name='주문 확정 일시')),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_auth.authuser')),
            ],
            options={
                'db_table': 'tb_order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveBigIntegerField(verbose_name='판매가')),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
            options={
                'db_table': 'tb_order_item',
            },
        ),
    ]