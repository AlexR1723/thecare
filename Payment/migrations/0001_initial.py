# Generated by Django 2.2.7 on 2020-07-29 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Brands_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование')),
                ('sale', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'db_table': 'brands',
                'ordering': ['name'],
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
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, null=True, verbose_name='Текст')),
                ('is_main', models.BooleanField(blank=True, null=True, verbose_name='Основной?')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
                'db_table': 'contact',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование типа')),
            ],
            options={
                'verbose_name': 'Тип контакта',
                'verbose_name_plural': 'Типы контактов',
                'db_table': 'contact_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Оплата',
                'verbose_name_plural': 'Оплаты',
                'db_table': 'payment',
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
                ('main_photo', models.ImageField(blank=True, null=True, upload_to='uploads/product/', verbose_name='Фото')),
                ('artikul', models.TextField(blank=True, max_length=20, null=True, verbose_name='Артикул')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('components', models.TextField(blank=True, null=True, verbose_name='Состав')),
                ('slug', models.TextField(blank=True, null=True, verbose_name='Ссылка')),
                ('date', models.DateField(blank=True, null=True)),
                ('artik_brand', models.TextField(blank=True, max_length=20, null=True)),
                ('is_top', models.BooleanField(blank=True, null=True)),
                ('hit_for_brand', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'product',
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
