# Generated by Django 4.2.5 on 2023-11-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rooms_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='embedCode',
            field=models.TextField(blank=True, null=True),
        ),
    ]