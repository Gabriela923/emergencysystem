# Generated by Django 4.0.1 on 2022-04-10 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0006_alter_epidemicsituation_infections_proportion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epidemicsituation',
            name='infections_number',
            field=models.IntegerField(default=0, verbose_name='感染人数'),
        ),
    ]
