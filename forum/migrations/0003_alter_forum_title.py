# Generated by Django 5.1.2 on 2024-10-27 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_forum_recommendations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
