# Generated by Django 4.0.1 on 2022-04-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0027_trucksdeploy_td_sup_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trucks',
            name='truck_type',
            field=models.CharField(choices=[('2轴车', '2轴车'), ('3轴车', '3轴车'), ('4轴车', '4轴车'), ('5轴车', '5轴车'), ('6轴车', '6轴车')], default='未填写', max_length=8, verbose_name='货车型号'),
        ),
        migrations.AlterField(
            model_name='trucksdeploy',
            name='td_type',
            field=models.CharField(choices=[('2轴车/17吨', '2轴车/17吨'), ('3轴车/25吨', '3轴车/25吨'), ('4轴车/35吨', '4轴车/35吨'), ('5轴车/43吨', '5轴车/43吨'), ('6轴车/49吨', '6轴车/49吨')], default='未填写', max_length=8, verbose_name='货车型号'),
        ),
    ]