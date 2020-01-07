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


class Feedback(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    email = models.CharField(max_length=200, blank=True, null=True, verbose_name='Email')
    subject = models.CharField(max_length=300, blank=True, null=True, verbose_name='Тема')
    text = models.TextField(blank=True, null=True, verbose_name='Текст')

    class Meta:
        managed = False
        db_table = 'feedback'
        verbose_name = _("Обратная связь")
        verbose_name_plural = _("Обратная связь")

