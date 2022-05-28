# Generated by Django 4.0.1 on 2022-04-21 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0041_deploywarehouse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploywarehouse',
            name='sup_type',
            field=models.CharField(choices=[('防护用品类', '防护用品类'), ('生命救助类', '生命救助类'), ('生命支持类', '生命支持类'), ('临时食宿类', '临时食宿类'), ('污染清理类', '污染清理类'), ('器材工具类', '器材工具类'), ('工程材料类', '工程材料类'), ('医疗用品类', '医疗用品类')], default='空', max_length=8, verbose_name='物资名称'),
        ),
        migrations.AlterField(
            model_name='deploywarehouse',
            name='sup_name',
            field=models.CharField(default='请填写', max_length=8, verbose_name='物资名称'),
        ),
    ]