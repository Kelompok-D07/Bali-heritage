# Generated by Django 5.1.2 on 2024-10-25 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0006_remove_restaurant_review_product_restaurant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(default=1, upload_to='restaurant_logo/'),
            preserve_default=False,
        ),
    ]
