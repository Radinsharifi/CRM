from django import forms
from .models import CallRecord, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'company_name', 'phone_number', 'email',
            'field_of_activity', 'job_title', 'landline', 'mobile',
            'website', 'acquisition_source'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})

class CallRecordForm(forms.ModelForm):
    class Meta:
        model = CallRecord
        fields = [
            'customer', 'result', 'notes', 'follow_up_date'
        ]
        widgets = {
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