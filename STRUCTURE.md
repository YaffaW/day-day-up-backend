app/
  ├── main.py              # 应用入口
  ├── database.py          # 数据库连接和配置
  ├── models/              # 数据库模型
  │   ├── __init__.py      # 模型模块入口
  │   ├── user.py          # 用户数据模型
  │   └── task.py          # 任务和时间安排数据模型
  ├── schemas/             # Pydantic模型
  │   ├── user.py          # 用户请求/响应模型
  │   └── task.py          # 任务请求/响应模型
  ├── routers/             # API路由
  │   ├── users.py         # 用户相关路由
  │   └── tasks.py         # 任务相关路由
  └── utils/               # 工具函数
      └── security.py      # 安全相关工具

# 项目结构说明

## app/main.py
- FastAPI应用实例
- 中间件配置（CORS等）
- 路由注册
- 健康检查端点

## app/database.py
- 数据库连接配置
- SQLAlchemy引擎设置
- 会话工厂创建
- 数据库依赖项

## app/models/
### app/models/user.py
- User数据模型定义
- 用户表结构

### app/models/task.py
- Task任务数据模型
- ScheduleRecord时间安排记录模型
- 枚举类型定义

### app/models/__init__.py
- 导入所有模型类

## app/schemas/
### app/schemas/user.py
- 用户相关的Pydantic模型
- 请求/响应数据验证

### app/schemas/task.py
- 任务相关的Pydantic模型
- 包括任务和时间安排的请求/响应模型

## app/routers/
### app/routers/users.py
- 用户相关API端点
- 用户CRUD操作实现

### app/routers/tasks.py
- 任务相关API端点
- 任务CRUD操作
- 时间安排查询与自动生成功能

## app/utils/security.py
- 密码加密/验证工具
- 安全相关函数

## 环境配置
- .env.example - 环境变量示例
- requirements.txt - 项目依赖
- STRUCTURE.md - 项目结构说明

## 运行
- main.py - 应用启动脚本

## 启动项目
1. 安装依赖: pip install -r requirements.txt
2. 配置数据库连接: 复制 .env.example 为 .env 并填入正确值
3. 启动服务: python main.py