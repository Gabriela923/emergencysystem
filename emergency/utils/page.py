"""
分页组件，单独写成一个文件是为了防止视图函数中代码量过多
实现分页功能，上一页下一页跳转功能，当前页面颜色改变功能，实现页码自动跟随居中功能，
实现页码在第一页和最后一页时，上一页下一页图标处显示禁用图标及其链接为javascript:void(0)功能
"""
from django.utils.safestring import mark_safe  # 导入页面渲染模块，解决返回前端再渲染的操作
import re

class MyPageNation(object):

    def __init__(self, page_num, total_count, base_url, get_data=None, per_page_num=10, page_num_show=5, ):
        try:
            page_num = int(page_num)
        except ValueError:
            page_num = 1
        self.get_data = get_data
        self.page_num = page_num  # 当前页码数字 需要传参
        self.per_page_num = per_page_num  # 每页只显示数据条数 需要传参
        self.base_url = base_url  # 地址路径， 需要传参
        a, b = divmod(total_count, self.per_page_num)  # a是商 b是余数  total_count为数据总条数，需要传参
        if b:
            page_count = a + 1
        else:
            page_count = a
        self.page_count = page_count

        if page_num <= 0:
            page_num = 1
        elif page_num > page_count:
            page_num = page_count
        self.page_num_show = page_num_show  # 显示页码个数 需要传参
        half_show = self.page_num_show // 2
        if page_num - half_show <= 0:
            start_num = 1
            end_num = self.page_num_show + 1

        elif page_num + half_show > page_count:
            start_num = page_count - self.page_num_show + 1
            end_num = page_count + 1

        else:
            start_num = page_num - half_show
            end_num = page_num + half_show + 1

        if page_count < self.page_num_show:
            start_num = 1
            end_num = page_count + 1
        self.start_num = start_num
        self.end_num = end_num

    def start_data_num(self):
        return (self.page_num-1) * self.per_page_num

    def end_data_num(self):
        return self.page_num * self.per_page_num

    def page_html(self):
        page_count_range = range(self.start_num, self.end_num)
        page_html = ''
        page_pre_html = '<nav aria-label="Page navigation"><ul class="pagination">'
        first_page_html = '<li><a href="{1}?page={0}" aria-label="Previous">' \
                          '<span aria-hidden="true">首页</span></a></li>'.format(1, self.base_url)
        if self.page_num <= 1:
            pre_page = '<li class="disabled"><a href="javascript:void(0)" aria-label="Previous">' \
                       '<span aria-hidden="true">&laquo;</span></a></li>'
        else:
            pre_page = '<li><a href="{1}?{2}page={0}" aria-label="Previous">' \
                       '<span aria-hidden="true">&laquo;</span></a></li>'.format(self.page_num - 1, self.base_url,
        re.sub('page=\d+', '', self.get_data, ) if 'page=' in self.get_data+'&' else self.get_data+'&')

        page_html += page_pre_html + first_page_html + pre_page
        # 生成页码
        for i in page_count_range:
            if i == self.page_num:
                # page_html += '<li class="active"><a href="{1}?page={0}">{0}</a></li>'.format(i, self.base_url)
                page_html += '<li class="active"><a href="{1}?{3}page={0}">{2}</a></li>'.format(i, self.base_url, i,
                re.sub('page=\d+', '', self.get_data, ) if 'page=' in self.get_data+'&' else self.get_data+'&')
            else:
                # page_html += '<li><a href="{1}?page={0}">{0}</a></li>'.format(i, self.base_url)
                page_html += '<li><a href="{1}?{3}page={0}">{2}</a></li>'.format(i, self.base_url, i,
                re.sub('page=\d+', '', self.get_data, ) if 'page=' in self.get_data+'&' else self.get_data+'&')
        if self.page_num >= self.page_count:
            page_next_html = '<li class="disabled"><a href="javascript:void(0)" aria-label="Next">' \
                             '<span aria-hidden="true">&raquo;</span></a></li>'
        else:
            page_next_html = '<li><a href="{1}?{2}page={0}" aria-label="Next">' \
                             '<span aria-hidden="true">&raquo;</span></a></li>'.format(self.page_num + 1, self.base_url,
            re.sub('page=\d+', '', self.get_data, ) if 'page=' in self.get_data+'&' else self.get_data+'&')

        last_page_html = '<li><a href="{1}?{2}page={0}" aria-label="Previous">' \
                         '<span aria-hidden="true">尾页</span></a></li>'.format(self.page_count, self.base_url,
        re.sub('page=\d+', '', self.get_data, ) if 'page=' in self.get_data+'&' else self.get_data+'&')

        end_html = '</ul></nav>'

        page_html += page_next_html + last_page_html + end_html

        return mark_safe(page_html)