# Generated by Django 4.0.1 on 2022-04-10 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0008_epidemicsituation_material'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='epidemicsituation',
            name='material',
        ),
        migrations.AddField(
            model_name='epidemicsituation',
            name='material',
            field=models.ManyToManyField(blank=True, null=True, to='emergency.MaterialRequirements'),
        ),
    ]