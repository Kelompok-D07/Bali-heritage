# Generated by Django 5.1.2 on 2024-10-25 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0005_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='review',
        ),
        migrations.AddField(
            model_name='product',
            name='restaurant_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Homepage.restaurant'),
            preserve_default=False,
        ),
    ]