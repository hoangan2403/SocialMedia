from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from . import dao
from .models import Category, Product, User, Auction, Post, LikeType, Report, ReportType, Hashtag, ParticipateAuction


class SocialNetworkAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống mạng xã hội từ thiện'

    def get_urls(self):
        return [
                   path('auction-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        year = request.GET.get('year')
        month = request.GET.get('month')

        stats_like = dao.count_LikeAuction_By_CateOfProduct(year, month)
        stats_cmm = dao.count_CmmAuction_By_CateOfProduct(year, month)
        stats_auction = dao.count_Auction_By_CateOfProduct(year, month)

        return TemplateResponse(request, 'admin/stats.html', {
            'stats_Like': stats_like,
            'stats_Cmm': stats_cmm,
            'stats_Auction': stats_auction
        })


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