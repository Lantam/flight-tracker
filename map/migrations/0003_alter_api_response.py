# Generated by Django 4.2.5 on 2023-09-09 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_alter_api_aircraft_icao_alter_api_airline_icao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='response',
            field=models.JSONField(null=True),
        ),
    ]