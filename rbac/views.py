from django.shortcuts import render
from django.views import View
from rbac import models
from emergency.views import tem_objs


def roles(request):
    print(tem_objs)

    return render(request, 'roles.html', {'tem_objs': tem_objs})
# Create your views here.
