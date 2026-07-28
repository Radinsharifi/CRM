from django.contrib import admin
from .models import Customer, CallRecord

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'phone_number')

@admin.register(CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    list_display = ('customer', 'contact_person', 'result', 'created_at')