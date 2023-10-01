# Generated by Django 4.2.5 on 2023-09-25 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=10)),
                ('country_code', models.CharField(max_length=2, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('elevation', models.IntegerField(null=True)),
                ('head_direction', models.IntegerField(null=True)),
                ('airline_icao', models.CharField(max_length=3, null=True)),
                ('aircraft_icao', models.CharField(max_length=4, null=True)),
                ('departure_icao', models.CharField(max_length=4, null=True)),
                ('arrival_icao', models.CharField(max_length=4, null=True)),
                ('status', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(null=True)),
            ],
        ),
    ]