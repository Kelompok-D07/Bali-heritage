# Generated by Django 5.1.2 on 2024-10-27 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaliLoka_stories', '0003_alter_storiesentry_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storiesentry',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
