# Generated by Django 4.1.5 on 2023-01-28 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_alter_city_slug_alter_language_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='slug',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]