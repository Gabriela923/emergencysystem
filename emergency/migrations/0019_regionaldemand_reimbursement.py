# Generated by Django 4.0.1 on 2022-04-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0018_regionaldemand_sums'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionaldemand',
            name='reimbursement',
            field=models.CharField(choices=[('未处理', '未处理'), ('已处理', '已处理')], default='未处理', max_length=4, verbose_name='报销状态'),
        ),
    ]
