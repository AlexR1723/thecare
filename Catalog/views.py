from django.shortcuts import render
from .models import *
from uuslug import slugify
from django.db.models import Q
import random
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import xlrd, xlwt, json, re, hashlib, random, datetime
from collections import Counter
from django.http import Http404
from django.db.models import Count

from django.conf import settings





def f_pages(page, queryset, count_item):
    try:
        cnt_pgs = queryset.count()
    except:
        return True, [], 0, 0, 0, []

    try:
        page = int(page) - 1
        count_pages = int(cnt_pgs / count_item) + (cnt_pgs % count_item > 0)
        if page < 0 or page > count_pages:
            # print('exep 1')
            return False, [], 0, 0, 0, []
        else:
            pgs = page * count_item
    except:
        # print('exep 2')
        return False, [], 0, 0, 0, []
    if pgs == 0:
        query_res = queryset[:count_item]
    else:
        query_res = queryset[pgs:pgs + count_item]

    pages = []
    if page >= 3:
        pages.append(1)
    if page >= 4:
        pages.append('')
    if page - 2 >= 0:
        pages.append(page - 2 + 1)
    if page - 1 >= 0:
        pages.append(page - 1 + 1)
    if count_pages != 1:
        pages.append(page + 1)
    chs = len(pages)
    if page + 1 < count_pages:
        pages.append(page + 1 + 1)
    if page + 2 < count_pages:
        pages.append(page + 2 + 1)
    if count_pages - page > 4:
        pages.append('')
    if count_pages - page > 3:
        pages.append(count_pages)

    if page - 1 >= 0:
        prev = page - 1 + 1
    else:
        prev = False
    if page + 1 < count_pages:
        next = page + 1 + 1
    else:
        next = False

    return True, pages, chs, prev, next, query_res


def get_filter(text):
    filter_dict = {'new': '-id', 'price_up': 'productsize__price', 'price_down': '-productsize__price', 'name': 'title'}
    filt = filter_dict.get(str(text))
    if not filt:
        filt = '-id'
    return filt


def search(text, is_search=False):
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

    q_needs = Q()
    if needs:
        q_needs1 = Q()
        for item in needs:
            try:
                item = int(item)
                q_needs1.add(Q(need_id=item), Q.OR)
                needs_id.append(item)
            except:
                item = ''
        prod_needs = set(ProductNeed.objects.filter(q_needs1).values_list('product_id', flat=True))
        for item in prod_needs:
            q_needs.add(Q(id=item), Q.OR)

    q_resources = Q()
    if resources:
        for item in resources:
            try:
                item = int(item)
                q_resources.add(Q(resource_id=item), Q.OR)
                resources_id.append(item)
            except:
                item = ''

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
    if price_from:
        q_price.add(Q(price__gte=price_from), Q.AND)
    if price_until:
        q_price.add(Q(price__lte=price_until), Q.AND)

    qname = Q()
    if is_search == 'Поиск':
        names = str(is_search).lower().split('_')
        for i in names:
            qname.add(Q(title__icontains=i), Q.AND)
    if q_resources or q_needs or q_brand or q_price or qname:
        product = Product.objects.filter(Q(q_resources) & Q(q_needs) & Q(q_brand) & Q(q_price) & Q(qname))
        if is_search == 'New_products':
            dat = datetime.datetime.today() + datetime.timedelta(days=-30)
            product = product.filter(date__gte=dat)
    else:
        product = Product.objects.filter(id=0)
    return resources_id, needs_id, brands_id, price_from, price_until, product


def get_url(url, rec=False):
    url_page = str(url)
    dict = {'For_men': 'Для мужчин',
            'For_body': 'Для тела',
            'For_face': 'Для лица',
            'For_hair': 'Для волос',
            'Dyes_for_hair': 'Красители для волос',
            'Sets_and_miniatures': 'Наборы и миниатюры',
            'Beauty_box': 'Бьюти боксы',
            'Sale': 'Скидки',
            'Brands': 'Бренды',
            'New_products': 'Новинки'}
    head = dict.get(url_page)
    # print(head)
    if not head and not rec:
        return url, 'Поиск'

    if rec:
        for key, value in dict.items():
            if value == url:
                url_page = key
                head = value
    return url_page, head


def left_filter(url_page, head, filter=False, prod=False):
    if head == 'Поиск':
        names = str(url_page).lower().split('_')
        print('names')
        print(names)
        qname = Q()
        for i in names:
            qname.add(Q(title__icontains=i), Q.OR)
        qshort = Q()
        for i in names:
            qshort.add(Q(shot_description__icontains=i), Q.OR)
        prod1 = list(Product.objects.filter(qname).values_list('id', flat=True))
        prod2 = list(Product.objects.filter(qshort).values_list('id', flat=True))
        # prod3 = list(set(prod1) & set(prod2))

        if len(prod1) != 0 and len(prod2) != 0:
            prod3 = list(set(prod1) & set(prod2))
            if len(prod3) == 0:
                # print(prod1)
                # print(prod2)
                prod1.extend(prod2)
                prod3 = prod1
            #     print(prod3)
            # print(prod3)
        else:
            if len(prod1) == 0:
                # print('prod1=0')
                prod3 = prod2
            if len(prod2) == 0:
                # print('prod2=0')
                prod3 = prod1

        prod3 = Product.objects.filter(id__in=prod3)
        ids = list(prod3.values_list('id', flat=True))
        need = NeedType.objects.filter(productneed__product__id__in=ids).distinct().order_by('name')
        resource = ResourceType.objects.filter(product__id__in=ids).distinct().order_by('name')
        brands = Brands_model.objects.filter(product__id__in=ids).distinct().order_by('name')
        if type(prod).__name__ == 'QuerySet':
            # print('query')
            # prod = prod.filter(qname)
            prod = prod.filter(id__in=ids)
        else:
            # prod = Product.objects.filter(id__in=ids)
            prod = prod3

        if filter:
            prod = prod.order_by(get_filter(filter))
        return False, resource, need, brands, prod
    lefts = False
    if url_page != 'Sale' and url_page != 'Brands' and url_page != 'New_products':
        resource = ResourceType.objects.filter(category__name__icontains=head).order_by('name')
        need = NeedType.objects.filter(category__name__icontains=head).order_by('name')
        brands = Brands_model.objects.all().order_by('name')
        if prod != False and prod.count() == 0:
            return resource, need, brands, prod

        if filter and not prod:
            queryset = Product.objects.filter(category__name__icontains=head).order_by(get_filter(filter))
        if not filter and not prod:
            queryset = Product.objects.filter(category__name__icontains=head).order_by('-id')
        if filter and prod:
            queryset = prod.filter(category__name__icontains=head).order_by(get_filter(filter))
        if not filter and prod:
            queryset = prod.filter(category__name__icontains=head).order_by('-id')
    else:
        brands = Brands_model.objects.all().order_by('name')
        if url_page == 'Sale':
            lefts = 'sale'
            if filter and not prod:
                queryset = Product.objects.filter(productsize__sale__gt=0).order_by(get_filter(filter))
            if not filter and not prod:
                queryset = Product.objects.filter(productsize__sale__gt=0).order_by('-id')
            if filter and prod:
                queryset = prod.filter(productsize__sale__gt=0).order_by(get_filter(filter))
            if not filter and prod:
                queryset = prod.filter(productsize__sale__gt=0).order_by('-id')
            resource = CategoryType.objects.filter(product__productsize__sale__gt=0).distinct().order_by('name')
            need = resource

        if url_page == 'Brands':
            lefts = 'brands'
            if filter:
                if filter == 'new':
                    queryset = prod.order_by('-hit_for_brand', '-id')
                else:
                    queryset = prod.order_by(get_filter(filter))
            else:
                queryset = prod.order_by('-hit_for_brand', '-id')
            resource = CategoryType.objects.all()
            need = resource
        if url_page == 'New_products':
            dat = datetime.datetime.today() + datetime.timedelta(days=-30)
            lefts = 'new'
            print('lefts new prods')
            resource = CategoryType.objects.filter(product__date__gte=dat).distinct().order_by('name')
            need = resource
            if filter and not prod:
                queryset = Product.objects.filter(date__gte=dat).order_by(get_filter(filter))
            if not filter and not prod:
                queryset = Product.objects.filter(date__gte=dat).order_by('-id')
            if filter and prod:
                queryset = prod.order_by(get_filter(filter))
            if not filter and prod:
                queryset = prod.order_by('-id')

    return lefts, resource, need, brands, queryset


def Items_catalog(request):

    return render(request, 'Catalog/Items_catalog.html', locals())


def Face(request):
    # dic = global_function(request)

    # head = 'Средства для лица'
    # product = Product.objects.all()
    # resource = ResourceType.objects.filter(category__name='Для лица')
    # need = NeedType.objects.filter(category__name='Для лица')
    # url_page = 'face'

    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog(request, head_url):
    print('catalog')
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    print(head_url)
    print(url_page)
    print(head)
    is_search = False
    is_filter = False
    is_page = False
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=False)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_filter(request, head_url, filter):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = False
    is_filter = True
    is_page = False

    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=False)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_page(request, head_url, page):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = False
    is_filter = False
    is_page = True

    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=False)
    try:
        page = int(page)
    except:
        raise Http404("")
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if not status:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_page_filter(request, head_url, page, filter):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = False
    is_filter = True
    is_page = True

    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=False)
    try:
        page = int(page)
    except:
        raise Http404("")
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if not status:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search(request, head_url, text):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = True
    is_filter = False
    is_page = False

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=product)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_filter(request, head_url, text, filter):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = True
    is_filter = True
    is_page = False

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=product)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_page(request, head_url, text, page):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = True
    is_filter = False
    is_page = True

    try:
        page = int(page)
    except:
        raise Http404("")

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=product)
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_page_filter(request, head_url, text, page, filter):
    url_page, head = get_url(head_url)
    if not head:
        raise Http404("")
    is_search = True
    is_filter = True
    is_page = True

    try:
        page = int(page)
    except:
        raise Http404("")

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=product)
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        raise Http404("")
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Item_card(request, slug):
    slug = str(slug).split('-')
    try:
        s_id = int(slug[0])
        s_name = '-'.join(slug[1:])
        itm = Product.objects.get(id=s_id)
        if slugify(itm.title) != s_name:
            raise Http404("")
        else:
            item = itm
            category, head = get_url(item.category.name, True)
    except:
        raise Http404("")

    res = ProductNeed.objects.filter(product_id=item.id).values_list('need_id', flat=True)
    query = Q()
    for i in res:
        query.add(Q(need_id=i), Q.OR)
    prods = ProductNeed.objects.filter(Q(query)).exclude(product_id=item.id)
    ids = list(prods.values_list('product_id', flat=True))
    ids.sort(key=Counter(ids).get, reverse=True)
    ids1 = []
    for i in ids:
        if len(ids1)>=12:
            break
        else:
            if i not in ids1:
                ids1.append(i)
    prods = Product.objects.filter(id__in=ids1)
    res=[]
    for i in ids1:
        for j in prods:
            if i==j.id:
                res.append(j)
    prods=res

    sizes = ProductSize.objects.filter(product_id=item.id)
    if sizes.count() == 1:

        if sizes[0].size.float_name != 0.0:
            sizename = sizes[0].size.float_name
        else:
            not_size = True
        if sizes[0].size.str_name:
            sizename = sizes[0].size.str_name

    sizes = sizes.order_by('size__float_name')
    lst = []
    have_sale = False
    have_tone=False
    for i in sizes:
        # ls = []
        res={}
        res['id']=i.id
        # ls.append(i.id)
        if i.size.float_name:
            res['size'] = i.size.float_name
            # ls.append(i.size.float_name)
        if i.size.str_name:
            res['size'] = i.size.str_name
            # ls.append(i.size.str_name)
        # ls.append(i.price)
        # ls.append(i.old_price)
        # ls.append(i.count)
        # ls.append(i.sale)
        res['price']=i.price
        res['old_price'] = i.old_price
        res['count'] = i.count
        res['sale'] = i.sale
        if int(i.sale) > 0:
            print(i)
            have_sale = True
        if i.is_tone:
            have_tone=True
        # lst.append(ls)
        lst.append(res)
    print(lst)
    # tones=[]
    # if have_tone:
    #     tn={}
    #     tn['id']
    # result={}
    # for i in sizes:
    #
    return render(request, 'Catalog/Item_card.html', locals())
