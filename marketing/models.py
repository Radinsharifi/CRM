from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

def default_follow_up():
    return timezone.now().date() + timedelta(days=3)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="دسته‌بندی")

    class Meta:
        ordering = ['name']
        verbose_name = "دسته‌بندی مشتری"
        verbose_name_plural = "دسته‌بندی‌های مشتریان"

    def __str__(self):
        return self.name

class Customer(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="نام نام خانوادگی")
    company_name = models.CharField(max_length=255, verbose_name="نام شرکت")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="دسته‌بندی"
    )
    insider = models.IntegerField(blank=True, null=True, verbose_name="داخلی")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="شماره تماس")
    province = models.CharField(max_length=100, blank=True, verbose_name="استان")
    city = models.CharField(max_length=100, blank=True, verbose_name="شهر")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    field_of_activity = models.CharField(max_length=255, blank=True, null=True, verbose_name="حوزه فعالیت")
    job_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="سمت")
    landline = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن ثابت")
    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن همراه")
    website = models.URLField(blank=True, null=True, verbose_name="وبسایت")
    acquisition_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="نحوه آشنایی")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="ثبت شده توسط"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.full_name})"

class CallRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='calls')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="ثبت شده توسط"
    )
    
    # Interaction Details
    result = models.TextField(max_length=2000, verbose_name="نتیجه تماس")
    duration_minutes = models.IntegerField(
        null=True,
        blank=False,
        default=0,
        verbose_name="مدت زمان مکالمه (دقیقه)"
    )
    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name="مدت زمان مکالمه (ثانیه)"
    )
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")
    follow_up_date = models.DateField(default=default_follow_up, verbose_name="تاریخ پیگیری")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CallReminder(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'زیاد'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='call_reminders',
        verbose_name='نام مشتری'
    )
    subject = models.CharField(max_length=255, verbose_name='موضوع پیگیری')
    follow_up_date = models.DateField(verbose_name='تاریخ پیگیری')
    follow_up_time = models.TimeField(verbose_name='ساعت پیگیری')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='اولویت ریمایندر'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ثبت شده توسط'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['follow_up_date', 'follow_up_time']
        verbose_name = 'یادآوری تماس'
        verbose_name_plural = 'یادآوری‌های تماس'

    def __str__(self):
        return f'{self.customer} - {self.subject}'


class TomorrowTask(models.Model):
    new_customer_follow_ups = models.ManyToManyField(
        Customer,
        blank=True,
        related_name='new_customer_tomorrow_tasks',
        verbose_name='لیست پیگیری مشتری جدید'
    )
    existing_customer_follow_ups = models.ManyToManyField(
        Customer,
        blank=True,
        related_name='existing_customer_tomorrow_tasks',
        verbose_name='لیست پیگیری مشتری قدیمی'
    )
    rate_inquiry_follow_ups = models.TextField(blank=True, verbose_name='پیگیری استعلام نرخ دهی')
    bill_of_lading_follow_ups = models.TextField(blank=True, verbose_name='پیگیری بارنامه')
    is_completed = models.BooleanField(default=False, verbose_name='انجام شده')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ثبت شده توسط'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_completed', '-created_at']
        verbose_name = 'کار فردا'
        verbose_name_plural = 'کارهای فردا'

    def __str__(self):
        return f'کار فردا #{self.pk}'