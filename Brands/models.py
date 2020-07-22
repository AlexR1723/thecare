from django.db import models
from django.utils.translation import ugettext_lazy as _


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


class Brands_model(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    sale = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")

    def save(self, *args, **kwargs):
        print(self.sale)
        products = ProductSize.objects.filter(product__brand__id=self.id)
        for p in products:
            price = p.price
            if p.old_price != None and p.old_price != '' and p.old_price != 0:
                price = p.old_price
            p.old_price = price
            p.sale = self.sale
            p.price = ((price * 100) / self.sale)
            p.save()
        super(Brands_model, self).save(*args, **kwargs)


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

    # price = models.IntegerField(blank=True, null=True, verbose_name="Стоимость")
    # sale = models.IntegerField(blank=True, null=True)
    # sale_is_number = models.BooleanField(blank=True, null=True)
    # count = models.IntegerField(blank=True, null=True)
    # sale_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = _("товар")
        verbose_name_plural = _("Товары")

    # def get_absolute_url(self):
    #     return reverse('Item_card', kwargs={'slug': self.slug})
    #
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super(Product, self).save(*args, **kwargs)
    #         string = str(self.id) + '-' + self.title
    #     else:
    #         string = str(self.id) + '-' + self.title
    #     self.slug = slugify(string)
    #     super(Product, self).save(*args, **kwargs)

    # self.note = self.note.replace('\n', '<br />')
    # self.description = self.description.replace('\n', '<br />')
    # self.components = self.components.replace('\n', '<br />')

    def __str__(self):
        return str(self.id) + ' ' + self.title

    # def needed(self):
    #     prods = ProductNeed.objects.filter(product_id=self.id)
    #     return prods
    #
    # def get_sizes(self):
    #     sizes = ProductSize.objects.filter(product=self)
    #     return sizes


class Size(models.Model):
    str_name = models.TextField(blank=True, null=True)
    float_name = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'size'


class ProductSize(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    size = models.ForeignKey('Size', models.DO_NOTHING, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True, verbose_name="Стоимость", default=0)
    count = models.IntegerField(blank=True, null=True, verbose_name="Количество", default=0)
    sale = models.IntegerField(blank=True, null=True, verbose_name="Скидка", default=0)
    old_price = models.IntegerField(blank=True, null=True, verbose_name="Старая цена", default=0)

    class Meta:
        managed = False
        db_table = 'product_size'


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
