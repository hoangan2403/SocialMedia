import datetime

from django.db.models import Count
from .models import *
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractQuarter


def load_Auction(params={}):
    q = Auction.objects.filter(active = True)

    kw = params.get('kw')
    if kw:
        q = q.filter(product__icontains=kw)

    cate_id = params.get('product_cate_id')
    if cate_id:
        q = q.filter(product__category_id=cate_id)

    return q

def top_user_by_post(year):
    d = User.objects.filter(userpost__created_date__year=year).annotate(count=Count('userpost')).values('id', 'username', 'count').order_by('-count')[:10]
    return d

def count_user():
    u = User.objects.all().count()

    return u


def count_Post():
    current_year = datetime.datetime.now().year
    d = Post.objects.filter(created_date__year=current_year).count()

    return d


def count_Auction():
    current_year = datetime.datetime.now().year
    a = Auction.objects.filter(created_date__year=current_year).count()

    return a


def count_Auction_By_Time(year, quarter):
    current_year = datetime.datetime.now().year
    # current_quarter = (datetime.datetime.now().month - 1) // 3 + 1
    year = int(year) if year else None
    quarter = int(quarter) if quarter else None
    try:
        year = int(year)
    except (ValueError, TypeError):
        year = None

    # if quarter is not None:
    try:
        quarter = int(quarter)
    except (ValueError, TypeError):
        quarter = None

    if quarter is None:
        a = []
        d = Auction.objects.filter(start_date__year=current_year).annotate(month=ExtractMonth('start_date')).annotate(count=Count('id')).values('month', 'count').order_by('month')
        for i in range(12):
            tong = 0;
            for t in d:
                if (i + 1) == t['month']:
                    tong += t['count']

            data1 = {
                'month': (i + 1),
                'sum': tong
            }
            a.append(data1)
        return a
    else:
        a1 = []

        d1 = Auction.objects.filter(start_date__year=year).annotate(month=ExtractMonth('start_date')).annotate(count=Count('id')).values('month', 'count').order_by('month')

        for i in range(12):
            tong = 0;
            for t in d1:
                if (i + 1) == t['month']:
                    tong += t['count']

            data = {
                'month': (i + 1),
                'sum': tong
            }
            a1.append(data)
        quarters=[]
        # dau = 1
        # cuoi = 4
        # if( quarter == 2):
        #     dau = 4
        #     cuoi = 7
        # if( quarter == 3):
        #     dau = 7
        #     cuoi = 10
        # if(quarter==4):
        #     dau = 10
        #     cuoi= 13

        dau = (3 * quarter) - 2
        cuoi = (quarter * 3) + 1

        for i in range(dau, cuoi):
            for q in a1:
                if i == q['month']:
                    quarters.append(q)

        return quarters



def count_Auction_by_quater():
    quater = [1, 2, 3, 4]
    year = 2024
    d =[]
    a = (Auction.objects.filter(start_date__year=2024).annotate(quater=ExtractQuarter('start_date')).annotate(count=Count('id')).values('quater','count').order_by('quater'))
    for i in quater:
        tong = 0
        for t in a:
            if i == t['quater']:
                tong += t['count']

        data = {
            'quater': i,
            'count': tong
        }
        d.append(data)
    return d



def count_Auction_by_month():
    year='2024'
    c = Auction.objects.annotate(count=Count('id')).filter(start_date__year=year)
    d = Auction.objects.filter(start_date__year=2024).annotate(month=ExtractMonth('start_date')).annotate(count=Count('id')).values('month','count').order_by('month')
    a=[]

    for i in range(12):
        tong = 0;
        for t in d:
            if (i+1) == t['month']:
                tong+= t['count']

        data={
            'month':(i+1),
            'sum':tong
        }
        a.append(data)
    print(a)
    return a


def count_Auction_By_CateOfProduct(year, month):
    filters = {}
    if year:
        filters['product__auction__start_date__year'] = year
        if month:
            filters['product__auction__start_date__month'] = month

    return (Category.objects.filter(**filters).annotate(count3=Count('product__auction__id'))
            .values("id", "name", "count3").order_by('count3'))


def count_LikeAuction_By_CateOfProduct(year, month):
    filters = {}
    if year:
        filters['product__auction__start_date__year'] = year
        if month:
            filters['product__auction__start_date__month'] = month

    return (Category.objects.filter(**filters).annotate(count1=Count('product__auction__user_care__id'))
            .values("id", "name", "count1").order_by('count1'))


def count_CmmAuction_By_CateOfProduct(year, month):
    filters = {}
    if year:
        filters['product__auction__start_date__year'] = year
        if month:
            filters['product__auction__start_date__month'] = month

    return (Category.objects.filter(**filters).annotate( count2=Count('product__auction__participateauction__id'))
            .values("id","name","count2").order_by('count2'))


def get_year_of_auction():
    return Auction.objects.values('start_date__year').distinct()

# def count_Auction_By_Date():
#