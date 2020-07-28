from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from uuslug import slugify
import datetime


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


class Users(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    patronymic = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    street = models.TextField(blank=True, null=True)
    house = models.TextField(blank=True, null=True)
    flat = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


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


class CategoryType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_type'

    def __str__(self):
        return self.name


class NeedType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование")
    category = models.ForeignKey(CategoryType, models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")

    class Meta:
        managed = False
        db_table = 'need_type'
        verbose_name = _("портебности")
        verbose_name_plural = _("Потребности")

    def __str__(self):
        return self.name


class Brands_model(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    sale = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'
        ordering = ['name']
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")


class Product(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name="Наименование")
    shot_description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    main_photo = models.ImageField(upload_to='uploads/product/', blank=True, null=True,
                                   verbose_name="Фото")
    artikul = models.TextField(blank=True, null=True, max_length=20, verbose_name="Артикул")
    note = models.TextField(blank=True, null=True, verbose_name="Примечание")
    components = models.TextField(blank=True, null=True, verbose_name="Состав")
    category = models.ForeignKey('CategoryType', models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    resource = models.ForeignKey('ResourceType', models.DO_NOTHING, blank=True, null=True, verbose_name="Средство")
    brand = models.ForeignKey('Brands_model', models.DO_NOTHING, blank=True, null=True)
    slug = models.TextField(blank=True, null=True, verbose_name="Ссылка")
    date = models.DateField(blank=True, null=True)
    artik_brand = models.TextField(blank=True, null=True, max_length=20)
    is_top = models.BooleanField(blank=True, null=True)
    hit_for_brand = models.BooleanField(blank=True, null=True)

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
        self.date = datetime.datetime.today()
        super(Product, self).save(*args, **kwargs)

        # self.note = self.note.replace('\n', '<br />')
        # self.description = self.description.replace('\n', '<br />')
        # self.components = self.components.replace('\n', '<br />')

    def __str__(self):
        return str(self.id) + ' ' + self.title

    def needed(self):
        prods = ProductNeed.objects.filter(product_id=self.id)
        return prods

    def get_sizes(self):
        sizes = ProductSize.objects.filter(product=self)
        return sizes

    def get_price(self):
        sizes = ProductSize.objects.filter(product=self).order_by('size__float_name', 'size__str_name')
        if sizes.count() > 0:
            sizes=sizes[0]
            return sizes
        else:
            return 0


class Size(models.Model):
    str_name = models.TextField(blank=True, null=True)
    float_name=models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'size'


class ProductSize(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    size = models.ForeignKey('Size', models.DO_NOTHING, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True, verbose_name="Стоимость", default=0)
    count = models.IntegerField(blank=True, null=True, verbose_name="Количество", default=0)
    sale = models.IntegerField(blank=True, null=True, verbose_name="Скидка", default=0)
    old_price = models.IntegerField(blank=True, null=True, verbose_name="Старая цена", default=0)

    class Meta:
        managed = False
        db_table = 'product_size'


class ProductNeed(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    need = models.ForeignKey(NeedType, models.DO_NOTHING, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'product_need'
        verbose_name = _("Потребности")
        verbose_name_plural = _("Потребности")



class ProductTone(models.Model):
    product_size = models.ForeignKey(ProductSize, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_tone'



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


class Files(models.Model):
    file = models.FileField(upload_to='excel', max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class Slider(models.Model):
    image = models.ImageField(upload_to='uploads', max_length=500, blank=True, null=True, verbose_name='Изображение')

    class Meta:
        managed = False
        db_table = 'slider'
        verbose_name = _("Слайд")
        verbose_name_plural = _("Слайдер")


class MainBlock(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Наименование')
    image = models.ImageField(upload_to='uploads', max_length=500, blank=True, null=True, verbose_name='Изображение')

    class Meta:
        managed = False
        db_table = 'main_block'
        verbose_name = _("Блок")
        verbose_name_plural = _("Блоки с картинками")




class Product_str(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name="Наименование")
    shot_description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    main_photo = models.TextField(blank=True, null=True,  verbose_name="Фото")
    artikul = models.TextField(blank=True, null=True, max_length=20, verbose_name="Артикул")
    note = models.TextField(blank=True, null=True, verbose_name="Примечание")
    components = models.TextField(blank=True, null=True, verbose_name="Состав")
    category = models.ForeignKey('CategoryType', models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    resource = models.ForeignKey('ResourceType', models.DO_NOTHING, blank=True, null=True, verbose_name="Средство")
    brand = models.ForeignKey('Brands_model', models.DO_NOTHING, blank=True, null=True)
    slug = models.TextField(blank=True, null=True, verbose_name="Ссылка")
    date = models.DateField(blank=True, null=True)
    artik_brand = models.TextField(blank=True, null=True, max_length=20)
    is_top = models.BooleanField(blank=True, null=True)
    hit_for_brand = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = _("товар")
        verbose_name_plural = _("Товары")

    def save(self, *args, **kwargs):
        if not self.id:
            super(Product_str, self).save(*args, **kwargs)
            string = str(self.id) + '-' + self.title
        else:
            string = str(self.id) + '-' + self.title
        self.slug = slugify(string)
        self.date = datetime.datetime.today()
        super(Product_str, self).save(*args, **kwargs)