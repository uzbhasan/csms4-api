# Generated by Django 3.1.1 on 2020-09-16 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('role', models.CharField(choices=[('SA', 'System administrator'), ('AD', 'Administrator'), ('GM', "Company's general manager"), ('MA', "Company's manager"), ('EM', "Company's employee")], max_length=40, verbose_name='Role')),
                ('first_name', models.CharField(max_length=150, verbose_name='First name')),
                ('last_name', models.CharField(max_length=150, verbose_name='Last name')),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
                ('last_login', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Last login')),
                ('phone_number', models.CharField(blank=True, default=None, max_length=45, null=True, verbose_name='Phone number')),
                ('avatar', models.ImageField(blank=True, default=None, max_length=254, null=True, upload_to='images/account/%Y/%m/%d/', verbose_name='Avatar')),
                ('company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
    ]
