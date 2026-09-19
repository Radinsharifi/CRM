import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0010_customer_city_customer_province_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='موضوع پیگیری')),
                ('follow_up_date', models.DateField(verbose_name='تاریخ پیگیری')),
                ('follow_up_time', models.TimeField(verbose_name='ساعت پیگیری')),
                ('priority', models.CharField(choices=[('low', 'کم'), ('medium', 'متوسط'), ('high', 'زیاد')], default='medium', max_length=10, verbose_name='اولویت ریمایندر')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ثبت شده توسط')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_reminders', to='marketing.customer', verbose_name='نام مشتری')),
            ],
            options={
                'verbose_name': 'یادآوری تماس',
                'verbose_name_plural': 'یادآوری‌های تماس',
                'ordering': ['follow_up_date', 'follow_up_time'],
            },
        ),
        migrations.CreateModel(
            name='TomorrowTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(choices=[('new_customer', 'پیگیری مشتری جدید'), ('existing_customer', 'پیگیری مشتری قدیمی'), ('rate_inquiry', 'پیگیری استعلام نرخ دهی'), ('bill_of_lading', 'پیگیری بارنامه')], max_length=30, verbose_name='نوع پیگیری')),
                ('notes', models.TextField(blank=True, verbose_name='توضیحات')),
                ('is_completed', models.BooleanField(default=False, verbose_name='انجام شده')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='ثبت شده توسط')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tomorrow_tasks', to='marketing.customer', verbose_name='نام مشتری')),
            ],
            options={
                'verbose_name': 'کار فردا',
                'verbose_name_plural': 'کارهای فردا',
                'ordering': ['is_completed', '-created_at'],
            },
        ),
    ]