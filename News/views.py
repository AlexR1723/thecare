from django.shortcuts import render
from .models import *
import datetime, traceback
from uuslug import slugify


def func_contact():
    number = Contact.objects.filter(is_main=True, contact_id=2)[0].text
    email = Contact.objects.filter(is_main=True, contact_id=4)[0].text
    return number, email


def f_pages(page, queryset):
    cnt_pgs = queryset.count()

    try:
        page = int(page) - 1
        count_pages = int(cnt_pgs / 10) + (cnt_pgs % 10 > 0)
        if page < 0 or page > count_pages:
            # print('exep 1')
            return False, [], 0, 0, 0, []
        else:
            pgs = page * 10
    except:
        # print('exep 2')
        return False, [], 0, 0, 0, []
    if pgs == 0:
        query_res = queryset[:10]
    else:
        query_res = queryset[pgs:pgs + 10]

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


def News(request):
    number, email = func_contact()
    news = News_model.objects.all()[:10]

    # News_model.objects.all().delete()
    #
    # text = ' Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et ' \
    #        'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ' \
    #        'ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu ' \
    #        'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt ' \
    #        'mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ' \
    #        'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ' \
    #        'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate ' \
    #        'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt ' \
    #        'in culpa qui officia deserunt mollit anim id est laborum'
    # for i in range(93):
    #     # sl=
    #     n = News_model(name='News number #' + str(i), text='Text for news number #' + str(i) + text)
    #     n.save()
    #     print(i)



    # lst=News_model.objects.all()
    # for i in lst:
    #     i.slug=slugify(str(i.id)+'-'+i.name)
    #     i.save()

    page = 1
    queryset = News_model.objects.count()

    queryset = News_model.objects.all().order_by('-date')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset)
    if status == False:
        # вывод страницы 404
        print('news pages error')
    else:
        news = query_res

    return render(request, 'News/News.html', locals())


def News_page(request, page):
    number, email = func_contact()

    queryset = News_model.objects.all().order_by('-date')
    status, pages, chs, prev, next, query_res = f_pages(page, queryset)
    if status == False:
        # вывод страницы 404
        print('news pages error')
    else:
        news = query_res

    return render(request, 'News/News.html', locals())

def News_detail(request, slug):
    number, email = func_contact()

    # print(slug)
    slug=str(slug)
    slug=slug.split('-')
    # print(slug)
    s_id = int(slug[0])
    s_name = '-'.join(slug[1:])

    item=News_model.objects.get(id=s_id)

    # print(slugify(item.name))
    # print(s_name)

    if slugify(item.name)!=s_name:
        print('slug error')
        # вывод страницы 404
    else:
        news=item


    return render(request, 'News/News_details.html', locals())