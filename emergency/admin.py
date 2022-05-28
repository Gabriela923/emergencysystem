from django.contrib import admin
from rbac.models import Role, Permission
from emergency import models

# admin.site.register(models.Users)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(models.UserInfo)
admin.site.register(models.Department)
admin.site.register(models.DetailedInfo)
admin.site.register(models.News)
admin.site.register(models.EmergencySupplies)
admin.site.register(models.EpidemicSituation)
admin.site.register(models.RegionalDemand)
admin.site.register(models.Trucks)
admin.site.register(models.Warehouse)
admin.site.register(models.MaterialSupplier)


# Register your models here.
