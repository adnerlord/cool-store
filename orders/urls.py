from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$',
        views.OrderCreate,
        name='OrderCreate'),
    url(r'^admin/order/(?P<order_id>\d+)/detail/$',
        views.AdminOrderDetail,
        name='AdminOrderDetail'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$',
        views.AdminOrderPDF,
        name='AdminOrderPDF'),
    url(r'^admin/order/(?P<order_id>\d+)/$',
        views.AdminOrderCompete,
        name='AdminOrderCompete'),
]
