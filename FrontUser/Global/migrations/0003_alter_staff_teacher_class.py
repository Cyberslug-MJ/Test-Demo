# Generated by Django 5.1.3 on 2024-12-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Global', '0002_alter_subjects_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='teacher_class',
            field=models.ManyToManyField(related_name='teacher_class', to='Global.subclasses'),
        ),
    ]
