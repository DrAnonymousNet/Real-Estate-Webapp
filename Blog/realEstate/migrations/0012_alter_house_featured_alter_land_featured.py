# Generated by Django 4.0.3 on 2022-04-05 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realEstate', '0011_alter_house_date_listed_alter_land_date_listed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='land',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]