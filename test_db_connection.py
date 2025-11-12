import os
os.environ['DATABASE_URL'] = 'postgresql://postgres@localhost/daydayup'

from app.database import engine, Base
from sqlalchemy import inspect, text

def test_connection():
    try:
        # 检查数据库连接
        inspector = inspect(engine)
        print("✅ 数据库连接成功!")
        
        # 获取所有表名
        tables = inspector.get_table_names()
        print(f"📊 数据库中现有表: {tables}")
        
        # 创建所有表
        print("📝 正在创建表...")
        Base.metadata.create_all(bind=engine)
        print("✅ 表已创建/确认存在")
        
        # 再次检查表
        tables = inspector.get_table_names()
        print(f"📊 更新后数据库表: {tables}")
        
        # 显示表结构
        if tables:
            for table in tables:
                print(f"\n📋 表 '{table}' 的列:")
                columns = inspector.get_columns(table)
                for col in columns:
                    print(f"  - {col['name']} ({col['type']})")
        
        # 检查是否有用户表
        if 'users' in tables:
            print("\n✅ 用户表创建成功!")
        else:
            print("\n⚠️ 用户表可能未创建")
        
        print("\n🎉 数据库连接测试完成!")
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()