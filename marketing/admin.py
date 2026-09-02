from django.contrib import admin
from .models import Customer, CallRecord

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'full_name', 'phone_number', 'field_of_activity', 'created_by')

@admin.register(CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    list_display = ('customer', 'result', 'created_at', 'created_by')