# Generated by Django 2.1.3 on 2018-12-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20181126_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='sailing',
            name='sailing_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
