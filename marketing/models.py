from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

def default_follow_up():
    return timezone.now().date() + timedelta(days=3)

class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام رابط اصلی")
    company_name = models.CharField(max_length=255, verbose_name="نام شرکت")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تماس")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.name})"

class CallRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='calls')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="ثبت شده توسط"
    )
    # Make these Optional so the form submits easily
    field_of_activity = models.CharField(max_length=255, blank=True, null=True, verbose_name="حوزه فعالیت")
    contact_person = models.CharField(max_length=255, verbose_name="شخص رابط") # Keep Required
    job_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="سمت")
    landline = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن ثابت")
    mobile = models.CharField(max_length=20, verbose_name="تلفن همراه") # Keep Required
    email_at_call = models.EmailField(blank=True, null=True, verbose_name="آدرس ایمیل")
    website = models.URLField(blank=True, null=True, verbose_name="وبسایت")
    acquisition_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="نحوه آشنایی")
    
    # Interaction Details
    result = models.CharField(max_length=255, verbose_name="نتیجه تماس")
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")
    follow_up_date = models.DateField(default=default_follow_up, verbose_name="تاریخ پیگیری")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']