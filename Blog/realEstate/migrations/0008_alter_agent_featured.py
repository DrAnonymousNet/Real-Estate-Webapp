# Generated by Django 4.0.3 on 2022-04-04 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realEstate', '0007_house_no_of_bathroom_house_no_of_plots_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='featured',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
