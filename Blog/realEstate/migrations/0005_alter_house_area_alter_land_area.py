# Generated by Django 4.0.3 on 2022-04-01 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realEstate', '0004_remove_house_location_remove_land_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='area',
            field=models.CharField(blank=True, default='Tanke', max_length=50),
        ),
        migrations.AlterField(
            model_name='land',
            name='area',
            field=models.CharField(blank=True, default='Tanke', max_length=50),
        ),
    ]
