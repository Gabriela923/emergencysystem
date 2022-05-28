# Generated by Django 4.0.1 on 2022-04-14 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0025_trucks'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrucksDeploy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('td_name', models.CharField(default='未填写', max_length=16, verbose_name='物资名称')),
                ('td_number', models.IntegerField(default=0, verbose_name='调配物资数量')),
                ('td_card', models.CharField(default='未填写', max_length=16, verbose_name='货车编号')),
                ('td_type', models.CharField(choices=[('2轴车', '2轴车'), ('3轴车', '3轴车'), ('4轴车', '4轴车'), ('5轴车', '5轴车'), ('6轴车及以上', '6轴车及以上')], default='未填写', max_length=8, verbose_name='货车型号')),
            ],
        ),
        migrations.AlterField(
            model_name='trucks',
            name='truck_load',
            field=models.CharField(choices=[('17吨', '17吨'), ('25吨', '25吨'), ('35吨', '35吨'), ('43吨', '43吨'), ('49吨', '49吨')], default='未填写', max_length=8, verbose_name='货车载重'),
        ),
        migrations.AlterField(
            model_name='trucks',
            name='truck_number',
            field=models.CharField(default='未填写', max_length=16, unique=True, verbose_name='货车编号'),
        ),
    ]