from django import forms
from .models import MissingChild

class MissingChildForm(forms.ModelForm):
    class Meta:
        model = MissingChild
        fields = ['name', 'age', 'gender', 'image', 'date_missing', 'place_of_birth', 'last_seen', 'guardian_name', 'guardian_contact']

    def __init__(self, *args, **kwargs):
        super(MissingChildForm, self).__init__(*args, **kwargs)
        
        # Set required attribute for specific fields
        self.fields['image'].required = True
        self.fields['gender'].required = True
        self.fields['last_seen'].required = True
        self.fields['date_missing'].required = True
        
        # Set required attribute for non-mandatory fields to False
        self.fields['name'].required = False
        self.fields['age'].required = False
        self.fields['place_of_birth'].required = False
        self.fields['guardian_name'].required = False
        self.fields['guardian_contact'].required = False

    # Add additional validation if needed
    def clean(self):
        cleaned_data = super().clean()
        
        # Perform custom validation here
        
        return cleaned_data
