# Generated by Django 2.1.3 on 2018-12-14 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_run_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawhtml',
            name='data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
