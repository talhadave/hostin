# Generated by Django 4.2.5 on 2023-12-03 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_rename_user_info_booking_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
