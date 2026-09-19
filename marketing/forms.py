from django import forms
from .models import CallRecord, CallReminder, Customer, TomorrowTask

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'company_name', 'full_name', 'category', 'province', 'city', 'phone_number', 'email',
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
            'customer', 'result', 'duration_minutes', 'duration_seconds', 'notes', 'follow_up_date'
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


class CallReminderForm(forms.ModelForm):
    class Meta:
        model = CallReminder
        fields = ['customer', 'subject', 'follow_up_date', 'follow_up_time', 'priority']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-select' if isinstance(field.widget, forms.Select) else 'form-input'})


class TomorrowTaskForm(forms.ModelForm):
    class Meta:
        model = TomorrowTask
        fields = [
            'new_customer_follow_ups', 'existing_customer_follow_ups',
            'rate_inquiry_follow_ups', 'bill_of_lading_follow_ups', 'is_completed'
        ]
        widgets = {
            'new_customer_follow_ups': forms.SelectMultiple(attrs={'class': 'customer-follow-up-select', 'size': 5}),
            'existing_customer_follow_ups': forms.SelectMultiple(attrs={'class': 'customer-follow-up-select', 'size': 5}),
            'rate_inquiry_follow_ups': forms.Textarea(attrs={'rows': 3}),
            'bill_of_lading_follow_ups': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-select' if isinstance(field.widget, forms.Select) else 'form-input'})