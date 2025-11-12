import os
os.environ['DATABASE_URL'] = 'postgresql://postgres@localhost/daydayup'

from app.database import engine, Base
from app.models.task import Task, ScheduleRecord
from app.models.user import User
from sqlalchemy import inspect, text

def test_connection():
    try:
        # 检查数据库连接
        inspector = inspect(engine)
        print("✅ 数据库连接成功!")
        
        # 获取所有表名
        tables = inspector.get_table_names()
        print(f"📊 数据库中现有表: {tables}")
        
        # 手动创建任务相关的表
        print("📝 正在创建任务相关表...")
        Task.__table__.create(bind=engine, checkfirst=True)
        ScheduleRecord.__table__.create(bind=engine, checkfirst=True)
        User.__table__.create(bind=engine, checkfirst=True)
        print("✅ 任务相关表已创建/确认存在")
        
        # 再次检查表
        tables = inspector.get_table_names()
        print(f"📊 更新后数据库表: {tables}")
        
        # 显示表结构
        for table in tables:
            if table in ['tasks', 'schedule_records', 'users']:
                print(f"\n📋 表 '{table}' 的列:")
                columns = inspector.get_columns(table)
                for col in columns:
                    print(f"  - {col['name']} ({col['type']})")
        
        # 检查是否有所需的表
        if 'tasks' in tables and 'schedule_records' in tables:
            print("\n✅ 任务和时间表相关表创建成功!")
        else:
            print("\n⚠️ 任务和时间表相关表可能未创建")
        
        print("\n🎉 数据库连接测试完成!")
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()