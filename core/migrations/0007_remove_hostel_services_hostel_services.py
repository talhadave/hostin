# Generated by Django 4.2.5 on 2023-11-13 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_services_hostel_hostel_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostel',
            name='services',
        ),
        migrations.AddField(
            model_name='hostel',
            name='services',
            field=models.ManyToManyField(to='core.services', verbose_name='Services'),
        ),
    ]
