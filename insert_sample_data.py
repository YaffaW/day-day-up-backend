import os
os.environ['DATABASE_URL'] = 'postgresql://postgres@localhost/daydayup'

from app.database import engine
from sqlalchemy import text

def insert_sample_data():
    with engine.connect() as conn:
        # 开始事务
        trans = conn.begin()
        
        try:
            # 插入示例任务数据
            conn.execute(text("""
            INSERT INTO tasks (id, type, title, theme_color, progress, is_completed, description, repeat_weekdays, start_date, end_date, start_time, end_time, status) VALUES
            ('1', 'progress', 'Learning English', '#ffcc00', 10, FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布', '[1,2,3,4,5,6]', '2025-08-24', NULL, '10:00:00', '11:00:00', 'active');
            """))
            
            conn.execute(text("""
            INSERT INTO tasks (id, type, title, theme_color, progress, is_completed, description, repeat_weekdays, start_date, end_date, start_time, end_time, status) VALUES
            ('2', 'regular', '源码学习', '#00ccff', NULL, FALSE, '阅读 React、Vue 等前端框架源码', '[6]', '2025-08-24', NULL, NULL, NULL, 'active');
            """))
            
            conn.execute(text("""
            INSERT INTO tasks (id, type, title, theme_color, progress, is_completed, description, repeat_weekdays, start_date, end_date, start_time, end_time, status) VALUES
            ('3', 'recurring', '学习webgl', '#51ff00', NULL, FALSE, '为了找工作，快速入门webgl', '[1,2,3,4,5,6]', '2025-08-24', NULL, NULL, NULL, 'active');
            """))
            
            # 为重复任务在本周生成多个时间安排记录
            # 为任务1（Learning English）生成本周的安排
            conn.execute(text("""
            INSERT INTO schedule_records (id, task_id, date, start_time, end_time, title, theme_color, is_completed, description) VALUES
            ('sched-1-2025-08-25', '1', '2025-08-25', '10:00:00', '11:00:00', 'Learning English', '#ffcc00', FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布'),
            ('sched-1-2025-08-26', '1', '2025-08-26', '10:00:00', '11:00:00', 'Learning English', '#ffcc00', FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布'),
            ('sched-1-2025-08-27', '1', '2025-08-27', '10:00:00', '11:00:00', 'Learning English', '#ffcc00', FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布'),
            ('sched-1-2025-08-28', '1', '2025-08-28', '10:00:00', '11:00:00', 'Learning English', '#ffcc00', FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布'),
            ('sched-1-2025-08-29', '1', '2025-08-29', '10:00:00', '11:00:00', 'Learning English', '#ffcc00', FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布'),
            ('sched-1-2025-08-30', '1', '2025-08-30', '10:00:00', '11:00:00', 'Learning English', '#ffcc00', FALSE, '《The You You Are》：跟读练习、总结出自己的思考并发布');
            """))
            
            # 为任务2（源码学习）生成本周的安排（每周六）
            conn.execute(text("""
            INSERT INTO schedule_records (id, task_id, date, start_time, end_time, title, theme_color, is_completed, description) VALUES
            ('sched-2-2025-08-30', '2', '2025-08-30', '09:00:00', '12:00:00', '源码学习', '#00ccff', FALSE, '阅读 React、Vue 等前端框架源码');
            """))
            
            # 为任务3（学习webgl）生成本周的安排
            conn.execute(text("""
            INSERT INTO schedule_records (id, task_id, date, start_time, end_time, title, theme_color, is_completed, description) VALUES
            ('sched-3-2025-08-25', '3', '2025-08-25', '14:00:00', '16:00:00', '学习webgl', '#51ff00', FALSE, '为了找工作，快速入门webgl'),
            ('sched-3-2025-08-26', '3', '2025-08-26', '14:00:00', '16:00:00', '学习webgl', '#51ff00', FALSE, '为了找工作，快速入门webgl'),
            ('sched-3-2025-08-27', '3', '2025-08-27', '14:00:00', '16:00:00', '学习webgl', '#51ff00', FALSE, '为了找工作，快速入门webgl'),
            ('sched-3-2025-08-28', '3', '2025-08-28', '14:00:00', '16:00:00', '学习webgl', '#51ff00', FALSE, '为了找工作，快速入门webgl'),
            ('sched-3-2025-08-29', '3', '2025-08-29', '14:00:00', '16:00:00', '学习webgl', '#51ff00', FALSE, '为了找工作，快速入门webgl'),
            ('sched-3-2025-08-30', '3', '2025-08-30', '14:00:00', '16:00:00', '学习webgl', '#51ff00', FALSE, '为了找工作，快速入门webgl');
            """))
            
            # 演示某个任务单独修改的情况，例如将任务1在2025-08-26的安排单独修改
            conn.execute(text("""
            INSERT INTO schedule_records (id, task_id, date, start_time, end_time, title, theme_color, is_completed, description) VALUES
            ('sched-1-2025-08-26-mod', '1', '2025-08-26', '15:00:00', '16:30:00', 'Learning English', '#ffcc00', TRUE, '《The You You Are》：跟读练习、总结出自己的思考并发布');
            """))
            
            # 演示一个临时任务（在任务表中不存在）
            conn.execute(text("""
            INSERT INTO schedule_records (id, task_id, date, start_time, end_time, title, theme_color, is_completed, description) VALUES
            ('temp-task-001', NULL, '2025-08-26', '13:00:00', '14:00:00', '临时会议', '#999999', FALSE, '临时安排的团队会议');
            """))
            
            # 提交事务
            trans.commit()
            print("✅ 示例数据插入成功！")
            
        except Exception as e:
            # 回滚事务
            trans.rollback()
            print(f"❌ 插入数据失败: {e}")
            raise e

if __name__ == "__main__":
    insert_sample_data()