# Generated by Django 4.2 on 2024-07-12 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.CharField(max_length=200, unique=True)),
                ('permission', models.CharField(choices=[('ANONYMOUS', '비회원'), ('NORMAL', '일반 회원'), ('ADMIN', '관리자'), ('MASTER', '마스터')], default='NORMAL', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tb_auth_user',
            },
        ),
    ]
