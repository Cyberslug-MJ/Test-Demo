# Generated by Django 5.1.3 on 2024-12-08 21:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(blank=True, max_length=60, unique=True, verbose_name='username')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Parent', 'Parent'), ('Student', 'Student'), ('Teacher', 'Teacher')], db_index=True, max_length=7)),
                ('school_name', models.CharField(blank=True, db_index=True, max_length=200, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, default='N/A', max_length=200, verbose_name='first_name')),
                ('last_name', models.CharField(blank=True, default='N/A', max_length=200, verbose_name='last_name')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'CustomUser',
                'verbose_name_plural': 'CustomUser',
            },
        ),
        migrations.CreateModel(
            name='SchoolProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='school', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='school profile')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('logo', models.ImageField(blank=True, upload_to='logo/', verbose_name='logo')),
                ('address', models.CharField(blank=True, max_length=255)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('theme', models.CharField(blank=True, max_length=7)),
                ('tier', models.CharField(choices=[('Tier 1', 'Tier 1'), ('Tier 2', 'Tier 2'), ('Tier 3', 'Tier 3')], default='Tier 1', max_length=6, verbose_name='tier')),
                ('subdomain_url', models.URLField(blank=True, default='http://www.yourschool.domain.com')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
                ('profile_picture', models.ImageField(blank=True, default='images/profile_pic.webp', upload_to='images')),
                ('firstname', models.CharField(blank=True, max_length=100)),
                ('lastname', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.CharField(blank=True, default='N/A', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'User Profile',
            },
        ),
    ]