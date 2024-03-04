from django.contrib import admin
from .models import Item, Order, Discount, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total_cost')
    list_filter = ('created_at',)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('order', 'percentage')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('order', 'percentage')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)
