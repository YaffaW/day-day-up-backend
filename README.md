# DayDayUp Backend

基于 FastAPI 和 PostgreSQL 的后端项目

## 项目结构

```
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
```

## 技术栈

- FastAPI: 现代高性能Web框架
- PostgreSQL: 关系型数据库
- SQLAlchemy: ORM
- Pydantic: 数据验证
- Uvicorn: ASGI服务器

## 安装和运行

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件并填入正确的数据库连接信息
   ```

3. 启动开发服务器：
   ```bash
   python main.py
   ```

4. 访问API文档：
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API端点

- GET / - 主页
- GET /health - 健康检查
- /api/v1/users/ - 用户相关API

## 环境变量

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT密钥
- `ALGORITHM`: 加密算法
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 访问令牌过期时间

## 数据库模型

当前包含用户模型，支持用户注册、登录、信息更新等功能。