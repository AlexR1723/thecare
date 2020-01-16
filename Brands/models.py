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
    name = models.CharField(max_length=200, blank=True, null=True,verbose_name='Наименование')
    image = models.ImageField(upload_to='uploads/',blank=True, null=True,verbose_name='Изображение')

    class Meta:
        managed = False
        db_table = 'brands'
        verbose_name = _("Брэнд")
        verbose_name_plural = _("Брэнды")

