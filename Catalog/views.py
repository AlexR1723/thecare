from django.shortcuts import render
from .models import *
from uuslug import slugify
from django.db.models import Q
import random


def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
    return number, email


def f_pages(page, queryset, count_item):
    cnt_pgs = queryset.count()

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
    filter_dict = {'new': '-id', 'price_up': 'price', 'price_down': '-price', 'name': 'title'}
    try:
        filt = filter_dict[str(text)]
    except:
        filt = '-id'
    return filt


def search(text):
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
    product = Product.objects.filter(Q(q_resources) & Q(q_needs) & Q(q_brand) & Q(q_price))
    return resources_id ,needs_id ,brands_id,product

def get_url(url):
    url_page = str(url)
    dict={'For_men':'Для мужчин',
          'For_body': 'Для тела',
          'For_face': 'Для лица',
          'For_hair': 'Для волос',
          'Dyes_for_hair': 'Красители для волос',
          'Sale': 'Скидки',
          'Sets_and_miniatures': 'Наборы и миниатюры'
          }
    try:
        head=dict[url_page]
    except:
        head=False

    print(head)
    print(url_page)
    return url_page,head


def Items_catalog(request):
    number, email = func_contact()

    return render(request, 'Catalog/Items_catalog.html', locals())


def Face(request):
    number, email = func_contact()

    head = 'Средства для лица'
    product = Product.objects.all()
    resource = ResourceType.objects.filter(category__name='Для лица')
    need = NeedType.objects.filter(category__name='Для лица')
    url_page = 'face'

    # function "add resource type"
    # res_list = CategoryType.objects.all()
    # inc = 0
    # for i in res_list:
    #     for j in range(7):
    #         sj = str(j)
    #         res = ResourceType(name='Средство ' + i.name + ' #' + sj, category_id=i.id)
    #         res.save()
    #         inc = inc + 1
    #         print('res type ' + str(inc) + '/' + str(res_list.count() * 7))

    # function "add needs type"
    # res_list=CategoryType.objects.all()
    # inc=0
    # for i in res_list:
    #     for j in range(7):
    #         sj=str(j)
    #         res=NeedType(name='Потребность '+i.name+' #'+sj, category_id=i.id)
    #         res.save()
    #         inc = inc + 1
    #         print('needs '+str(inc)+'/'+str(res_list.count()*7))

    # function "add product"
    # cat = 'Красители для волос'
    # lorem = ' Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus tincidunt finibus sem, quis maximus purus ' \
    #         'porttitor mollis. Sed sem eros, finibus nec orci nec, tristique fringilla massa. Phasellus pharetra, nunc in' \
    #         ' sollicitudin porttitor, lectus libero sagittis sapien, a volutpat orci nunc ac libero. Duis ut mi et ipsum' \
    #         ' rutrum varius. Cras auctor rutrum sem, euismod mollis purus interdum ac. Duis at dictum felis. Vivamus' \
    #         ' gravida, odio dapibus ornare faucibus, libero ipsum dignissim erat, non suscipit lacus nunc sed eros. Proin' \
    #         ' et purus mauris. In varius libero elit, imperdiet ornare neque fermentum sit amet. Sed sed nunc ultricies,' \
    #         ' tincidunt sem quis.'
    #
    # brnds = Brands_model.objects.all().values_list('id', flat=True)
    # category_type = CategoryType.objects.get(name__icontains=cat).id
    # res=ResourceType.objects.filter(category_id=category_type).values_list('id',flat=True)
    # for i in range(300):
    #     si = str(i)
    #     rand = random.randrange(1, 12)
    #     img = 'uploads/test_' + str(rand) + '.png'
    #     price = random.randrange(100, 30000, 50)
    #     artic = random.randrange(10000000, 99999999)
    #     size = random.randrange(10, 1000, 10)
    #     p = Product(title='Product #' + si, shot_description='Short description for product #' + si,
    #                 description='Full description for produc #' + si + lorem, main_photo=img, price=price,
    #                 artikul=artic, note='Note for product #' + si + lorem,
    #                 components='Components for product #' + si + lorem, size=size, brand_id=random.choice(brnds),
    #                 category_id=category_type,resource_id=random.choice(res))
    #     p.save()
    #     print('prod #' + si + '/' + str(300))

    # function "add product need"
    # cat = 'Для мужчин'
    # prods=Product.objects.filter(category__name__icontains=cat)
    # needs=NeedType.objects.filter(category__name__icontains=cat).values_list('id', flat=True)
    # needs=list(needs)
    # inc=0
    # for i in prods:
    #     count_needs=random.randrange(1,5)
    #     nds=needs
    #     random.shuffle(nds)
    #     for j in range(count_needs):
    #         pn=ProductNeed(product_id=i.id,need_id=nds[j])
    #         pn.save()
    #     inc=inc+1
    #     print('prod #' + str(inc) + '/' + str(prods.count())+' count prod need:'+str(count_needs))

    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog(request,head_url):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page,head=get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')

    is_search = False
    is_filter = False
    is_page=False
    # print('is for men')
    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    page = 1
    queryset = Product.objects.filter(category__name__icontains=head).order_by('-id')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men error')
    else:
        products = query_res

    # link_filter='/catalog/'+url_page+'/'
    # prod_list = list()
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_filter(request,head_url, filter):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = False
    is_filter = True
    is_page=False
    print('is filter')
    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    page = 1
    queryset = Product.objects.filter(category__name__icontains=head).order_by(get_filter(filter))
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men error')
    else:
        products = query_res

    # prod_list = list()
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_page(request,head_url, page):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = False
    is_filter = False
    is_page=True
    print('is page')

    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')

    queryset = Product.objects.filter(category__name__icontains=head).order_by('-id')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if not status:
        # вывод страницы 404
        print('catalog for_men pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_page_filter(request,head_url, page, filter):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = False
    is_filter = True
    is_page=True

    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')

    queryset = Product.objects.filter(category__name__icontains=head).order_by(get_filter(filter))
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if not status:
        # вывод страницы 404
        print('catalog for_men pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search(request,head_url, text):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = False
    is_page=False

    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    resources_id ,needs_id ,brands_id,product = search(text)

    page = 1
    queryset = product.order_by('-id')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_filter(request,head_url, text, filter):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = True
    is_page=False

    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    resources_id ,needs_id ,brands_id,product = search(text)

    page = 1
    queryset = product.order_by(get_filter(filter))
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_page(request,head_url, text, page):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = False
    is_page=True

    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')

    resources_id ,needs_id ,brands_id,product = search(text)

    queryset = product.order_by('-id')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_page_filter(request,head_url, text, page, filter):
    number, email = func_contact()

    # head = 'Для мужчин'
    # url_page = 'for_men'
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = True
    is_page=True

    resource = ResourceType.objects.filter(category__name__icontains=head)
    need = NeedType.objects.filter(category__name__icontains=head)
    brands = Brands_model.objects.all()

    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')

    resources_id ,needs_id ,brands_id,product = search(text)

    queryset = product.order_by(get_filter(filter))
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search pages error')
    else:
        products = query_res
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
