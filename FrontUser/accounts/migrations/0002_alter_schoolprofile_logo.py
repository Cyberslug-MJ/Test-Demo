# Generated by Django 5.1.3 on 2024-12-09 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolprofile',
            name='logo',
            field=models.URLField(blank=True, default='https://my-bucket.s3.amazonaws.com/my-folder/my-image.jpg?AWSAccessKeyId=EXAMPLE&Expires=1672531199&Signature=abcdef', max_length=1000, verbose_name='logo'),
        ),
    ]