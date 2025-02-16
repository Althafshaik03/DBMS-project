from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('customerclick', views.customerclick_view,name='customerclick'),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customerlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='customerlogin'),

    path('apply-policy', views.apply_policy_view,name='apply-policy'),
    path('apply-claim', views.apply_claim_view,name='apply-claim'),
    path('apply/<int:pk>', views.apply_view,name='apply'),
    path('apply-Claims/<int:pk>', views.apply_Claims_view,name='apply-Claims'),
    path('history', views.history_view,name='history'),
    path('claim_history', views.claim_history_view,name='claim_history'),

    path('ask-question', views.ask_question_view,name='ask-question'),
    path('question-history', views.question_history_view,name='question-history'),
    path('download-pdf/<int:customer_id>/', views.generate_pdf_report, name='download-pdf'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/recommend_policy/', views.recommend_policy, name='recommend_policy'),
]

