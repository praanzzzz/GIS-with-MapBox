from django import forms
from .models import FarmModel

class AddressForm(forms.ModelForm):
    class Meta:
        model = FarmModel
        fields = ['barangay', 'city_or_municipality', 'country']

class FarmDetailsForm(forms.ModelForm):
    class Meta:
        model = FarmModel
        fields = ['acres', 'crops_planted']
