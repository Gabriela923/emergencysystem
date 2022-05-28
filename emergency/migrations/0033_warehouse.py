# Generated by Django 4.0.1 on 2022-04-18 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0032_trucksimage_remark_trucksimage_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_name', models.CharField(default='未填写', max_length=16, verbose_name='仓库名称')),
                ('warehouse_img_path', models.CharField(default='D:/', max_length=32, verbose_name='仓库图片')),
                ('warehouse_address', models.CharField(default='未填写', max_length=16, verbose_name='仓库地址')),
                ('warehouse_scale', models.CharField(default='未填写', max_length=16, verbose_name='仓库规模')),
                ('warehouse_date', models.DateTimeField(blank=True, null=True, verbose_name='仓库建设日期')),
            ],
        ),
    ]
