from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # 验证用户凭据
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # 登录成功
            login(request, user)
            messages.success(request, f'欢迎回来，{user.username}！')
            
            # 重定向到原本想访问的页面，或默认仪表板
            next_page = request.GET.get('next', '/dashboard/')
            return redirect(next_page)
        else:
            # 登录失败
            messages.error(request, '用户名或密码错误，请重试。')
    
    return render(request, 'accounts/login.html')

def user_logout(request):
    """用户登出视图"""
    username = request.user.username if request.user.is_authenticated else "访客"
    logout(request)
    messages.success(request, f'{username}，您已成功退出系统。')
    return redirect('/accounts/login/')

@login_required
def dashboard(request):
    """用户仪表板 - 受保护的管理区域"""
    return render(request, 'accounts/dashboard.html', {
        'user': request.user,
        'title': '用户仪表板'
    })

@login_required
def tech_demo(request):
    """技术展示指南页面 - 展示项目技术深度"""
    return render(request, 'accounts/tech_demo.html', {
        'user': request.user,
        'session_key': request.session.session_key,
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'remote_addr': request.META.get('REMOTE_ADDR', ''),
    })

def home(request):
    """首页 - 智能导航到相应页面"""
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        return redirect('/accounts/login/')