# DayDayUp Backend

基于 FastAPI 和 PostgreSQL 的后端项目，支持任务管理和时间表安排功能。

## 项目结构

```
app/
  ├── main.py              # 应用入口
  ├── database.py          # 数据库连接和配置
  ├── models/              # 数据库模型
  │   ├── __init__.py
  │   ├── user.py          # 用户模型
  │   └── task.py          # 任务和时间安排模型
  ├── schemas/             # Pydantic模型
  │   ├── user.py          # 用户模型定义
  │   └── task.py          # 任务模型定义
  ├── routers/             # API路由
  │   ├── users.py         # 用户相关路由
  │   └── tasks.py         # 任务相关路由
  └── utils/               # 工具函数
      └── security.py      # 安全相关工具
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
   # 或使用 uvicorn 直接运行
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

4. 访问API文档：
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

## API端点

### 任务管理相关
- `GET /api/v1/tasks/` - 获取任务列表
- `POST /api/v1/tasks/` - 创建任务
- `PUT /api/v1/tasks/{task_id}` - 更新任务
- `DELETE /api/v1/tasks/{task_id}` - 删除任务（软删除）

### 时间表安排相关
- `POST /api/v1/schedule/` - 获取时间表数据（支持单日或时间段查询）

### 用户相关
- `GET /api/v1/users/` - 获取用户列表
- `POST /api/v1/users/` - 创建用户
- `PUT /api/v1/users/{user_id}` - 更新用户信息
- `DELETE /api/v1/users/{user_id}` - 删除用户

### 系统相关
- `GET /` - 主页
- `GET /health` - 健康检查

## 环境变量

- `DATABASE_URL`: 数据库连接字符串（默认: postgresql://postgres@localhost/daydayup）

## 数据库模型

### 用户模型 (users)
支持用户注册、登录、信息更新等基本用户管理功能。

### 任务模型 (tasks)
- `id`: 任务唯一标识
- `type`: 任务类型 (regular, recurring, progress)
- `title`: 任务标题
- `theme_color`: 任务颜色
- `progress`: 进度 (0-100)
- `is_completed`: 完成状态
- `description`: 任务描述
- `repeat_weekdays`: 重复星期配置 (JSON格式)
- `start_date/end_date`: 任务起止日期
- `start_time/end_time`: 任务默认时间
- `status`: 任务状态 (active, deleted)

### 时间安排记录模型 (schedule_records)
- `id`: 记录唯一标识
- `task_id`: 关联任务ID (临时任务可为空)
- `date`: 安排日期
- `start_time/end_time`: 开始/结束时间
- `title/theme_color`: 任务标题和颜色 (冗余字段)
- `is_completed`: 完成状态
- `description`: 任务描述
- `status`: 记录状态 (active, deleted)

## 核心功能

### 任务管理
- 获取任务列表
- 创建新任务
- 编辑任务信息
- 删除任务（软删除，对历史记录无影响，仅对未来安排生效）

### 时间表安排
- 获取单日或多日时间安排
- 自动为今日及未来日期按规则生成安排
- 支持重复任务按规则自动生成
- 软删除确保历史记录完整