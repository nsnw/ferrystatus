# Generated by Django 2.1.3 on 2018-11-19 06:19

import data.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_sailing_sailing_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sailing',
            name='day_of_week',
            field=models.CharField(blank=True, choices=[(data.models.DayOfWeek('Monday'), 'Monday'), (data.models.DayOfWeek('Tuesday'), 'Tuesday'), (data.models.DayOfWeek('Wednesday'), 'Wednesday'), (data.models.DayOfWeek('Thursday'), 'Thursday'), (data.models.DayOfWeek('Friday'), 'Friday'), (data.models.DayOfWeek('Saturday'), 'Saturday'), (data.models.DayOfWeek('Sunday'), 'Sunday')], max_length=16, null=True),
        ),
    ]
