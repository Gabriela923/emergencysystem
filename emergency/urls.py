from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('index/', views.index, name='index'),
    path('templates/', views.templates, name='templates'),
    path('supplies_info/', views.supplies_info, name='supplies_info'),
    path('add_supplies/', views.add_supplies, name='add_supplies'),
    path('delete_supplies/?P<supplies_id>/', views.delete_supplies, name='delete_supplies'),
    path('edit_supplies/?P<supplies_id>/', views.edit_supplies, name='edit_supplies'),
    path('view_supplies/?P<supplies_id>/', views.view_supplies, name='view_supplies'),
    path('upload_pictures/', views.upload_pictures, name='upload_pictures'),
    path('images/', views.images, name='images'),
    path('add_news/', views.add_news, name='add_news'),
    path('department/?P<department_id>', views.department, name='department'),
    path('personal_info/?P<per_id>', views.personal_info, name='personal_info'),
    path('edit_per/?P<per_id>', views.edit_per, name='edit_per'),
    path('demand/', views.demand, name='demand'),
    path('supplier/', views.supplier, name='supplier'),
    path('regional_situation/', views.regional_situation, name='regional_situation'),
    path('agree/', views.agree, name='agree'),
    path('through/?P<sup_id>', views.through, name='through'),
    path('delete_sup/?P<sup_id>/', views.delete_sup, name='delete_sup'),
    path('procurement_through/?P<sup_id>', views.procurement_through, name='procurement_through'),
    path('procurement_delete_sup/?P<sup_id>/', views.procurement_delete_sup, name='procurement_delete_sup'),
    path('successful/?P<sup_id>', views.successful, name='successful'),
    path('failure/?P<sup_id>/', views.failure, name='failure'),
    path('procurement/', views.procurement, name='procurement'),
    path('procure_ing/', views.procure_ing, name='procure_ing'),
    path('successful_procure/', views.successful_procure, name='successful_procure'),
    path('finance/', views.finance, name='finance'),
    path('deploy/', views.deploy, name='deploy'),
    path('transport/', views.transport, name='transport'),
    path('trucks/', views.trucks, name='trucks'),
    path('failure_procure/', views.failure_procure, name='failure_procure'),
    path('trucks_cost/', views.trucks_cost, name='trucks_cost'),
    path('reimbursement/', views.reimbursement, name='reimbursement'),
    path('allocation_results/', views.allocation_results, name='allocation_results'),
    path('truck_results/', views.truck_results, name='truck_results'),
    path('warehouse/', views.warehouse, name='warehouse'),
    path('procurement_claim_expense/', views.procurement_claim_expense, name='procurement_claim_expense'),
    path('calculate/?P<sup_id>', views.calculate, name='calculate'),
    path('finance_agree/?P<sup_id>', views.finance_agree, name='finance_agree'),
    path('finance_filed/?P<sup_id>', views.finance_filed, name='finance_filed'),
    path('deploy_info/?P<sup_id>', views.deploy_info, name='deploy_info'),
    path('allocation/?P<sup_id>', views.allocation, name='allocation'),
    path('allocation_donation/?P<sup_id>', views.allocation_donation, name='allocation_donation'),
    path('depart/?P<sup_id>', views.depart, name='depart'),
    path('arrive/?P<sup_id>', views.arrive, name='arrive'),
    path('cost_agree/?P<sup_id>', views.cost_agree, name='cost_agree'),
    path('cost_failure/?P<sup_id>', views.cost_failure, name='cost_failure'),
    path('mater_view/?P<sup_id>', views.mater_view, name='mater_view'),
    path('mater_buy/?P<sup_id>', views.mater_buy, name='mater_buy'),
    path('donation_deploy/?P<sup_id>', views.donation_deploy, name='donation_deploy'),
    path('change_state/?P<sup_id>', views.change_state, name='change_state'),
    path('echarts/?P<view_id>', views.echarts, name='echarts'),
    path('abc/', views.abc, name='abc'),
    path('material_supplier/', views.material_supplier, name='material_supplier'),
    path('purchasing_situation/', views.purchasing_situation, name='purchasing_situation'),
    path('social_donation/', views.social_donation, name='social_donation'),
    path('social_donation_warehouse/', views.social_donation_warehouse, name='social_donation_warehouse'),
    path('warehouse_capacity/', views.warehouse_capacity, name='warehouse_capacity'),
    path('error_message/', views.error_message, name='error_message'),
    path('error_message_s/', views.error_message_s, name='error_message_s'),
    path('de_ware/', views.de_ware, name='de_ware'),
    path('demand_ware/', views.demand_ware, name='demand_ware'),
    path('donation_deploy_ware/', views.donation_deploy_ware, name='donation_deploy_ware'),
    path('permission/', views.permission, name='permission'),
    path('system_info/', views.system_info, name='system_info'),
    path('de_info/', views.de_info, name='de_info'),

]