# Generated by Django 4.2.5 on 2023-11-13 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_remove_hostel_services_hostel_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel',
            name='ownerUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Hostels', to=settings.AUTH_USER_MODEL),
        ),
    ]
