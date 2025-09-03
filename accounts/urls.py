from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 用户认证路由
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # 技术展示页面
    path('tech-demo/', views.tech_demo, name='tech_demo'),
]