from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
import re


class UserAuth(MiddlewareMixin):

    def process_request(self, request):
        # 登录认证白名单
        white_list = [reverse('login'), reverse('register'), '/admin/*',
                      ]
        request_path = request.path
        if request_path in white_list:
            return
        is_login = request.session.get('is_login', None)
        if not is_login:
            return redirect('login')

        # 权限认证白名单
        white_permission_list = [reverse('index'), '/admin/*', reverse('regional_situation'),
                                 reverse('permission'), reverse('templates'), reverse('system_info'),
                                 reverse('de_info')]
        if request_path in white_permission_list:
            return

        permissions_list = request.session.get('permissions_list', None)
        for reg in permissions_list:
            if str(request_path).strip('/').split('/')[0] == 'admin':
                return
            path = str(request_path).strip('/').split('/')[1]
            if path in reg['permissions__url']:
                return
        else:
            return redirect('permission')
