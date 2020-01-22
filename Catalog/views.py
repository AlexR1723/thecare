from django.shortcuts import render
from .models import *
from uuslug import slugify
from django.db.models import Q


def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
    return number, email


def Items_catalog(request):
    number, email = func_contact()

    return render(request, 'Catalog/Items_catalog.html', locals())


def Face(request):
    number, email = func_contact()

    head = 'Средства для лица'
    product = Product.objects.all()
    resource = ResourceType.objects.filter(category__name='Для лица')
    need = NeedType.objects.filter(category__name='Для лица')
    return render(request, 'Catalog/Items_catalog.html', locals())


def For_men(request):
    number, email = func_contact()

    head = 'Для мужчин'
    product = Product.objects.all()
    # resource=ResourceType.objects.filter(category__name='Для мужчин')
    # need=NeedType.objects.filter(category__name='Для мужчин')
    # brands=Brands_model.objects.all()

    resource = ResourceType.objects.filter(category__name='Для лица')
    need = NeedType.objects.filter(category__name='Для лица')
    brands = Brands_model.objects.all()
    url_page = 'for_men'

    return render(request, 'Catalog/Items_catalog.html', locals())


def For_men_s(request, text):
    number, email = func_contact()

    head='Для мужчин'
    # product=Product.objects.all()
    # resource = ResourceType.objects.filter(category__name='Для мужчин')
    # need = NeedType.objects.filter(category__name='Для мужчин')
    resource = ResourceType.objects.filter(category__name='Для лица')
    need = NeedType.objects.filter(category__name='Для лица')
    brands = Brands_model.objects.all()
    url_page = 'for_men'

    # print('for men s good')
    # print(text)

    text = str(text)
    arr = text.split('%')

    prices = ''
    resources = ''
    needs = ''
    brand = ''
    for i in arr:
        st = i.split('=')
        if st[0] == 'price':
            prices = st[1].split('&')
        if st[0] == 'resources':
            resources = st[1].split('&')
        if st[0] == 'needs':
            needs = st[1].split('&')
        if st[0] == 'brands':
            brand = st[1].split('&')

    resources_id = []
    needs_id = []
    brands_id = []

    if needs:
        q_needs = Q()
        for item in needs:
            try:
                item = int(item)
                q_needs.add(Q(need_id=item), Q.OR)
                needs_id.append(item)
            except:
                item = ''
        prod_needs = ProductNeed.objects.filter(q_needs).values_list('product_id', flat=True)
        pr = []
        for i in prod_needs:
            if i not in pr:
                pr.append(i)
        prod_needs = pr

    q_resources = Q()
    if resources:
        for item in resources:
            try:
                item = int(item)
                q_resources.add(Q(resource_id=item), Q.OR)
                resources_id.append(item)
            except:
                item = ''

    q_needs = Q()
    if needs:
        for item in prod_needs:
            q_needs.add(Q(pk=item), Q.OR)

    q_brand = Q()
    if brand:
        for item in brand:
            try:
                item = int(item)
                q_brand.add(Q(brand_id=item), Q.OR)
                brands_id.append(item)
            except:
                item = ''

    try:
        price_from = int(prices[0])
    except:
        price_from = ''
    try:
        price_until = int(prices[1])
    except:
        price_until = ''
    q_price = Q()
    if price_from and not price_until:
        q_price = Q(price__gte=price_from)
    if price_until and not price_from:
        q_price = Q(price__lte=price_until)
    if price_from and price_until and price_from < price_until:
        q_price = Q(price__gte=price_from) & Q(price__lte=price_until)
    # print(q_price)

    product = Product.objects.filter(Q(q_resources) & Q(q_needs) & Q(q_brand) & Q(q_price))
    # print(product)
    # print(product.count())

    return render(request, 'Catalog/Items_catalog.html', locals())


def Item_card(request, slug):
    number, email = func_contact()

    # print(slug)
    slug = str(slug)
    slug = slug.split('-')
    try:
        s_id = int(slug[0])
        s_name = '-'.join(slug[1:])
        itm = Product.objects.get(id=s_id)
        if slugify(itm.title) != s_name:
            print('slug error')
            # вывод страницы 404
        else:
            item = itm
            # prods = ProductForNews.objects.filter(news_id=item.id)
    except:
        print('slug error')
        # вывод страницы 404

    return render(request, 'Catalog/Item_card.html', locals())
