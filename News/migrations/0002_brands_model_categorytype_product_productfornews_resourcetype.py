# Generated by Django 2.2.7 on 2020-01-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Брэнд',
                'verbose_name_plural': 'Брэнды',
                'db_table': 'brands',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'category_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Наименование')),
                ('shot_description', models.TextField(blank=True, null=True, verbose_name='Краткое описание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('main_photo', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Фото')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Стоимость')),
                ('artikul', models.IntegerField(blank=True, null=True, verbose_name='Артикул')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('components', models.TextField(blank=True, null=True, verbose_name='Состав')),
                ('size', models.IntegerField(blank=True, null=True, verbose_name='Объем')),
                ('slug', models.TextField(blank=True, null=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductForNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Продукт к новости',
                'verbose_name_plural': 'Продукты к новостям',
                'db_table': 'product_for_news',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'средства',
                'verbose_name_plural': 'Средства',
                'db_table': 'resource_type',
                'managed': False,
            },
        ),
    ]
