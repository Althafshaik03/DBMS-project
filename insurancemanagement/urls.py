
from django.contrib import admin
from django.urls import path
from insurance import views
from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),


    path('customer/',include('customer.urls')),
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='insurance/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    
    path('adminlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-view-customer', views.admin_view_customer_view,name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),

    path('admin-category', views.admin_category_view,name='admin-category'),
    path('admin-view-category', views.admin_view_category_view,name='admin-view-category'),
    path('admin-update-category', views.admin_update_category_view,name='admin-update-category'),
    path('update-category/<int:pk>', views.update_category_view,name='update-category'),
    path('admin-add-category', views.admin_add_category_view,name='admin-add-category'),
    path('admin-delete-category', views.admin_delete_category_view,name='admin-delete-category'),
    path('delete-category/<int:pk>', views.delete_category_view,name='delete-category'),


    path('admin-policy', views.admin_policy_view,name='admin-policy'),
    path('admin-add-policy', views.admin_add_policy_view,name='admin-add-policy'),
    path('admin-view-policy', views.admin_view_policy_view,name='admin-view-policy'),
    path('admin-update-policy', views.admin_update_policy_view,name='admin-update-policy'),
    path('update-policy/<int:pk>', views.update_policy_view,name='update-policy'),
    path('admin-delete-policy', views.admin_delete_policy_view,name='admin-delete-policy'),
    path('delete-policy/<int:pk>', views.delete_policy_view,name='delete-policy'),

    path('admin-claim', views.admin_claim_view,name='admin-claim'),
    path('admin-add-claim', views.admin_add_claim_view,name='admin-add-claim'),
    path('admin-view-claim', views.admin_view_claim_view,name='admin-view-claim'),
    path('admin-update-claim', views.admin_update_claim_view,name='admin-update-claim'),
    path('update-claim/<int:pk>', views.update_claim_view,name='update-claim'),
    path('admin-delete-claim', views.admin_delete_claim_view,name='admin-delete-claim'),
    path('delete-claim/<int:pk>', views.delete_claim_view,name='delete-claim'),

    path('admin-view-policy-holder', views.admin_view_policy_holder_view,name='admin-view-policy-holder'),
    path('admin-view-approved-policy-holder', views.admin_view_approved_policy_holder_view,name='admin-view-approved-policy-holder'),
    path('admin-view-disapproved-policy-holder', views.admin_view_disapproved_policy_holder_view,name='admin-view-disapproved-policy-holder'),
    path('admin-view-waiting-policy-holder', views.admin_view_waiting_policy_holder_view,name='admin-view-waiting-policy-holder'),
    path('approve-request/<int:pk>', views.approve_policy_request_view,name='approve-request'),
    path('reject-request/<int:pk>', views.disapprove_policy_request_view,name='reject-request'),

    path('admin-view-claim-holder', views.admin_view_claim_holder_view,name='admin-view-claim-holder'),
    path('admin-view-approved-claim-holder', views.admin_view_approved_claim_holder_view,name='admin-view-approved-claim-holder'),
    path('admin-view-disapproved-claim-holder', views.admin_view_disapproved_claim_holder_view,name='admin-view-disapproved-claim-holder'),
    path('admin-view-waiting-claim-holder', views.admin_view_waiting_claim_holder_view,name='admin-view-waiting-claim-holder'),
    path('approve-request/<int:pk>', views.approve_claim_request_view,name='approve-request'),
    path('reject-request/<int:pk>', views.disapprove_claim_request_view,name='reject-request'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('update-question/<int:pk>', views.update_question_view,name='update-question'),

]
