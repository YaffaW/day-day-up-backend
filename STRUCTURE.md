app/
  ├── main.py          # 应用入口
  ├── database.py      # 数据库连接和配置
  ├── models/          # 数据库模型
  │   └── user.py
  ├── schemas/         # Pydantic模型
  │   └── user.py
  ├── routers/         # API路由
  │   └── users.py
  └── utils/           # 工具函数
      └── security.py

# 项目结构说明

## app/main.py
- FastAPI应用实例
- 中间件配置
- 路由注册
- 健康检查

## app/database.py
- 数据库连接配置
- SQLAlchemy引擎设置
- 会话管理

## app/models/user.py
- User数据模型定义
- 数据库表结构

## app/schemas/user.py
- Pydantic模型定义
- 请求/响应数据验证

## app/routers/users.py
- 用户相关API端点
- CRUD操作实现

## app/utils/security.py
- 密码加密/验证工具
- 安全相关函数

## 环境配置
- .env.example - 环境变量示例
- requirements.txt - 项目依赖

## 运行
- main.py - 应用启动脚本

## 启动项目
1. 安装依赖: pip install -r requirements.txt
2. 配置数据库连接: 复制 .env.example 为 .env 并填入正确值
3. 启动服务: python main.py