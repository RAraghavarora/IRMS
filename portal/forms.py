from dal import autocomplete
from django import forms
from portal.models import Reserves, Aqbasket
from django.utils.translation import ugettext_lazy as _


class ReservesForm(forms.ModelForm):
    class Meta:
        model = Reserves
        fields = ['itemnumber']
        widgets = {
            'itemnumber': autocomplete.ModelSelect2(url='portal:search_query')
        }
        labels = {
            "itemnumber": _("Search for a book "),
        }

class AqBasketForm(forms.ModelForm):
    class Meta:
        model = Aqbasket
        fields = ['booksellerid']
        widgets = {
            'booksellerid': autocomplete.ModelSelect2(url='portal:search_vendor')
        }
        labels = {
            "booksellerid": _("Choose Vendor"),
        }

text = "gAAAAABdCNv9XAmsfL2yJEbYX6InJi8Ky10Ltr3SIcrVz6GKlxWc1AOau1WgXz0oQFKW6WTrqczx89YD3r2GdZKDxPItyAODag=="
