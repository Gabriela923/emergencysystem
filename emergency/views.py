import os

from django.shortcuts import (
    render, redirect, HttpResponse
)
from django.views import View
from emergency import models
from django import forms
from emergency.utils.hashlib_func import md
from emergency.utils.per_mess import per_mess
from emergency.utils.page import MyPageNation
from django.conf import settings
from multiselectfield.forms.fields import MultiSelectFormField
import re
from django.forms import widgets as wid
from django.db.models import Q

tem_objs = models.Department.objects.all()
count_list = list(range(1, 31))


# 注册功能Form组件
class RegisterForm(forms.Form):
    """
    主要用于规定字段规则，字段样式，字段报错信息等
    """
    # 姓名字段
    username = forms.CharField(
        max_length=8,
        min_length=2,
        widget=forms.widgets.TextInput(attrs={'placeholder': '姓名', 'autocomplete': 'off'}),
        error_messages={
            'required': '姓名不能为空',
            'max_length': '姓名不能大于8位',
            'min_length': '姓名不能小于2位',
        }
    )
    # 工号字段
    number = forms.CharField(
        max_length=24,
        min_length=8,
        widget=forms.widgets.TextInput(attrs={'placeholder': '工号', 'autocomplete': 'off'}),
        error_messages={
            'required': '工号不能为空',
            'max_length': '工号不能大于24位',
            'min_length': '工号不能小于8位',
        }
    )
    # 密码字段
    password = forms.CharField(
        max_length=16,
        min_length=8,
        widget=forms.widgets.TextInput(attrs={'type': 'password', 'placeholder': '密码', 'autocomplete': 'off'}),
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码不能大于24位',
            'min_length': '密码不能小于8位',
        }
    )
    # 确认密码字段
    r_password = forms.CharField(
        max_length=16,
        min_length=8,
        widget=forms.widgets.TextInput(attrs={'type': 'password', 'placeholder': '确认密码', 'autocomplete': 'off'}),
        error_messages={
            'required': '确认密码不能为空',
            'max_length': '确认密码不能大于24位',
            'min_length': '确认密码不能小于8位',
        }
    )

    # 全局钩子
    def clean(self):
        """
        用于判定两次密码输入是否一致
        :return: 一致则返回这两个相同密码，否则添加错误信息
        """
        values = self.cleaned_data
        password = values.get('password')
        r_password = values.get('r_password')
        if password == r_password:
            return values
        else:
            self.add_error('r_password', '两次输入密码不一致')


# 注册功能视图函数
class RegisterView(View):
    """
    GET请求进入注册页面
    POST请求提交数据进行验证，如果通过验证，用户进入登录页面进行登录，验证失败则报错重新输入注册信息
    """
    # GET请求
    def get(self, request):
        register_form_obj = RegisterForm()
        return render(request, 'register.html', {'register_form_obj': register_form_obj})

    # POST请求
    def post(self, request):
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            print(register_form_obj.cleaned_data)
            register_form_obj.cleaned_data.pop('r_password')
            password = register_form_obj.cleaned_data.pop('password')
            password = md(password)
            register_form_obj.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(
                **register_form_obj.cleaned_data
            )
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form_obj': register_form_obj})


# 登录功能类
class LoginView(View):
    """
    GET请求进入登录页面
    POST请求提交数据进行验证，如果通过验证，用户进入主页面，验证失败则报错重新输入登录信息
    """
    # GET请求
    def get(self, request):
        return render(request, 'login.html')

    # POST请求
    def post(self, request):
        uname = request.POST.get('uname')
        nub = request.POST.get('nub')
        pw = request.POST.get('pw')
        user_obj = models.UserInfo.objects.filter(username=uname, number=nub, password=md(pw)).first()
        if user_obj:
            request.session['is_login'] = True
            request.session['username'] = uname
            permissions_list = user_obj.roles.values('permissions__url', 'permissions__title',
                                                     'permissions__icon', 'permissions__is_menu').distinct()
            menu_list = []
            for permissions in permissions_list:
                is_menu = permissions['permissions__is_menu']
                print(is_menu)
                if is_menu is True:
                    menu_list.append(permissions)
            request.session['permissions_list'] = list(permissions_list)
            request.session['menu_list'] = list(menu_list)
            return redirect('index')

        else:
            return render(request, 'login.html', {'error': '请检查您的姓名、工号、密码是否正确'})


def index(request):
    news_objs = models.News.objects.all()[: 10]
    news_two_objs = models.News.objects.all()[10: 20]
    per_id = per_mess(request)
    return render(request, 'index.html', {'news_objs': news_objs, 'per_id': per_id, 'tem_objs': tem_objs,
                                          'news_two_objs': news_two_objs})


def templates(request):
    per_id = per_mess(request)
    return render(request, 'systemtemplate.html', {'tem_objs': tem_objs, 'per_id': per_id})


def supplies_info(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    print(sf, kw)
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.EmergencySupplies.objects.filter(q_objs)
    else:
        supplies_list = models.EmergencySupplies.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'supplies_info.html', {'supplies_objs': supplies_objs,
                                                  'page_html': page_html,
                                                  'tem_objs': tem_objs,
                                                  'per_id': per_id})


class Supplies(forms.ModelForm):

    class Meta:
        model = models.EmergencySupplies
        fields = "__all__"
        exclude = ("txt_path",)

        error_messages = {
            'supplies_name': {'required': '不能为空',},
            'supplies_price': {'required': '不能为空'},
            'supplies_quantity': {'required': '不能为空'},
        }

        labels = {
            'image': '图片'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


class EditSupplies(forms.ModelForm):

    class Meta:
        model = models.EmergencySupplies
        fields = "__all__"
        exclude = ("txt_path", )

        error_messages = {
            'supplies_name': {'required': '不能为空',},
            'supplies_price': {'required': '不能为空'},
            'supplies_quantity': {'required': '不能为空'},
        }

        labels = {
            'image': '图片'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


def add_supplies(request):
    per_id = per_mess(request)
    if request.method == 'GET':
        per_id = per_mess(request)
        supplies_forms = Supplies()
        return render(request, 'add_supplies.html', {'supplies_forms': supplies_forms, 'per_id': per_id,
                                                     'tem_objs': tem_objs, })

    else:
        supplies_forms = Supplies(request.POST)
        number = request.POST.get('supplies_quantity')
        s_name = request.POST.get("supplies_name")
        price = request.POST.get('supplies_price')
        number, price = int(number), float(price)
        if number <= 0 or price <= 0:
            return HttpResponse("您的操作无效 ，因您输入的物资数或物资价格为0或负数")

        if supplies_forms.is_valid():
            supplies_forms.save()
            txt_base = r'D:\PycharmProjects\emergencysystem\static\text\{0}.txt'.format(s_name)
            with open(txt_base, 'w', encoding='utf-8') as f:
                f.write(str(number))
            models.EmergencySupplies.objects.filter(supplies_name=s_name).update(txt_path=txt_base)
            return redirect('add_supplies')

        else:
            return render(request, 'add_supplies.html', {'supplies_forms': supplies_forms, 'tem_objs': tem_objs,
                                                         'per_id': per_id})


def delete_supplies(request, supplies_id):
        models.EmergencySupplies.objects.filter(id=supplies_id).delete()
        txt_base = models.EmergencySupplies.objects.get(id=supplies_id).txt_path
        os.remove(txt_base)
        return redirect('supplies_info')


def view_supplies(request, supplies_id):
    per_id = per_mess(request)
    view_obj = models.EmergencySupplies.objects.filter(id=supplies_id).first()
    view_img_obj = '/img/supplies_img/{0}'.format(view_obj.image.image_path)
    print(view_obj.id)
    return render(request, 'view_supplies.html', {'view_obj': view_obj, 'view_img_obj': view_img_obj, 'per_id': per_id,
                                                  'tem_objs': tem_objs, })


def edit_supplies(request, supplies_id):
    edit_obj = models.EmergencySupplies.objects.filter(id=supplies_id).first()
    if request.method == "GET":
        per_id = per_mess(request)
        supplies_forms = EditSupplies(instance=edit_obj)
        return render(request, 'edit_supplies.html', {'supplies_forms': supplies_forms, 'per_id': per_id, 'tem_objs': tem_objs, })

    else:
        supplies_forms = EditSupplies(request.POST, instance=edit_obj)
        number = request.POST.get('supplies_quantity')
        price = request.POST.get('supplies_price')
        number, price = int(number), float(price)
        if number <= 0 or price <= 0:
            return HttpResponse("您的操作无效 ，因您输入的物资数或物资价格为0或负数")
        if supplies_forms.is_valid():
            supplies_forms.save()
            txt_base = models.EmergencySupplies.objects.get(id=supplies_id).txt_path
            with open(txt_base, 'a', encoding='utf-8') as f:
                f.write(','+str(number))
            return redirect('supplies_info')
        else:
            return render(request, 'edit_supplies.html', {'supplies_forms': supplies_forms})


def upload_pictures(request):
    if request.method == 'GET':
        per_id = per_mess(request)
        return render(request, 'upload_pictures.html', {'per_id': per_id, 'tem_objs': tem_objs, })
    else:
        photo = request.FILES.get('photo', '')
        photo_data = photo.read()
        photo_name = photo.name.split('.')[0]
        photo_type = photo.name.split('.')[1]
        photo_path = photo.name
        print(photo_path)
        models.Image.objects.create(image_name=photo_name, image_type=photo_type, image_base=photo_data,
                                    image_path=photo_path,)
        with open(r"D:\PycharmProjects\emergencysystem\static\img\supplies_img\{0}".format(photo.name), 'wb') as f:
            f.write(photo_data)

        return redirect('upload_pictures')


def images(request):
    per_id = per_mess(request)
    img = models.Image.objects.filter(id=1).values('image_base')
    for i in img:
        with open(r"C:\Users\86153\Desktop\img\new.jpg", 'wb') as f:
            f.write(i['image_base'])
        # print(i['image_base'].decode())
    return render(request, 'images.html', {'per_id': per_id})


def add_news(request):
    per_id = per_mess(request)
    if request.method == 'GET':
        return render(request, 'add_news.html', {'per_id': per_id, 'tem_objs': tem_objs, })
    else:
        news_info = request.POST.get('info', '')
        print(news_info)
        models.News.objects.create(news_info=news_info)
        return redirect('add_news')


def department(request, department_id):
    per_id = per_mess(request)
    dep_objs = models.Department.objects.filter(id=department_id).first()
    return render(request, 'department.html', {'dep_objs': dep_objs, 'per_id': per_id, 'tem_objs': tem_objs, })


def personal_info(request, per_id):
    per_objs = models.UserInfo.objects.filter(id=per_id).first()
    per_objs = per_objs.detailedInfo
    return render(request, 'personal_info.html', {'per_id': per_id, 'per_objs': per_objs, 'tem_objs': tem_objs, })


class EditPer(forms.ModelForm):
    class Meta:
        model = models.DetailedInfo
        fields = "__all__"
        exclude = ('department', 'det_number', 'det_name')

        error_messages = {
            'supplies_name': {'required': '不能为空',},
            'supplies_price': {'required': '不能为空'},
            'supplies_quantity': {'required': '不能为空'},
        }

        labels = {
            'image': '图片'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


def edit_per(request, per_id):
    edit_obj = models.UserInfo.objects.filter(id=per_id).first()
    edit_obj = edit_obj.detailedInfo
    print(edit_obj)
    if request.method == 'GET':
        supplies_forms = EditPer(instance=edit_obj)
        return render(request, 'edit_per.html', {"per_id": per_id, 'tem_objs': tem_objs, 'supplies_forms': supplies_forms})
    else:
        edit_forms = EditPer(request.POST, instance=edit_obj)
        if edit_forms.is_valid():
            edit_forms.save()
            return redirect('index')
        else:
            render(request, 'edit_per.html', {'edit_forms': edit_forms, 'per_id': per_id})


def regional_situation(request):
    per_id = per_mess(request)
    reg_objs = models.EpidemicSituation.objects.all()
    num_count, in_number, = 0, 0
    for i in reg_objs:
        num_count += i.number
        in_number += i.infections_number
    pro_num = round(in_number/num_count, 5) * 1000
    return render(request, 'regional_situation.html', {"per_id": per_id, 'tem_objs': tem_objs, 'reg_objs': reg_objs,
                                                       'num_count': num_count,
                                                       'in_number': in_number,
                                                       'pro_num': pro_num,
                                                       })


class EpidemicSi(forms.ModelForm):

    class Meta:
        model = models.RegionalDemand
        fields = "__all__"
        exclude = ('state', 'procurement_state', 'procure_ing_state', 'failure_why', 'sums', 'reimbursement', 'result', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


def demand(request):
    per_id = per_mess(request)
    if request.method == 'GET':
        supplies_forms = EpidemicSi()
        return render(request, 'demand.html', {"per_id": per_id, 'tem_objs': tem_objs,
                                               'supplies_forms': supplies_forms})
    else:
        supplies_forms = EpidemicSi(request.POST)
        number = request.POST.get('sup_num')
        number = int(number)
        if number <= 0:
            return HttpResponse("您的操作无效 ，因您输入的需求物资数为0或负数")
        if supplies_forms.is_valid():
            supplies_forms.save()
            return redirect('demand')

        else:
            return render(request, 'demand.html', {'supplies_forms': supplies_forms,
                                                   "per_id": per_id, 'tem_objs': tem_objs, })


def agree(request):
    # 拿到当前页面页码
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='未处理').count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='未处理').reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'agree.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def through(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).update(state='已处理')
    return redirect('agree')


def delete_sup(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).delete()
    return redirect('agree')


def procurement(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='已处理', procurement_state='未处理').count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='已处理', procurement_state='未处理').reverse()[
                    page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'procurement.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def procurement_through(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).update(procurement_state='已处理')
    return redirect('procurement')


def procurement_delete_sup(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).delete()
    return redirect('procurement')


def procure_ing(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='未填写').count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='未填写').reverse()[
                    page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'procure_ing.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def successful(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).update(procure_ing_state='采购成功')
    return redirect('procure_ing')


def failure(request, sup_id):
    if request.method == 'GET':
        per_id = per_mess(request)
        # models.RegionalDemand.objects.filter(id=sup_id).delete()
        return render(request, 'failure_why.html', {'per_id': per_id,
                                                    'sup_id': sup_id,
                                                    'tem_objs': tem_objs})
    else:
        why = request.POST.get("why")
        models.RegionalDemand.objects.filter(id=sup_id).update(failure_why=why, procure_ing_state='采购失败')
        return redirect('procure_ing')


def successful_procure(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='采购成功').count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='采购成功').reverse()[
                    page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'successful_procure.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def failure_procure(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='采购失败').count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='采购失败').reverse()[
                    page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'failure_procure.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def procurement_claim_expense(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='采购成功').count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='已处理', procurement_state='已处理', procure_ing_state='采购成功').reverse()[
                    page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'procurement_claim_expense.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def calculate(request, sup_id):
    if request.method == 'GET':
        per_id = per_mess(request)
        return render(request, 'calculate.html', {'tem_objs': tem_objs, 'per_id': per_id})
    else:
        units = int(request.POST.get('unit'))
        sup_nums = models.RegionalDemand.objects.get(id=sup_id).sup_num
        su = units * sup_nums
        print(su)
        models.RegionalDemand.objects.filter(id=sup_id).update(sums=su)
        return redirect('procurement_claim_expense')


def finance(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.RegionalDemand.objects.filter(q_objs)
    else:
        supplies_list = models.RegionalDemand.objects.all()
    supplies_count = supplies_list.filter(state='已处理', procurement_state='已处理',procure_ing_state='采购成功',
                                         reimbursement='未处理', sums__gt=0).count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.filter(state='已处理', procurement_state='已处理',procure_ing_state='采购成功',
                                         reimbursement='未处理', sums__gt=0).reverse()[
                    page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'finance.html', {
        'supplies_objs': supplies_objs,
        'page_html': page_html,
        'tem_objs': tem_objs,
        'per_id': per_id
    })


def finance_agree(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).update(reimbursement='已处理', result='通过')
    return redirect('finance')


def finance_filed(request, sup_id):
    models.RegionalDemand.objects.filter(id=sup_id).update(reimbursement='已处理', result='否决')
    return redirect('finance')


def deploy(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.EmergencySupplies.objects.filter(q_objs)
    else:
        supplies_list = models.EmergencySupplies.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'deploy.html', {'supplies_objs': supplies_objs, 'page_html': page_html, 'tem_objs': tem_objs,
                                           'per_id': per_id})


class Deployment(forms.ModelForm):

    class Meta:
        model = models.Deploy
        fields = "__all__"
        exclude = ('d_name', 'process_state', 'transport_state', 'd_type', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


def deploy_info(request, sup_id):
    per_id = per_mess(request)
    if request.method == 'GET':
        supplies_forms = Deployment()
        return render(request, 'deploy_info.html', {"per_id": per_id, 'tem_objs': tem_objs,
                                                    'supplies_forms': supplies_forms})

    else:
        de_address = request.POST.get('d_address')
        de_number = request.POST.get('d_number')
        s_number = models.EmergencySupplies.objects.get(id=sup_id).supplies_quantity
        s_int_number = int(s_number)
        de_int_number = int(de_number)
        if de_int_number <= 0:
            return HttpResponse("错误！您输入的数量为0或负数")
        if s_int_number - de_int_number >= 0:
            difference_value = s_int_number - de_int_number
            models.EmergencySupplies.objects.filter(id=sup_id).update(supplies_quantity=difference_value)
            de_name = models.EmergencySupplies.objects.get(id=sup_id).supplies_name
            de_type = models.EmergencySupplies.objects.get(id=sup_id).supplies_type
            models.Deploy.objects.create(d_address=de_address, d_number=de_number, d_name=de_name,
                                         d_type=de_type)
            txt_base = models.EmergencySupplies.objects.get(id=sup_id).txt_path
            with open(txt_base, 'a', encoding='utf-8') as f:
                f.write(',' + str(difference_value))
            return redirect('deploy')
        else:
            return redirect('error_message')


def transport(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.Deploy.objects.filter(q_objs)
    else:
        supplies_list = models.Deploy.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'transport.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                              'tem_objs': tem_objs,
                                              'per_id': per_id})


def trucks(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.Trucks.objects.filter(q_objs)
    else:
        supplies_list = models.Trucks.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    truck_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'trucks.html', {'truck_objs': truck_objs, 'page_html': page_html, 'tem_objs': tem_objs,
                                           'per_id': per_id})


class TruckDep(forms.ModelForm):

    class Meta:
        model = models.TrucksDeploy
        fields = "__all__"
        exclude = ('td_name', 'td_sup_type', 'td_number', 'td_type', 'td_con', 'nature', 'td_address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


def allocation(request, sup_id):
    per_id = per_mess(request)
    if request.method == 'GET':
        supplies_forms = TruckDep()
        return render(request, 'allocation.html', {"per_id": per_id, 'tem_objs': tem_objs,
                                                   'supplies_forms': supplies_forms})
    else:
        td_card = request.POST.get("td_card")
        if models.Trucks.objects.get(truck_number=td_card).truck_state == '忙碌':
            return HttpResponse("该车辆处于忙碌状态，请选择别的车辆")
        t_address = models.Deploy.objects.get(id=sup_id).d_address
        sup_name = models.Deploy.objects.get(id=sup_id).d_name
        t_type = models.Trucks.objects.get(truck_number=td_card).truck_type
        sup_type = models.Deploy.objects.get(id=sup_id).d_type
        sup_number = models.Deploy.objects.get(id=sup_id).d_number
        models.Deploy.objects.filter(id=sup_id).update(process_state='已处理')
        t_num = models.Trucks.objects.get(truck_number=td_card).truck_number
        models.TrucksDeploy.objects.create(td_name=sup_name, td_sup_type=sup_type, td_number=sup_number,
                                           td_card=t_num, td_type=t_type, td_address=t_address)
        return redirect('allocation_results')


def allocation_donation(request, sup_id):
    per_id = per_mess(request)
    if request.method == 'GET':
        supplies_forms = TruckDep()
        return render(request, 'allocation_donation.html', {"per_id": per_id, 'tem_objs': tem_objs,
                                                   'supplies_forms': supplies_forms})
    else:
        td_card = request.POST.get("td_card")
        if models.Trucks.objects.get(truck_number=td_card).truck_state == '忙碌':
            return HttpResponse("该车辆处于忙碌状态，请选择别的车辆")
        t_address = models.DeployWarehouse.objects.get(id=sup_id).ware_name
        sup_name = models.DeployWarehouse.objects.get(id=sup_id).sup_name
        t_type = models.Trucks.objects.get(truck_number=td_card).truck_type
        sup_type = models.DeployWarehouse.objects.get(id=sup_id).sup_type
        sup_number = models.DeployWarehouse.objects.get(id=sup_id).deploy_number
        models.DeployWarehouse.objects.filter(id=sup_id).update(transportation_state='运输中')
        t_num = models.Trucks.objects.get(truck_number=td_card).truck_number
        models.TrucksDeploy.objects.create(td_name=sup_name, td_sup_type=sup_type, td_number=sup_number,
                                           td_card=t_num, td_type=t_type, td_address=t_address, nature='社会捐赠')
        return redirect('allocation_results')

def allocation_results(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.TrucksDeploy.objects.filter(q_objs)
    else:
        supplies_list = models.TrucksDeploy.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    truck_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'allocation_results.html', {'truck_objs': truck_objs, 'page_html': page_html,
                                                       'tem_objs': tem_objs, 'per_id': per_id})


def depart(request, sup_id):
    models.TrucksDeploy.objects.filter(id=sup_id).update(td_con='运输中')
    return redirect('allocation_results')


def arrive(request, sup_id):
    models.TrucksDeploy.objects.filter(id=sup_id).update(td_con='已送达')
    return redirect('allocation_results')


def trucks_cost(request):
    if request.method == 'GET':
        per_id = per_mess(request)
        return render(request, 'trucks_cost.html', {'per_id': per_id, 'tem_objs': tem_objs, })
    else:
        cost = request.POST.get("cost")
        if int(cost) <= 0:
            return HttpResponse("您的操作无效，因为您输入的报销费用为0或者负数")
        cause = request.POST.get("cause")
        photo = request.FILES.get("ph", '')
        photo_data = photo.read()
        photo_name = photo.name.split('.')[0]
        photo_path = photo.name
        print(photo_path)
        models.TrucksImage.objects.create(image_name=photo_name, image_path=photo_path, cost=cost, cause=cause)
        with open(f"D:\PycharmProjects\emergencysystem\static\img\s_trucks_cost\{photo.name}", 'wb') as f:
            f.write(photo_data)

        return redirect('trucks_cost')


def truck_results(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.TrucksImage.objects.filter(q_objs)
    else:
        supplies_list = models.TrucksImage.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    truck_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'truck_results.html', {'truck_objs': truck_objs, 'page_html': page_html,
                                                  'tem_objs': tem_objs,
                                                  'per_id': per_id})


def reimbursement(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.TrucksImage.objects.filter(q_objs)
    else:
        supplies_list = models.TrucksImage.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    truck_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'reimbursement.html', {'truck_objs': truck_objs, 'page_html': page_html,
                                                  'tem_objs': tem_objs,
                                                  'per_id': per_id})


def cost_agree(request, sup_id):
    models.TrucksImage.objects.filter(id=sup_id).update(status='通过')
    models.TrucksImage.objects.filter(id=sup_id).update(remark='空')
    return redirect('reimbursement')


def cost_failure(request, sup_id):
    models.TrucksImage.objects.filter(id=sup_id).update(status='否决')
    models.TrucksImage.objects.filter(id=sup_id).update(remark='申请有误，请重新审核该报销申请后再次提交')
    return redirect('reimbursement')


def warehouse(request):
    per_id = per_mess(request)
    return render(request, 'warehouse.html', {'tem_objs': tem_objs, 'per_id': per_id})


def supplier(request):
    return render(request, 'supplier.html')


def abc(request):
    with open(r'D:\PycharmProjects\emergencysystem\static\text\1.txt', 'r', encoding='utf-8') as f:
        file_list = f.read().split(',')[-3:]
    return render(request, '1.html', {'file_list': file_list, 'count_list': count_list})


def material_supplier(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.MaterialSupplier.objects.filter(q_objs)
    else:
        supplies_list = models.MaterialSupplier.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'material_supplier.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                                      'tem_objs': tem_objs, 'per_id': per_id})


def purchasing_situation(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.PurchasingResults.objects.filter(q_objs)
    else:
        supplies_list = models.PurchasingResults.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'purchasing_situation.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                                         'tem_objs': tem_objs, 'per_id': per_id})


def mater_view(request, sup_id):
    per_id = per_mess(request)
    view_obj = models.MaterialSupplier.objects.filter(id=sup_id).first()
    return render(request, 'mater_view.html', {'view_obj': view_obj, 'per_id': per_id, 'tem_objs': tem_objs, })


def mater_buy(request, sup_id):
    if request.method == 'GET':
        per_id = per_mess(request)
        view_obj = models.MaterialSupplier.objects.filter(id=sup_id).first()
        return render(request, 'mater_buy.html', {'view_obj': view_obj, 'per_id': per_id, 'tem_objs': tem_objs, })
    else:
        num = request.POST.get("number")
        suss = int(num) * int(models.MaterialSupplier.objects.get(id=sup_id).supplies_price)
        s_name = models.MaterialSupplier.objects.get(id=sup_id).supplies_name
        s_type = models.MaterialSupplier.objects.get(id=sup_id).supplies_type
        s_price = models.MaterialSupplier.objects.get(id=sup_id).supplies_price
        s_info = models.MaterialSupplier.objects.get(id=sup_id).supplies_info
        s_quantity = int(num)
        number = models.MaterialSupplier.objects.get(id=sup_id).supplies_quantity
        number = int(number)
        if s_quantity > number or s_quantity <= 0:
            return HttpResponse("该物资库存不足或您输入的数量为0、负数")
        difference_value = number - s_quantity
        models.MaterialSupplier.objects.filter(id=sup_id).update(supplies_quantity=difference_value)
        models.PurchasingResults.objects.create(supplies_name=s_name, supplies_price=s_price, supplies_type=s_type,
                                                supplies_quantity=s_quantity, s_sum=suss, supplies_info=s_info)
        return redirect('material_supplier')


class SocialDonat(forms.ModelForm):

    class Meta:
        model = models.SocialDonation
        fields = "__all__"
        exclude = ('deploy_state', 'transportation_state', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


def social_donation(request):
    per_id = per_mess(request)
    if request.method == 'GET':
        supplies_forms = SocialDonat()
        return render(request, 'social_donation.html', {"per_id": per_id, 'tem_objs': tem_objs,
                                                        'supplies_forms': supplies_forms})

    else:
        s_name = request.POST.get('supplies_name')
        s_quantity = request.POST.get('supplies_quantity')
        s_unit = request.POST.get('supplies_unit')
        s_type = request.POST.get('supplies_type')
        s_donor = request.POST.get('donor')
        s_quantity = int(s_quantity)
        if s_quantity <= 0:
            return HttpResponse('您的操作无效，因输入的调配数量为0或负数')
        models.SocialDonation.objects.create(supplies_name=s_name, supplies_quantity=s_quantity, supplies_type=s_type,
                                             supplies_unit=s_unit, donor=s_donor)
        return redirect('social_donation')


def social_donation_warehouse(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.SocialDonation.objects.filter(q_objs)
    else:
        supplies_list = models.SocialDonation.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'social_donation_warehouse.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                                              'tem_objs': tem_objs, 'per_id': per_id})


def warehouse_capacity(request):
    per_id = per_mess(request)
    ware_objs = models.Warehouse.objects.all()
    return render(request, 'warehouse_capacity.html', {"per_id": per_id, 'tem_objs': tem_objs, 'ware_objs': ware_objs,
                                                       })


def error_message(request):
    return render(request, 'error_message.html',)


def error_message_s(request):
    return render(request, 'error_message_s.html',)


class DeployWare(forms.ModelForm):
    class Meta:
        model = models.DeployWarehouse
        fields = "__all__"
        exclude = ('transportation_state', 'sup_name', 'sup_type', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})


def donation_deploy(request, sup_id):
    per_id = per_mess(request)
    if request.method == 'GET':
        deploy_ware_objs = DeployWare()
        return render(request, 'donation_deploy.html', {"per_id": per_id, 'tem_objs': tem_objs,
                                                        'deploy_ware_objs': deploy_ware_objs})
    else:
        dn = request.POST.get("deploy_number")
        wn = request.POST.get("ware_name")
        dn = int(dn)
        if dn <= 0:
            return HttpResponse("输入物资为0或者负数")
        sq = int(models.SocialDonation.objects.get(id=sup_id).supplies_quantity)
        if dn > sq:
            return redirect('error_message_s')
        else:
            count = sq - dn
            with open(r'D:\PycharmProjects\emergencysystem\static\text\1.txt', 'a', encoding='utf-8') as f:
                f.write(','+str(count))
            models.SocialDonation.objects.filter(id=sup_id).update(supplies_quantity=count)
            s_name = models.SocialDonation.objects.get(id=sup_id).supplies_name
            s_type = models.SocialDonation.objects.get(id=sup_id).supplies_type
            models.DeployWarehouse.objects.create(ware_name=wn, sup_name=s_name, deploy_number=dn, sup_type=s_type)
            return redirect('de_ware')


def de_ware(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.DeployWarehouse.objects.filter(q_objs)
    else:
        supplies_list = models.DeployWarehouse.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'de_ware.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                            'tem_objs': tem_objs, 'per_id': per_id})


def demand_ware(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.Deploy.objects.filter(q_objs)
    else:
        supplies_list = models.Deploy.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'demand_ware.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                            'tem_objs': tem_objs, 'per_id': per_id})


def donation_deploy_ware(request):
    get_data = request.GET.urlencode()
    page_num = request.GET.get('page', 'none')  # 拿到当前页面页码
    sf = request.GET.get('search_field')
    kw = request.GET.get('kw')
    if kw:
        q_objs = Q()
        q_objs.children.append((sf, kw))
        supplies_list = models.DeployWarehouse.objects.filter(q_objs)
    else:
        supplies_list = models.DeployWarehouse.objects.all()
    supplies_count = supplies_list.count()
    per_page_num = settings.PER_PAGE_NUM
    page_num_show = settings.PAGE_NUM_SHOW
    base_url = request.path  # 访问当前路径
    page_obj = MyPageNation(page_num, supplies_count, base_url, get_data, per_page_num, page_num_show, )
    page_html = page_obj.page_html()
    per_id = per_mess(request)

    supplies_objs = supplies_list.reverse()[page_obj.start_data_num(): page_obj.end_data_num()]
    return render(request, 'donation_deploy_ware.html', {'supplies_objs': supplies_objs, 'page_html': page_html,
                                                'tem_objs': tem_objs, 'per_id': per_id})


def change_state(request, sup_id):
    state = models.Trucks.objects.get(id=sup_id).truck_state
    if state == '空闲':
        models.Trucks.objects.filter(id=sup_id).update(truck_state='忙碌')
        return redirect('trucks')
    else:
        models.Trucks.objects.filter(id=sup_id).update(truck_state='空闲')
        return redirect('trucks')


def echarts(request, view_id):
    per_id = per_mess(request)
    txt_base = models.EmergencySupplies.objects.get(id=view_id).txt_path
    with open(txt_base, 'r', encoding='utf-8') as f:
        file_list = f.read().split(',')[-30:]
    return render(request, 'echarts.html', {'tem_objs': tem_objs, 'per_id': per_id,
                                            'file_list': file_list, 'count_list': count_list})


def permission(request):
    return render(request, 'permission.html')


def system_info(request):
    per_id = per_mess(request)
    return render(request, 'system_info.html', {'tem_objs': tem_objs, 'per_id': per_id,})


def de_info(request):
    per_id = per_mess(request)
    return render(request, 'de_info.html', {'tem_objs': tem_objs, 'per_id': per_id,})
# Create your views here.

