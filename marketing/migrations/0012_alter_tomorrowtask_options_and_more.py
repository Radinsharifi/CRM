import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0011_callreminder_tomorrowtask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tomorrowtask',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='tomorrowtask',
            name='task_type',
        ),
        migrations.RemoveField(
            model_name='tomorrowtask',
            name='notes',
        ),
        migrations.AddField(
            model_name='tomorrowtask',
            name='bill_of_lading_follow_ups',
            field=models.TextField(blank=True, verbose_name='پیگیری بارنامه'),
        ),
        migrations.AddField(
            model_name='tomorrowtask',
            name='rate_inquiry_follow_ups',
            field=models.TextField(blank=True, verbose_name='پیگیری استعلام نرخ دهی'),
        ),
        migrations.AddField(
            model_name='tomorrowtask',
            name='existing_customer_follow_ups',
            field=models.ManyToManyField(blank=True, related_name='existing_customer_tomorrow_tasks', to='marketing.customer', verbose_name='لیست پیگیری مشتری قدیمی'),
        ),
        migrations.AddField(
            model_name='tomorrowtask',
            name='new_customer_follow_ups',
            field=models.ManyToManyField(blank=True, related_name='new_customer_tomorrow_tasks', to='marketing.customer', verbose_name='لیست پیگیری مشتری جدید'),
        ),
        migrations.AlterModelOptions(
            name='tomorrowtask',
            options={'ordering': ['is_completed', '-created_at'], 'verbose_name': 'کار فردا', 'verbose_name_plural': 'کارهای فردا'},
        ),
    ]