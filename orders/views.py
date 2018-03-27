# -*- coding: utf-8 -*-
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import OrderItem, Order
from shop.models import Product
from .forms import OrderCreateForm
from .tasks import OrderCreated
import weasyprint


@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])
    return response


@staff_member_required
def AdminOrderCompete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.completed:
        Order.objects.filter(id=order_id).update(completed=True, paid=True)

        for item in order.items.all():
            ordered = list(Product.objects.filter(name=item.product).values('ordered'))[0]['ordered'] - item.quantity
            stock = list(Product.objects.filter(name=item.product).values('stock'))[0]['stock'] - item.quantity
            Product.objects.filter(name=item.product).update(ordered=ordered, stock=stock)
    return render(request, 'admin/orders/order/complete.html', {'order': order})


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                item['product'].ordered += item['quantity']
                print("##############", item, "##############")
                item['product'].save()
            cart.clear()

            # Ассинхронная отправка сообщения
            OrderCreated.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})
