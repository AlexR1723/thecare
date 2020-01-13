# Generated by Django 2.2.7 on 2020-01-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'db_table': 'news',
                'managed': False,
            },
        ),
    ]
