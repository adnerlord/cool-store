# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from orders.models import Order
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from io import BytesIO
import weasyprint


def PaymentNotification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()

        # Отправка Email
        subject = 'Cool-Store - заказ: {}'.format(order.id)
        message = 'К email сообщению прикреплен PDF файл с информацией о вашем заказе.'
        email = EmailMessage(subject, message, 'ejen.proj.shop@gmail.com', [order.email])

        # Генерация PDF
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        weasyprint.HTML(string=html).write_pdf(out,
                                               stylesheets=[
                                                   weasyprint.CSS(settings.STATIC_ROOT + 'css/bootstrap.min.css')])

        # Прикрепляем pdf
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()


valid_ipn_received.connect(PaymentNotification)
