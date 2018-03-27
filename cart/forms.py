# -*- coding: utf-8 -*-
from django import forms


class CartAddProductForm(forms.Form):
    max = 100
    quantity = forms.IntegerField(label="Кол-во", max_value=max,
                                  min_value=1, initial=1)
    update = forms.BooleanField(required=False, initial=False,
                                widget=forms.HiddenInput)
