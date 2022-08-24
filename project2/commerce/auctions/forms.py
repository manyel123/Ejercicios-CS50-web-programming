from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = (
            'user_id',
            'creation_date',
            'is_active',
        )
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'initial_bid': forms.NumberInput(attrs={'class': 'form-control'}),
        }