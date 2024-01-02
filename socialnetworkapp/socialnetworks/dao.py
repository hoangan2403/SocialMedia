from django.db.models import Count
from .models import Auction, Category, Product


def load_Auction(params={}):
    q = Auction.objects.filter(active = True)

    kw = params.get('kw')
    if kw:
        q = q.filter(product__icontains=kw)

    cate_id = params.get('product_cate_id')
    if cate_id:
        q = q.filter(product__category_id=cate_id)

    return q


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


# def count_Auction_By_Date():
#