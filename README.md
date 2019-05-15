# hellofamily
## Web架构（MVC架构）
### 后端
- 采用Flask框架，配置flask_login用户登录状态，flask-wtform管理表单。
- 采用Redis作为缓存中间件，提高/topic/profile页面的访问性能。
- 采用Celery任务队列，处理发送邮件业务，提供顺畅的访问性能。

### 数据库
- 采用MySQLK数据库，并使用SQLAlchemy数据库ORM工具。

### 前端
- 采用了Bootstrap作为前端的css和js框架
- 编写话题采用了mditor.js提供markdown的编辑环境

## 主要业务
### 用户
- 登录注册（用户注册后，会发送一份激活邮件到邮箱，激活后，方可使用论坛大部分功能。）
- 
- 