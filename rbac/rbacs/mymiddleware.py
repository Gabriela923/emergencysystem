from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import (render, HttpResponse, redirect, reverse)
import re


class PermissionAuth(MiddlewareMixin):

    def process_request(self, request):

        # 登录认证白名单
        white_list = [reverse('login'), '/admin/*']
        request_path = request.path
        for i in white_list:
            if re.match(i, request_path):
                return
        is_login = request.session.get("is_login")
        if not is_login:
            return redirect('login')

        # 权限认证白名单
        white_permission_list = [reverse('index')]
        if request_path in white_permission_list:
            return

        permissions_list = request.session.get('permissions_list')
        for reg in permissions_list:
            reg = r"%s$" % reg['permissions__url']
            if re.match(reg, request_path):
                return
        else:
            return HttpResponse('无权限')