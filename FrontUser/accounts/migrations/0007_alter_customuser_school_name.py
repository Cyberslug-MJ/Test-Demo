# Generated by Django 5.1.3 on 2024-12-11 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customuser_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='school_name',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
