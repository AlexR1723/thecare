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
    date = models.DateTimeField(default=timezone.now,blank=True, null=True, verbose_name='Дата публикации')
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
        self.text=self.text.replace('\n','<br />')


