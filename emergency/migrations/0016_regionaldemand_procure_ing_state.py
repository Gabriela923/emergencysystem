# Generated by Django 4.0.1 on 2022-04-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0015_regionaldemand_procurement_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionaldemand',
            name='procure_ing_state',
            field=models.CharField(choices=[('采购成功', '采购成功'), ('采购失败', '采购失败')], default='未填写', max_length=8, verbose_name='采购部门采购状态'),
        ),
    ]
