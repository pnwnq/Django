from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    """
    用户认证系统的单元测试套件
    测试核心认证流程的正确性和安全性
    """
    def setUp(self):
        """
        测试环境初始化
        创建测试客户端和测试用户
        """
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_dashboard_access_unauthenticated(self):
        """
        测试未登录用户访问受保护页面
        验证@login_required装饰器的权限控制功能
        """
        print("\nRunning: test_dashboard_access_unauthenticated...")
        response = self.client.get(reverse('dashboard'))
        
        # 期望返回302状态码（重定向）
        self.assertEqual(response.status_code, 302, "未登录访问dashboard应返回302")
        
        # 验证重定向到登录页面
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard')}", 
                             msg_prefix="未登录访问dashboard应重定向到登录页")
        print("PASSED: Unauthenticated user was correctly redirected.")

    def test_successful_login_and_dashboard_access(self):
        """
        测试用户登录流程和授权访问
        验证正确凭据能够成功登录并访问受保护页面
        """
        print("\nRunning: test_successful_login_and_dashboard_access...")
        # 尝试登录
        login_response = self.client.post(reverse('accounts:login'), {
            'username': self.username,
            'password': self.password,
        })
        
        # 登录成功后，应该重定向到仪表板
        self.assertRedirects(login_response, reverse('dashboard'), 
                             msg_prefix="成功登录后应重定向到dashboard")

        # 登录后访问仪表板
        dashboard_response = self.client.get(reverse('dashboard'))
        
        # 验证返回200状态码（成功）
        self.assertEqual(dashboard_response.status_code, 200, "登录后访问dashboard应返回200")
        
        # 验证页面内容包含用户信息
        self.assertContains(dashboard_response, f"欢迎回来，{self.username}", 
                            msg_prefix="dashboard页面应包含欢迎信息")
        print("PASSED: User successfully logged in and accessed dashboard.")

    def test_logout_and_session_destruction(self):
        """
        测试用户登出和会话管理
        验证登出后会话被正确销毁，权限控制重新生效
        """
        print("\nRunning: test_logout_and_session_destruction...")
        # 首先，让用户登录
        self.client.login(username=self.username, password=self.password)
        
        # 然后，执行登出操作
        logout_response = self.client.get(reverse('accounts:logout'))
        
        # 登出后应该重定向到登录页
        self.assertRedirects(logout_response, reverse('accounts:login'),
                             msg_prefix="登出后应重定向到登录页")
                             
        # 登出后，再次尝试访问仪表板
        dashboard_response_after_logout = self.client.get(reverse('dashboard'))
        
        # 期望被再次重定向
        self.assertEqual(dashboard_response_after_logout.status_code, 302, "登出后访问dashboard应返回302")
        self.assertIn(reverse('accounts:login'), dashboard_response_after_logout.url,
                      "登出后访问dashboard应重定向到登录页")
        print("PASSED: User successfully logged out and session was destroyed.")
