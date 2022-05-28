from django.db import models


class Permission(models.Model):
    url = models.CharField('路径权限', max_length=64)
    title = models.CharField('权限信息', max_length=16)
    # menus = models.ForeignKey('Menu', null=True, blank=True)
    is_menu = models.BooleanField(default=False)
    icon = models.CharField('图标', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=16)
    permissions = models.ManyToManyField(to='Permission')

    def __str__(self):
        return self.name


class Users(models.Model):
    roles = models.ManyToManyField(to=Role)

    class Meta:
        abstract = True  # 执行数据库迁移指令时候，不会将这个类生成表

# Create your models here.
