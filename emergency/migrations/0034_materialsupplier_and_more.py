# Generated by Django 4.0.1 on 2022-04-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0033_warehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplies_name', models.CharField(max_length=64, unique=True, verbose_name='物资名称')),
                ('supplies_price', models.FloatField(verbose_name='物资价格')),
                ('supplies_quantity', models.IntegerField(verbose_name='物资数量')),
                ('supplies_img', models.CharField(default='/', max_length=64, verbose_name='图片路径')),
                ('supplies_info', models.CharField(choices=[('京东本地仓', '京东本地仓'), ('天猫国际仓', '天猫国际仓'), ('天猫超市仓', '天猫超市仓'), ('巴迪高企业', '巴迪高企业'), ('哈拿户外企业', '哈拿户外企业'), ('麦德里企业', '麦德里企业'), ('甜橙商贸企业', '甜橙商贸企业'), ('亿家老小医疗器械企业', '亿家老小医疗器械企业'), ('迪立家居企业', '迪立家居企业'), ('碧之道企业', '碧之道企业'), ('雅艺企业', '雅艺企业'), ('蓝均医疗用品企业', '蓝均医疗用品企业'), ('蓝均医疗用品企业', '蓝均医疗用品企业'), ('益舒净企业', '益舒净企业'), ('益舒净企业', '益舒净企业'), ('罗兰企业', '罗兰企业'), ('怡宝企业', '怡宝企业'), ('哇哈哈企业', '哇哈哈企业'), ('农夫山泉集团', '农夫山泉集团'), ('哇哈哈企业', '哇哈哈企业'), ('冰露企业', '冰露企业'), ('白象企业', '白象企业'), ('康师傅企业', '康师傅企业'), ('金龙鱼企业', '金龙鱼企业'), ('阿里健康企业', '阿里健康企业'), ('苏宁易购企业', '苏宁易购企业')], default='fulltime', max_length=32, verbose_name='供应商信息')),
                ('supplies_type', models.CharField(choices=[('食物', '食物'), ('防护', '防护'), ('水', '水'), ('日常用品', '日常用品')], default='fulltime', max_length=32, verbose_name='物资类型')),
            ],
        ),
        migrations.AlterField(
            model_name='emergencysupplies',
            name='supplies_info',
            field=models.CharField(choices=[('京东本地仓', '京东本地仓'), ('天猫国际仓', '天猫国际仓'), ('天猫超市仓', '天猫超市仓'), ('巴迪高企业', '巴迪高企业'), ('哈拿户外企业', '哈拿户外企业'), ('麦德里企业', '麦德里企业'), ('甜橙商贸企业', '甜橙商贸企业'), ('亿家老小医疗器械企业', '亿家老小医疗器械企业'), ('迪立家居企业', '迪立家居企业'), ('碧之道企业', '碧之道企业'), ('雅艺企业', '雅艺企业'), ('蓝均医疗用品企业', '蓝均医疗用品企业'), ('蓝均医疗用品企业', '蓝均医疗用品企业'), ('益舒净企业', '益舒净企业'), ('益舒净企业', '益舒净企业'), ('罗兰企业', '罗兰企业'), ('怡宝企业', '怡宝企业'), ('哇哈哈企业', '哇哈哈企业'), ('农夫山泉集团', '农夫山泉集团'), ('哇哈哈企业', '哇哈哈企业'), ('冰露企业', '冰露企业'), ('白象企业', '白象企业'), ('康师傅企业', '康师傅企业'), ('金龙鱼企业', '金龙鱼企业'), ('阿里健康企业', '阿里健康企业'), ('苏宁易购企业', '苏宁易购企业')], default='fulltime', max_length=32, verbose_name='供应商信息'),
        ),
    ]
