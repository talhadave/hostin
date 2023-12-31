# Generated by Django 4.2.5 on 2023-11-25 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_hostel_embedcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='Rooms/'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='core.hostel'),
        ),
    ]
