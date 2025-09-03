from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    """
    一个严谨的工程师，会用代码来捍卫自己系统的正确性。
    """
    def setUp(self):
        """
        在每个测试开始前，准备好我们的战场环境。
        创建一个测试客户端，和一个虚拟用户。
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
        **测试场景1：未授权访问 - 系统的第一道防线**
        
        验证：一个没有登录的用户，在尝试访问仪表板时，
        是否会被强制重定向到登录页面。
        这是权限控制的核心。
        """
        print("\nRunning: test_dashboard_access_unauthenticated...")
        response = self.client.get(reverse('dashboard'))
        
        # 我们期望服务器返回302状态码（重定向）
        self.assertEqual(response.status_code, 302, "未登录访问dashboard应返回302")
        
        # 我们期望它重定向到登录页面
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboard')}", 
                             msg_prefix="未登录访问dashboard应重定向到登录页")
        print("PASSED: Unauthenticated user was correctly redirected.")

    def test_successful_login_and_dashboard_access(self):
        """
        **测试场景2：成功登录与授权访问**
        
        验证：一个拥有正确凭据的用户，是否能成功登录，
        并随后能正常访问受保护的仪表板页面。
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

        # 现在，作为一个已登录用户，我们再次访问仪表板
        dashboard_response = self.client.get(reverse('dashboard'))
        
        # 我们期望服务器返回200状态码（成功）
        self.assertEqual(dashboard_response.status_code, 200, "登录后访问dashboard应返回200")
        
        # 我们可以检查页面内容，确认是正确的用户
        self.assertContains(dashboard_response, f"欢迎回来，{self.username}", 
                            msg_prefix="dashboard页面应包含欢迎信息")
        print("PASSED: User successfully logged in and accessed dashboard.")

    def test_logout_and_session_destruction(self):
        """
        **测试场景3：安全退出与会话销毁**
        
        验证：用户登出后，其会话是否被正确销毁，
        再次访问受保护页面时，是否会被再次拦截。
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
