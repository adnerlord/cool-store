# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Order, OrderItem
import unicodecsv as csv
import datetime


def OrderDetail(obj):
    return format_html('<a href="{}">Посмотреть</a>'.format(
        reverse('orders:AdminOrderDetail', args=[obj.id])))


OrderDetail.short_description = 'Инфо'


def ExportToCSV(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
            filename=Orders-{}.csv'.format(datetime.datetime.now().strftime("%d/%m/%Y"))
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Первая строка- оглавления
    writer.writerow([field.verbose_name for field in fields])
    # Заполняем информацией
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


ExportToCSV.short_description = 'Export to CSV'


def OrderPDF(obj):
    return format_html('<a href="{}">PDF</a>'.format(
        reverse('orders:AdminOrderPDF', args=[obj.id])
    ))


OrderPDF.short_description = 'В PDF'


def OrderComplete(obj):
    return format_html('<a href="{}">Завершить</a>'.format(
        reverse('orders:AdminOrderCompete', args=[obj.id])
    ))


OrderComplete.short_description = 'Завершить'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'completed', 'created', 'updated',
                    OrderDetail, OrderPDF, OrderComplete]
    list_filter = ['paid', 'completed', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [ExportToCSV]


admin.site.register(Order, OrderAdmin)
