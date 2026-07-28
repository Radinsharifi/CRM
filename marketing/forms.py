from django import forms
from .models import CallRecord, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'name', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})

class CallRecordForm(forms.ModelForm):
    class Meta:
        model = CallRecord
        fields = [
            'customer', 'field_of_activity', 'contact_person', 
            'job_title', 'landline', 'mobile', 'email_at_call', 
            'website', 'acquisition_source', 'result', 'notes', 'follow_up_date'
        ]
        widgets = {
            'first_contact_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Apply Select class to dropdowns, Input class to others
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-input'})