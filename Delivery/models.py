from django.db import models

# Create your models here.

class Delivery(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name='Текст')

    class Meta:
        managed = False
        db_table = 'delivery'
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"
