from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from uuslug import slugify


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
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        managed = False
        db_table = 'brands'
        ordering=['name']
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")


class Product(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name="Наименование")
    shot_description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    main_photo = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Фото")
    price = models.IntegerField(blank=True, null=True, verbose_name="Стоимость")
    artikul = models.IntegerField(blank=True, null=True, verbose_name="Артикул")
    note = models.TextField(blank=True, null=True, verbose_name="Примечание")
    components = models.TextField(blank=True, null=True, verbose_name="Состав")
    category = models.ForeignKey('CategoryType', models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    resource = models.ForeignKey('ResourceType', models.DO_NOTHING, blank=True, null=True, verbose_name="Средство")
    brand = models.ForeignKey('Brands_model', models.DO_NOTHING, blank=True, null=True)
    slug = models.TextField(blank=True, null=True, verbose_name="Ссылка")
    sale = models.IntegerField(blank=True, null=True)
    sale_is_number = models.BooleanField(blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)

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

        # self.note = self.note.replace('\n', '<br />')
        # self.description = self.description.replace('\n', '<br />')
        # self.components = self.components.replace('\n', '<br />')

    def __str__(self):
        return str(self.id) + ' ' + self.title

    def needed(self):
        prods=ProductNeed.objects.filter(product_id=self.id)
        return prods


class Size(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'size'


class ProductSize(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    size = models.ForeignKey('Size', models.DO_NOTHING, blank=True, null=True)

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
