# Generated by Django 4.2.5 on 2023-11-22 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_rename_user_profile_student'),
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='check_in_date',
            new_name='booking_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='check_out_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='student',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='User.student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='user_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
