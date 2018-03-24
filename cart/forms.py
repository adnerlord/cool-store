# -*- coding: utf-8 -*-
from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label="Кол-во", choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
