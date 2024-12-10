# Generated by Django 5.1.3 on 2024-12-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_schoolprofile_initial_update_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolprofile',
            name='initial_update',
        ),
        migrations.AddField(
            model_name='schoolprofile',
            name='is_updatable',
            field=models.BooleanField(default=True),
        ),
    ]