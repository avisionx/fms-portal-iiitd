# Generated by Django 3.1.7 on 2021-04-05 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_complaintcategories_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationChoices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
