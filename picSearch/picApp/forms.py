from django import forms
from .models import MissingChild

class MissingChildForm(forms.ModelForm):
    class Meta:
        model = MissingChild
        fields = ['name', 'age', 'image', 'date_missing', 'place_of_birth', 'last_seen', 'guardian_name', 'guardian_contact']
