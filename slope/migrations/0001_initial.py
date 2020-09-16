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
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Is open')),
                ('deadline', models.DateTimeField(verbose_name='Deadline')),
                ('ordered_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('is_inactive', models.BooleanField(default=False, verbose_name='Is inactive')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Slope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('lat', models.DecimalField(decimal_places=8, max_digits=10, verbose_name='Latitude')),
                ('lng', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Longitude')),
                ('address', models.CharField(max_length=254, verbose_name='Address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('is_inactive', models.BooleanField(default=False, verbose_name='Is inactive')),
                ('announced_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Announced at')),
                ('deadline', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Deadline for order fulfilment')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Company')),
                ('orders', models.ManyToManyField(related_name='orders', through='slope.Order', to='company.Company')),
            ],
            options={
                'verbose_name': 'Slope',
                'verbose_name_plural': 'Slopes',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='slope',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slope.slope', verbose_name='Slope'),
        ),
        migrations.CreateModel(
            name='ExpertImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=254, upload_to='images/slope/expert/%Y/%m/%d/', verbose_name='Image')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded at')),
                ('is_inactive', models.BooleanField(default=False, verbose_name='Is inactive')),
                ('slope', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slope.slope', verbose_name='Slope')),
            ],
            options={
                'verbose_name': 'Expert image',
                'verbose_name_plural': 'Expert images',
            },
        ),
        migrations.CreateModel(
            name='DModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=254, upload_to='files/models/%Y/%m/%d/', verbose_name='3D model')),
                ('generated_at', models.DateTimeField(auto_now_add=True, verbose_name='Generated at')),
                ('is_inactive', models.BooleanField(default=False, verbose_name='Is inactive')),
                ('slope', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slope.slope', verbose_name='Slope')),
            ],
            options={
                'verbose_name': '3D model',
                'verbose_name_plural': '3D models',
            },
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('slope', 'company')},
        ),
    ]