# Generated by Django 2.1.7 on 2019-02-21 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageface', '0004_auto_20190217_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
    ]
