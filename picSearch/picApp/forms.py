from django import forms
from .models import MissingChild

class MissingChildForm(forms.ModelForm):
    class Meta:
        model = MissingChild
        fields = ['name', 'age', 'gender', 'image', 'date_missing', 'place_of_birth', 'last_seen', 'guardian_name', 'guardian_contact']

def __init__(self, *args, **kwargs):
        super(MissingChildForm, self).__init__(*args, **kwargs)
        self.fields['last_seen'].widget.attrs.update({'placeholder': 'Place last seen'})