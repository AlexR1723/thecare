# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


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


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Brands(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class CategoryType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_type'


class Contact(models.Model):
    contact = models.ForeignKey('ContactType', models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    is_main = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class ContactType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_type'


class Delivery(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Feedback(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=300, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'


class Files(models.Model):
    file = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class MainBlock(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_block'


class NeedType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(CategoryType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'need_type'


class News(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    slug = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Payment(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment'


class Product(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name="Наименование")
    shot_description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    main_photo = models.ImageField(upload_to='uploads/product/', blank=True, null=True,
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


class ProductForNews(models.Model):
    news = models.ForeignKey(News, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_for_news'


class ProductNeed(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    need = models.ForeignKey(NeedType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_need'


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


class ProductTone(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_tone'


class ResourceType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(CategoryType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resource_type'


class Size(models.Model):
    str_name = models.TextField(blank=True, null=True)
    float_name = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'size'


class Slider(models.Model):
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'slider'


class Users(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
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
