# Generated by Django 2.2.7 on 2020-07-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_authuser_brands_model_categorytype_files_mainblock_needtype_product_productneed_productsize_resource'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_str',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Наименование')),
                ('shot_description', models.TextField(blank=True, null=True, verbose_name='Краткое описание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('main_photo', models.TextField(blank=True, null=True, verbose_name='Фото')),
                ('artikul', models.TextField(blank=True, max_length=20, null=True, verbose_name='Артикул')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('components', models.TextField(blank=True, null=True, verbose_name='Состав')),
                ('slug', models.TextField(blank=True, null=True, verbose_name='Ссылка')),
                ('date', models.DateField(blank=True, null=True)),
                ('artik_brand', models.TextField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductTone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'product_tone',
                'managed': False,
            },
        ),
    ]
