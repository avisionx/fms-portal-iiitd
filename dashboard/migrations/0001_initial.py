# Generated by Django 3.1.7 on 2021-02-26 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0003_auto_20210226_2328'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(1, 'Others'), (2, 'Electricity'), (3, 'House Keeping')], default=1)),
                ('description', models.TextField(blank=True, default='')),
                ('location', models.IntegerField(choices=[(1, 'Others'), (2, 'Hostel'), (3, 'New Acad Block'), (4, 'Library')], default=1)),
                ('location_desc', models.CharField(max_length=100)),
                ('dt_time', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customer')),
            ],
        ),
    ]
