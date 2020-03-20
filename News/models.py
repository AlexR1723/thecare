from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from uuslug import slugify
from django.utils import timezone
import datetime


# Create your models here.
class ContactType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Наименование типа')

    class Meta:
        managed = False
        db_table = 'contact_type'
        verbose_name = _("Тип контакта")
        verbose_name_plural = _("Типы контактов")


class Contact(models.Model):
    contact = models.ForeignKey('ContactType', models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name='Текст')
    is_main = models.BooleanField(blank=True, null=True, verbose_name='Основной?')

    class Meta:
        managed = False
        db_table = 'contact'
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")


class News_model(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Заголовок')
    text = models.TextField(blank=True, null=True, verbose_name='Текст')
    date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name='Изображение')
    slug = models.TextField(blank=True, null=True, verbose_name="Ссылка")

    class Meta:
        managed = False
        db_table = 'news'
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")

    def get_absolute_url(self):
        return reverse('News_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            super(News_model, self).save(*args, **kwargs)
            string = str(self.id) + '-' + self.name
        else:
            string = str(self.id) + '-' + self.name
        self.slug = slugify(string)
        super(News_model, self).save(*args, **kwargs)
        self.text = self.text.replace('\n', '<br />')

    def __str__(self):
        return str(self.id) + ' ' + self.name


class Brands_model(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        managed = False
        db_table = 'brands'
        verbose_name = _("Брэнд")
        verbose_name_plural = _("Брэнды")


class CategoryType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_type'

    def __str__(self):
        return self.name


class ResourceType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование")
    category = models.ForeignKey(CategoryType, models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")

    class Meta:
        managed = False
        db_table = 'resource_type'
        verbose_name = _("средства")
        verbose_name_plural = _("Средства")

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name="Наименование")
    shot_description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    main_photo = models.ImageField(upload_to='uploads/product/', max_length=500, blank=True, null=True,
                                   verbose_name="Фото")
    artikul = models.IntegerField(blank=True, null=True, verbose_name="Артикул")
    note = models.TextField(blank=True, null=True, verbose_name="Примечание")
    components = models.TextField(blank=True, null=True, verbose_name="Состав")
    category = models.ForeignKey('CategoryType', models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    resource = models.ForeignKey('ResourceType', models.DO_NOTHING, blank=True, null=True, verbose_name="Средство")
    brand = models.ForeignKey('Brands_model', models.DO_NOTHING, blank=True, null=True)
    slug = models.TextField(blank=True, null=True, verbose_name="Ссылка")
    date = models.DateField(blank=True, null=True)
    artik_brand = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = _("товар")
        verbose_name_plural = _("Товары")

    def get_absolute_url(self):
        return reverse('Item_card', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            super(Product, self).save(*args, **kwargs)
            string = str(self.id) + '-' + self.title
        else:
            string = str(self.id) + '-' + self.title
        self.slug = slugify(string)
        super(Product, self).save(*args, **kwargs)
        # self.text = self.text.replace('\n', '<br />')

    def __str__(self):
        return str(self.id) + ' ' + self.title


class ProductForNews(models.Model):
    news = models.ForeignKey('News_model', models.DO_NOTHING, blank=True, null=True, verbose_name='Новость')
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True, verbose_name='Продукт')

    class Meta:
        managed = False
        db_table = 'product_for_news'
        verbose_name = _("Продукт к новости")
        verbose_name_plural = _("Продукты к новостям")


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
