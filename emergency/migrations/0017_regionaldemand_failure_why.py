# Generated by Django 4.0.1 on 2022-04-11 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0016_regionaldemand_procure_ing_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionaldemand',
            name='failure_why',
            field=models.CharField(default='未填写', max_length=128, verbose_name='采购失败原因'),
        ),
    ]
