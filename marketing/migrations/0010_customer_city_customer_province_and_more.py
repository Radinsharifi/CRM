from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0009_category_callrecord_duration_minutes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=100, verbose_name='شهر'),
        ),
        migrations.AddField(
            model_name='customer',
            name='province',
            field=models.CharField(blank=True, max_length=100, verbose_name='استان'),
        ),
        migrations.AddField(
            model_name='callrecord',
            name='duration_seconds',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='مدت زمان مکالمه (ثانیه)'),
        ),
    ]