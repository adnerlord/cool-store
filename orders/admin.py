# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from .models import Order, OrderItem


def OrderDetail(obj):
    return format_html('<a href="{}">Посмотреть</a>'.format(
        reverse('orders:AdminOrderDetail', args=[obj.id])))


OrderDetail.short_description = 'Инфо'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated',
                    OrderDetail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
