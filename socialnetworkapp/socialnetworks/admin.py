import datetime

from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe, format_html
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path, reverse
from . import dao
from .models import Category, Product, User, Auction, Post, LikeType, Report, ReportType, Hashtag, ParticipateAuction


class SocialNetworkAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống mạng xã hội từ thiện'
    index_title = 'Bảng dữ liệu mạng xã hội từ thiện'

    def get_urls(self):
        return [
                   path('stats/', self.admin_view(self.stats_view), name='stats'),
                   path('nhap/', self.admin_view(self.nhap), name='nhap')
               ] + super().get_urls()

    def stats_view(self, request):
        year = request.GET.get('year')
        month = request.GET.get('month')
        quarters = request.GET.get('quarters')

        stats_like = dao.count_LikeAuction_By_CateOfProduct(year, month)
        stats_cmm = dao.count_CmmAuction_By_CateOfProduct(year, month)
        stats_auction = dao.count_Auction_By_CateOfProduct(year, month)

        return TemplateResponse(request, 'admin/stats.html', {
            'stats_Like': stats_like,
            'stats_Cmm': stats_cmm,
            'stats_Auction': stats_auction,
            'count': dao.count_Auction(year, quarters)
        })

    def nhap(self, request):
        year = request.GET.get('year')
        month = request.GET.get('month')
        quarters = request.GET.get('quarters')
        year_current = datetime.datetime.now().year
        print(year_current)

        stats_like = dao.count_LikeAuction_By_CateOfProduct(year, month)
        stats_cmm = dao.count_CmmAuction_By_CateOfProduct(year, month)
        stats_auction = dao.count_Auction_By_CateOfProduct(year, month)

        return TemplateResponse(request,'admin/nhap.html',{
            'stats_Like': stats_like,
            'stats_Cmm': stats_cmm,
            'stats_Auction': stats_auction,
            'years': dao.get_year_of_auction(),
            'counts_month': dao.count_Auction_by_month(),
            'count_quarter': dao.count_Auction_by_quater(),
            'count_auction': dao.count_Auction_By_Time(year, quarters),
            'count_post': dao.count_Post(),
            'year': year_current,
            'count_auction_current_year': dao.count_Auction(),
            'count_user': dao.count_user(),
            'top_3': dao.top_user_by_post(year_current)
        })

    def object_link(self, item):
        url = item.get_absolute_url()
        return format_html('<a href="{url}">open</a>', url=url)
    object_link.short_description = 'View on site'


admin_site = SocialNetworkAppAdminSite(name='myapp')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','image','name','description']
    readonly_fields = ['img']
    form = ProductForm

    def img(self, product):
        if product:
            return mark_safe(
                '<img src="/static/{url}" width = "120"/>' .format(url=product.image.name)
            )

    class Media:
        css = {
            'all' : ('/static/css/style.css', )
        }


class AuctionAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'product', 'start_date', 'end_date']


# Register your models here.
admin_site.register(Category, CategoryAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(User)
admin_site.register(Auction, AuctionAdmin)
admin_site.register(Post)
admin_site.register(LikeType)
admin_site.register(Report)
admin_site.register(ReportType)
admin_site.register(Hashtag)
admin_site.register(ParticipateAuction)
