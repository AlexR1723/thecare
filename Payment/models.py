from django.db import models
from django.utils.translation import ugettext_lazy as _


class Payment(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'payment'
        verbose_name = _("Оплата")
        verbose_name_plural = _("Оплаты")


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

