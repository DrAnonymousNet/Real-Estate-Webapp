# Generated by Django 4.0.3 on 2022-04-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realEstate', '0006_remove_house_amenity_house_amenity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='no_of_bathroom',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Bathroom'),
        ),
        migrations.AddField(
            model_name='house',
            name='no_of_plots',
            field=models.IntegerField(blank=True, default=2, verbose_name='Plots'),
        ),
        migrations.AlterField(
            model_name='land',
            name='no_of_plots',
            field=models.IntegerField(blank=True, default=2, verbose_name='Plots'),
        ),
    ]