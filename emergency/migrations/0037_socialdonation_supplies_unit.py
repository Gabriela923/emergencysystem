# Generated by Django 4.0.1 on 2022-04-19 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0036_socialdonation_alter_deploy_d_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialdonation',
            name='supplies_unit',
            field=models.CharField(default='空', max_length=8, verbose_name='物资单位'),
        ),
    ]
