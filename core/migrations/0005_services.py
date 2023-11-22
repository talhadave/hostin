# Generated by Django 4.2.5 on 2023-11-13 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_room_number_rooms_room_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hostel')),
            ],
        ),
    ]