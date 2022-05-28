from django.db import models
from multiselectfield import MultiSelectField
from rbac.models import Users


supplies_type_choices = (
        ('防护用品类', '防护用品类'),
        ('生命救助类', '生命救助类'),
        ('生命支持类', '生命支持类'),
        ('临时食宿类', '临时食宿类'),
        ('污染清理类', '污染清理类'),
        ('器材工具类', '器材工具类'),
        ('工程材料类', '工程材料类'),
        ('医疗用品类', '医疗用品类'),
)

supplies_info_choices = (
        ('京东本地仓', '京东本地仓'),
        ('天猫国际仓', '天猫国际仓'),
        ('天猫超市仓', '天猫超市仓'),
        ('巴迪高企业', '巴迪高企业'),
        ('哈拿户外企业', '哈拿户外企业'),
        ('麦德里企业', '麦德里企业'),
        ('甜橙商贸企业', '甜橙商贸企业'),
        ('亿家老小医疗器械企业', '亿家老小医疗器械企业'),
        ('迪立家居企业', '迪立家居企业'),
        ('碧之道企业', '碧之道企业'),
        ('雅艺企业', '雅艺企业'),
        ('蓝均医疗用品企业', '蓝均医疗用品企业'),
        ('蓝均医疗用品企业', '蓝均医疗用品企业'),
        ('益舒净企业', '益舒净企业'),
        ('益舒净企业', '益舒净企业'),
        ('罗兰企业', '罗兰企业'),
        ('怡宝企业', '怡宝企业'),
        ('哇哈哈企业', '哇哈哈企业'),
        ('农夫山泉集团', '农夫山泉集团'),
        ('哇哈哈企业', '哇哈哈企业'),
        ('冰露企业', '冰露企业'),
        ('白象企业', '白象企业'),
        ('康师傅企业', '康师傅企业'),
        ('金龙鱼企业', '金龙鱼企业'),
        ('阿里健康企业', '阿里健康企业'),
        ('苏宁易购企业', '苏宁易购企业'),
        ('社会捐赠物资', '社会捐赠物资'),

    )

reg_info_choices = (
        ('平岩市', '平岩市'),
        ('清州市', '清州市'),
        ('安中市', '安中市'),
        ('辽山市', '辽山市'),
        ('东义市', '东义市'),
    )

det_set_choices = (
    ('男', '男'),
    ('女', '女'),
)

nature_state_choices = (
    ('库存', '库存'),
    ('社会捐赠', '社会捐赠'),
)

state_choices = (
    ('未处理', '未处理'),
    ('已处理', '已处理'),
)

truck_state_choices = (
    ('空闲', '空闲'),
    ('忙碌', '忙碌'),
)

t_state_choices = (
    ('未处理', '未处理'),
    ('运输中', '运输中'),
    ('已签收入库', '已签收入库'),
)

transport_state_choices = (
    ('已到达', '已到达'),
    ('运输中', '运输中'),
)

result_state_choices = (
    ('未处理', '未处理'),
    ('通过', '通过'),
    ('否决', '否决'),
)

truck_type_choices = (
    ('2轴车', '2轴车'),
    ('3轴车', '3轴车'),
    ('4轴车', '4轴车'),
    ('5轴车', '5轴车'),
    ('6轴车', '6轴车'),
)

truck_load_choices = (
    ('17吨', '17吨'),
    ('25吨', '25吨'),
    ('35吨', '35吨'),
    ('43吨', '43吨'),
    ('49吨', '49吨'),
)

truck_driver_choices = (
    ('李强', '李强'),
    ('张虎', '张虎'),
    ('王守义', '王守义'),
    ('谢富贵', '谢富贵'),
    ('赵建国', '赵建国'),
)

truck_num_choices = (
    ('2轴车/17吨', '2轴车/17吨'),
    ('3轴车/25吨', '3轴车/25吨'),
    ('4轴车/35吨', '4轴车/35吨'),
    ('5轴车/43吨', '5轴车/43吨'),
    ('6轴车/49吨', '6轴车/49吨'),
)

procure_ing_state_choices = (
    ('采购成功', '采购成功'),
    ('采购失败', '采购失败'),
)

ware_state_choices = (
    ('平岩仓', '平岩仓'),
    ('东义仓', '东义仓'),
    ('清州仓', '清州仓'),
    ('安中仓', '安中仓'),
    ('安中仓', '安中仓'),
    ('珠山中心仓', '珠山中心仓'),
)


class UserInfo(Users):
    username = models.CharField(max_length=8, unique=True, null=False, default='未填写')
    number = models.CharField(max_length=24, unique=True, null=False, default='未填写')
    password = models.CharField(max_length=64, null=False, default='未填写')
    is_active = models.BinaryField(default=True)
    detailedInfo = models.OneToOneField(to='DetailedInfo', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username


class EmergencySupplies(models.Model):
    supplies_name = models.CharField('物资名称', max_length=64, unique=True)
    supplies_price = models.FloatField('物资价格')
    supplies_quantity = models.IntegerField('物资数量')
    supplies_unit = models.CharField('物资单位', default='kg', max_length=16)
    supplies_info = models.CharField('供应商信息', choices=supplies_info_choices, max_length=32, default='fulltime')
    supplies_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')
    image = models.OneToOneField(to_field='image_name', to='Image', on_delete=models.CASCADE)
    txt_path = models.CharField('文件路径', max_length=64, default='D:\PycharmProjects\emergencysystem\static', unique=True)

    def __str__(self):
        return self.supplies_name


class Image(models.Model):
    image_name = models.CharField("图片名称", max_length=128, unique=True)
    image_type = models.CharField('图片类型', max_length=16)
    image_path = models.CharField('图片路径', max_length=64)
    image_base = models.BinaryField('图片编码')

    def __str__(self):
        return self.image_name


class News(models.Model):
    news_info = models.CharField('新闻信息', max_length=128, default='空')
    news_herf = models.CharField("新闻链接", max_length=256, default='http')

    def __str__(self):
        return self.news_info


class Department(models.Model):
    department_name = models.CharField('部门名称', max_length=8, unique=True, default='空')
    department_message = models.CharField('部门信息', max_length=1024, default='空')

    def __str__(self):
        return self.department_name


class DetailedInfo(models.Model):
    det_name = models.CharField("姓名", max_length=8, unique=True, default='空')
    det_set = models.CharField('性别', choices=det_set_choices, max_length=4, default='fulltime')
    det_age = models.IntegerField('年龄', default=1)
    det_ph = models.CharField('电话', max_length=20, default='123')
    det_number = models.CharField('工号', max_length=16, default='DF')
    det_address = models.CharField('地址', max_length=24, default='浙江')
    department = models.ForeignKey(to_field='department_name', to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.det_name


class EpidemicSituation(models.Model):
    region_name = models.CharField('地区', max_length=16, default='未填写')
    number = models.IntegerField('地区人数', default=0)
    infections_number = models.IntegerField('感染人数',  default=0)
    infections_proportion = models.FloatField('比例', default=0)

    def __str__(self):
        return self.region_name


class RegionalDemand(models.Model):
    regional_name = models.CharField('地区名', choices=reg_info_choices, max_length=8, default='fulltime')
    supplies_name = models.CharField('物资名称', max_length=16, unique=False, default='未填写')
    supplies_unit = models.CharField('物资单位', max_length=8, default='箱')
    supplies_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')
    sup_num = models.IntegerField('需求物资数', default=0)
    state = models.CharField("需求部门处理状态", choices=state_choices, max_length=8, default='未处理', )
    procurement_state = models.CharField("采购部门处理状态", choices=state_choices, max_length=8, default='未处理',)
    procure_ing_state = models.CharField("采购部门采购状态", choices=procure_ing_state_choices, max_length=8, default='未填写',)
    failure_why = models.CharField("采购失败原因", max_length=128, default='未填写',)
    sums = models.IntegerField("总价", default=0,)
    reimbursement = models.CharField("报销状态", choices=state_choices, default='未处理', max_length=4)
    result = models.CharField("处理结果", choices=result_state_choices, default='未处理', max_length=4)

    def __str__(self):
        return self.regional_name


class Deploy(models.Model):
    d_address = models.CharField('调配地区', max_length=4, choices=reg_info_choices, default='未选择')
    d_name = models.CharField('物资名称', max_length=16, default='未填写')
    d_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')
    d_number = models.IntegerField('调配物资数量', default=0)
    process_state = models.CharField('处理状态', choices=state_choices, max_length=6, default='未处理')


class Trucks(models.Model):
    truck_number = models.CharField("货车编号", max_length=16, default='未填写', unique=True)
    truck_type = models.CharField("货车型号", max_length=8, choices=truck_type_choices, default='未填写')
    truck_load = models.CharField("货车载重", max_length=8, choices=truck_load_choices, default='未填写')
    truck_driver = models.CharField("货车司机", max_length=8, choices=truck_driver_choices, default='未填写')
    truck_state = models.CharField("货车状态", max_length=8, choices=truck_state_choices, default='空闲')

    def __str__(self):
        return self.truck_type


class TrucksDeploy(models.Model):
    td_address = models.CharField('调配地区', max_length=16, default='未填写')
    td_name = models.CharField('物资名称', max_length=16, default='未填写')
    td_sup_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')
    td_number = models.IntegerField('调配物资数量', default=0)
    td_card = models.CharField("货车编号", max_length=16, default='未填写', )
    td_type = models.CharField("货车型号", max_length=8, choices=truck_num_choices, default='未填写')
    td_con = models.CharField("发车情况", max_length=8, choices=transport_state_choices, default='未发车')
    nature = models.CharField("物资性质", max_length=8, choices=nature_state_choices, default='库存')


class TrucksImage(models.Model):
    cost = models.IntegerField('报销费用', default=0)
    cause = models.CharField("报销原因", max_length=32, default='未填写', null=False)
    image_name = models.CharField("图片名称", max_length=128, unique=True)
    image_path = models.CharField('图片路径', max_length=64)
    status = models.CharField('报销结果', max_length=4, choices=result_state_choices, default='未处理')
    remark = models.CharField('备注', max_length=64, default='空')

    def __str__(self):
        return self.cause


class Warehouse(models.Model):
    warehouse_name = models.CharField('仓库名称', max_length=16, default='未填写')
    warehouse_img_path = models.CharField("仓库图片", max_length=32, default='D:/')
    warehouse_address = models.CharField("仓库地址", max_length=16, default='未填写')
    warehouse_scale = models.CharField("仓库规模", max_length=16, default='未填写')
    warehouse_date = models.DateTimeField('仓库建设日期', null=True, blank=True)
    warehouse_max_capacity = models.IntegerField("仓库最大容量(m³)", default=0)
    warehouse_surplus_capacity = models.IntegerField("仓库剩余容量(m³)", default=0)

    def __str__(self):
        return self.warehouse_name


class MaterialSupplier(models.Model):
    supplies_name = models.CharField('物资名称', max_length=64, unique=True)
    supplies_price = models.FloatField('物资价格')
    supplies_quantity = models.IntegerField('物资数量')
    supplies_img = models.CharField('图片路径', max_length=64, default='/img/mater/')
    supplies_info = models.CharField('供应商信息', choices=supplies_info_choices, max_length=32, default='fulltime')
    supplies_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')

    def __str__(self):
        return self.supplies_name


class PurchasingResults(models.Model):
    supplies_name = models.CharField('物资名称', max_length=64,)
    supplies_price = models.FloatField('物资价格')
    supplies_quantity = models.IntegerField('物资采购数量')
    supplies_info = models.CharField('供应商信息', choices=supplies_info_choices, max_length=32, default='fulltime')
    supplies_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')
    s_sum = models.IntegerField("总价")

    def __str__(self):
        return self.supplies_name


class SocialDonation (models.Model):
    supplies_name = models.CharField('物资名称', max_length=64, unique=True)
    supplies_quantity = models.IntegerField('物资数量')
    supplies_unit = models.CharField("物资单位", max_length=8, default='空')
    supplies_type = models.CharField('物资类型', choices=supplies_type_choices, max_length=32, default='fulltime')
    donor = models.CharField("捐赠者署名", max_length=32, default='未填写')
    deploy_state = models.CharField("调配状态", choices=state_choices, default='未处理', max_length=8)
    transportation_state = models.CharField("运输状态", choices=t_state_choices, default='未处理', max_length=8)

    def __str__(self):
        return self.supplies_name


class DeployWarehouse(models.Model):
    ware_name = models.CharField('仓库名', max_length=8, choices=ware_state_choices, default='空')
    sup_name = models.CharField('物资名称', max_length=8, default='请填写')
    sup_type = models.CharField('物资类型', max_length=8, default='空', choices=supplies_type_choices)
    deploy_number = models.IntegerField('调入数量', default=0)
    transportation_state = models.CharField("运输状态", choices=t_state_choices, default='未处理', max_length=8)

# Create your models here.
