from django.shortcuts import render
from .models import *
from uuslug import slugify
from django.db.models import Q
import random
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import xlrd, xlwt, json, re, hashlib, random, datetime

from django.conf import settings


# def global_function(request):
#     number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
#     email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
#
#     ses = request.session.get(settings.CART_SESSION_ID)
#     ids = []
#     for i in ses.keys():
#         ids.append(int(i))
#     prods = ProductSize.objects.filter(id__in=ids)
#     for i in ids:
#         prod = prods.filter(id=i)[0]
#         count = ses[str(i)]['count']
#         ses[str(i)]['total'] = prod.price * count
#
#     basket = 0
#     ses = request.session.get(settings.CART_SESSION_ID)
#     if ses and ses is not None:
#         for i in ses.values():
#             basket += int(i['total'])
#
#     is_auth = request.user.is_authenticated
#     if is_auth:
#         is_auth = request.session.get('username', False)
#
#     user_name = ''
#     if is_auth:
#         user_name = AuthUser.objects.get(username=is_auth).first_name
#
#     result_dict = {
#         'number': number,
#         'email': email,
#         'basket': basket,
#         'is_auth': is_auth,
#         'user_name': user_name
#     }
#     return result_dict


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
        # print(qname)
        qshort=Q()
        for i in names:
            qshort.add(Q(shot_description__icontains=i), Q.OR)
        # print(qname)
        prod1 = list(Product.objects.filter(qname).values_list('id',flat=True))
        prod2 = list(Product.objects.filter(qshort).values_list('id',flat=True))
        print(len(prod1))
        print(len(prod2))

        # prod3 = list(set(prod1) & set(prod2))


        if len(prod1)!=0 and len(prod2)!=0:
            prod3=list(set(prod1) & set(prod2))
            if len(prod3)==0:
                # print(prod1)
                # print(prod2)
                prod1.extend(prod2)
                prod3=prod1
            #     print(prod3)
            # print(prod3)
        else:
            if len(prod1)==0:
                # print('prod1=0')
                prod3=prod2
            if len(prod2)==0:
                # print('prod2=0')
                prod3=prod1


        # prod1=prod3
        # print(len(prod3))
        # print(prod3)
        # print(type(prod))
        prod3=Product.objects.filter(id__in=prod3)
        # ids = list(prod1.values_list('id', flat=True))
        ids = list(prod3.values_list('id', flat=True))
        # print(len(ids))
        need = NeedType.objects.filter(productneed__product__id__in=ids).distinct('id').order_by('id', 'name')
        resource = ResourceType.objects.filter(product__id__in=ids).distinct('id').order_by('id', 'name')
        brands = Brands_model.objects.filter(product__id__in=ids).distinct('id').order_by('id', 'name')
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
            resource = CategoryType.objects.filter(product__productsize__sale__gt=0).distinct('id')
            need = resource

        if url_page == 'Brands':
            lefts = 'brands'
            if filter:
                if filter=='new':
                    queryset = prod.order_by('-hit_for_brand', '-id')
                else:
                    queryset = prod.order_by(get_filter(filter))
            else:
                queryset = prod.order_by('-hit_for_brand','-id')
            resource = CategoryType.objects.all()
            need = resource
        if url_page == 'New_products':
            dat = datetime.datetime.today() + datetime.timedelta(days=-30)
            lefts = 'new'
            resource = CategoryType.objects.filter(product__date__gte=dat).distinct('id')
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
    # dic = global_function(request)

    return render(request, 'Catalog/Items_catalog.html', locals())


def Face(request):
    # dic = global_function(request)

    head = 'Средства для лица'
    product = Product.objects.all()
    resource = ResourceType.objects.filter(category__name='Для лица')
    need = NeedType.objects.filter(category__name='Для лица')
    url_page = 'face'

    # print(Product.objects.filter(sale__gt=0).count())
    # prod_list=Product.objects.all().values_list('id',flat=True)
    # prod_list=random.choices(list(prod_list),k=300)
    # print('count - '+str(len(prod_list)))
    # inc=0
    # for i in prod_list:
    #     s=Product.objects.get(id=i)
    #     type_sale=random.randint(0,1)
    #     if type_sale==0:
    #         c_sale=random.randint(5,75)
    #         s.sale_is_number=False
    #         s.sale=c_sale
    #         s.sale_price=int(s.price*(100-c_sale)/100)
    #     else:
    #         c_sale = random.randint(50, s.price-30)
    #         s.sale_is_number = True
    #         s.sale = c_sale
    #         s.sale_price = int(s.price-c_sale)
    #     s.save()
    #     inc=inc+1
    #     print(str(inc)+'/'+str(len(prod_list)))

    # print(Product.objects.filter(sale__gt=0).count())
    # prods=Product.objects.filter(sale__gt=0)
    # prods=Product.objects.all()
    # inc=0
    # for i in prods:
    #     i.sale=0
    #     i.sale_is_number=False
    #     i.sale_price=0
    #     i.save()
    #     inc=inc+1
    #     print(str(inc)+'/'+str(prods.count()))

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


def Catalog(request, head_url):
    # dic = global_function(request)
    print('catalog')
    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
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
        # вывод страницы 404
        print('catalog for_men error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_filter(request, head_url, filter):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = False
    is_filter = True
    is_page = False

    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=False)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_page(request, head_url, page):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = False
    is_filter = False
    is_page = True

    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=False)
    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if not status:
        # вывод страницы 404
        print('catalog for_men pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_page_filter(request, head_url, page, filter):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = False
    is_filter = True
    is_page = True

    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=False)
    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if not status:
        # вывод страницы 404
        print('catalog for_men pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search(request, head_url, text):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = False
    is_page = False

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=product)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_filter(request, head_url, text, filter):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = True
    is_page = False

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=product)
    page = 1
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_page(request, head_url, text, page):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = False
    is_page = True

    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=False, prod=product)
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Catalog_search_page_filter(request, head_url, text, page, filter):
    # dic = global_function(request)

    url_page, head = get_url(head_url)
    if not head:
        # вывод страницы 404
        print('catalog for_men error')
    is_search = True
    is_filter = True
    is_page = True

    try:
        page = int(page)
    except:
        # вывод страницы 404
        print('catalog for_men pages error')

    resources_id, needs_id, brands_id, price_from, price_until, product = search(text, head_url)
    spec, resource, need, brands, queryset = left_filter(url_page, head, filter=filter, prod=product)
    status, pages, chs, prev, next, query_res = f_pages(page, queryset, 12)
    if status == False:
        # вывод страницы 404
        print('catalog for_men search pages error')
    else:
        products = query_res
    return render(request, 'Catalog/Items_catalog.html', locals())


def Item_card(request, slug):
    # dic = global_function(request)
    slug = str(slug)
    slug = slug.split('-')
    # s_id = int(slug[0])
    # s_name = '-'.join(slug[1:])
    # itm = Product.objects.get(id=s_id)
    # item=itm
    # category, head = get_url(item.category.name, True)
    # cat=item.category.id
    try:
    	s_id = int(slug[0])
    	s_name = '-'.join(slug[1:])
    	itm = Product.objects.get(id=s_id)
    	
    	# if slugify(itm.title) != s_name:
    	# 	print('slug error')
    	# 	# вывод страницы 404
    	# 	return render(request, 'Catalog/Item_card.html', locals())
    	# else:
    	item = itm
    	category, head = get_url(item.category.name, True)
    	# вывод страницы 404
    	cat = item.category.id
    	res = item.resource_id
    	ress = ProductNeed.objects.filter(product_id=item.id).values_list('need_id', flat=True)
    	query = Q()
    	for i in ress:
    		query.add(Q(need_id=i), Q.OR)
    	prods = ProductNeed.objects.filter(Q(query)).exclude(product_id=item.id)
    	prods = prods.order_by('product_id', 'id')
    	# .distinct('product_id')
    	prods = list(prods)
    	prods.reverse()
    	if len(prods) > 12:
    		prods = prods[:12]
    	
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
    	have_sale=False
    	for i in sizes:
    		ls = []
    		ls.append(i.id)
    		if i.size.float_name:
    			ls.append(i.size.float_name)
    		if i.size.str_name:
    			ls.append(i.size.str_name)
    		ls.append(i.price)
    		ls.append(i.old_price)
    		ls.append(i.count)
    		ls.append(i.sale)
    		if int(i.sale)>0:
    			print(i)
    			have_sale=True
    		lst.append(ls)
    	return render(request, 'Catalog/Item_card.html', locals())
    except:
    	print('slug error')
    	return render(request, 'Catalog/Item_card.html', locals())


# def get_product_sizes(request):
#     slug = request.GET.get('slug')
#     sizes = list(ProductSize.objects.filter(product__slug=slug).values())
    # lst = []
    # for i in sizes:
    #     try:
    #         i['size_id'] = float(Size.objects.get(id=i['size_id']).name)
    #     except:
    #         i['size_id'] = Size.objects.get(id=i['size_id']).name
    #     lst.append(i)
    # ls1 = sorted(lst, key=lambda sz: sz['size_id'])
    # return HttpResponse(json.dumps(sizes))
