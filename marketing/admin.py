from django.contrib import admin
from .models import Category, Customer, CallRecord

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'full_name', 'category', 'phone_number', 'field_of_activity', 'created_by')

@admin.register(CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    list_display = ('customer', 'result', 'duration_minutes', 'created_at', 'created_by')