# Generated by Django 2.2.7 on 2020-07-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_brands_model_categorytype_product_productfornews_resourcetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, default=0, null=True, verbose_name='Стоимость')),
                ('count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество')),
                ('sale', models.IntegerField(blank=True, default=0, null=True, verbose_name='Скидка')),
                ('old_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='Старая цена')),
            ],
            options={
                'db_table': 'product_size',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_name', models.TextField(blank=True, null=True)),
                ('float_name', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'size',
                'managed': False,
            },
        ),
    ]
