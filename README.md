# Django 用户认证系统

## 项目简介

这是一个基于 Django 5.2.5 构建的完整用户认证系统演示项目，实现了用户登录、登出、权限控制等核心功能。

## 功能特性

- ✅ **用户认证**：基于 Django 内置认证系统
- ✅ **安全控制**：@login_required 装饰器保护敏感页面
- ✅ **会话管理**：自动处理用户会话状态
- ✅ **响应式界面**：现代化的前端设计
- ✅ **消息提示**：用户友好的操作反馈
- ✅ **中文界面**：完整的中文本地化

## 技术栈

- **后端框架**：Django 5.2.5
- **数据库**：SQLite（开发环境）
- **前端**：HTML5 + CSS3 + Django Templates
- **Python 版本**：3.11+

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/pnwnq/Django.git
cd django-auth-system

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库初始化

```bash
# 执行数据库迁移
python manage.py migrate

# 创建管理员账户
python manage.py createsuperuser
```

### 4. 启动服务

```bash
python manage.py runserver
```

访问：http://127.0.0.1:8000/

## 项目结构

```
django-auth-system/
├── auth_system/          # 项目配置
│   ├── settings.py       # Django设置
│   ├── urls.py          # 主路由配置
│   └── wsgi.py          # WSGI配置
├── accounts/            # 认证应用
│   ├── views.py         # 视图逻辑
│   ├── urls.py          # 应用路由
│   └── apps.py          # 应用配置
├── templates/           # 模板文件
│   ├── base.html        # 基础模板
│   └── accounts/        # 认证相关模板
├── requirements.txt     # 依赖列表
└── manage.py           # Django管理脚本
```

## 核心功能说明

### 用户认证流程

1. **未登录访问** → 自动重定向到登录页面
2. **登录验证** → Django 内置认证机制验证
3. **登录成功** → 重定向到仪表板或原访问页面
4. **权限控制** → @login_required 保护敏感页面

### 安全特性

- CSRF 保护防止跨站请求伪造
- 密码哈希存储，不明文保存
- 会话管理和自动过期
- SQL 注入防护（Django ORM）

## 部署说明

### 生产环境配置

1. 修改 `settings.py`：

   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']

   # 使用更安全的数据库
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           # 其他配置...
       }
   }
   ```

2. 设置环境变量：

   ```bash
   export SECRET_KEY="your-secret-key"
   export DEBUG=False
   ```

3. 收集静态文件：
   ```bash
   python manage.py collectstatic
   ```

## 测试账户

为了方便测试，系统包含以下测试账户：

- **用户名**：admin
- **密码**：Admin123!

## 功能测试流程

### 权限控制演示

1. **测试未登录访问受保护页面**：
   - 访问 http://127.0.0.1:8000/
   - 在登录页面点击"🛡️ 测试受保护页面"按钮
   - 系统将自动重定向回登录页面（演示权限拦截）

2. **测试正常登录流程**：
   - 使用测试账户登录
   - 成功后进入用户仪表板
   - 查看权限控制演示成功提示

3. **测试登出功能**：
   - 在仪表板点击"🚪 安全退出"
   - 系统清除会话并重定向到登录页面
   - 再次尝试访问 `/dashboard/` 将被重定向到登录页面

## 技术亮点

### 🔐 Django 内置认证系统
- 使用 Django 的 `django.contrib.auth` 模块
- `authenticate()` 和 `login()` 函数处理用户验证
- `@login_required` 装饰器实现权限控制

### 🛡️ 安全机制
- **Session 管理**：基于 Cookie 的会话状态维护
- **CSRF 保护**：防止跨站请求伪造攻击
- **密码安全**：使用 Django 内置的密码哈希算法
- **XSS 防护**：Cookie 设置 HttpOnly 标志

### 🧪 自动化测试
项目包含完整的单元测试套件：

```bash
# 运行测试
python manage.py test accounts
```

测试覆盖：
- 未登录用户访问受保护页面的拦截
- 用户登录流程的完整验证
- 登出后会话清除的验证

### 📱 响应式设计
- 现代化的渐变色彩设计
- 移动端友好的响应式布局
- 平滑的动画过渡效果

## 开发指南

### 添加新功能

1. 在 `accounts/views.py` 中添加视图函数
2. 在 `accounts/urls.py` 中配置路由
3. 创建对应的模板文件
4. 编写相应的单元测试

### 自定义样式

模板文件位于 `templates/` 目录，可以直接修改 CSS 样式或添加 JavaScript 功能。

## 常见问题

**Q: 忘记管理员密码怎么办？**
A: 运行 `python manage.py createsuperuser` 创建新的管理员账户

**Q: 如何修改登录后的重定向页面？**
A: 修改 `settings.py` 中的 `LOGIN_REDIRECT_URL` 设置

**Q: 如何添加邮箱验证功能？**
A: 可以集成 `django-allauth` 或自行实现邮箱验证逻辑

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

MIT License

---

**注意**：这是一个演示项目，生产环境使用前请进行充分的安全审计和性能优化。
