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
 [动图](https://s2.ax1x.com/2019/05/15/E7GJ2D.gif)
![](https://s2.ax1x.com/2019/05/15/E7GJ2D.gif)
- 个人信息页面（修改个人信息，头像）
![](https://s2.ax1x.com/2019/05/15/E71158.gif)
- 忘记密码
![](https://s2.ax1x.com/2019/05/15/E71ha6.gif)
### 发表话题
- 发布话题
![](https://s2.ax1x.com/2019/05/15/E71Kbt.gif)
- 发表评论
![](https://s2.ax1x.com/2019/05/15/E71V8e.gif)
- 最近话题，回复，评论(采用了celery存储话题信息，避免因大量查询数据库操作增加服务器负担)
![](https://s2.ax1x.com/2019/05/15/E71jdP.gif)
### 管理员界面
- 管理员界面(有权限认证，只有管理员可查看)
![](https://s2.ax1x.com/2019/05/15/E71TRe.gif)