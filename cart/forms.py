# -*- coding: utf-8 -*-
from django import forms

INCOMING_QUANTITY = 6
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, INCOMING_QUANTITY)]


class CartAddProductForm(forms.Form):
    max = 100
    quantity = forms.IntegerField(label="Кол-во", max_value=max, min_value=0, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
