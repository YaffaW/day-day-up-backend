import os
os.environ['DATABASE_URL'] = 'postgresql://postgres@localhost/daydayup'

from app.database import SessionLocal
from app.models.task import Task, ScheduleRecord
from datetime import date, timedelta
import json

def debug_schedule_logic():
    db = SessionLocal()
    
    # 模拟API逻辑
    start_date = date(2025, 11, 20)
    end_date = date(2025, 11, 20)  # 相同日期，只查一天
    
    # 获取当前日期
    current_date = date.today()
    
    print(f"查询范围: {start_date} 到 {end_date}")
    print(f"当前日期: {current_date}")
    
    # 查询在指定日期范围内已有的安排记录
    existing_records = db.query(ScheduleRecord).filter(
        ScheduleRecord.date >= start_date,
        ScheduleRecord.date <= end_date,
        ScheduleRecord.status == "active"
    ).all()
    
    print(f"已存在安排记录数量: {len(existing_records)}")
    for record in existing_records:
        print(f"  - {record.date}: {record.title} (ID: {record.task_id})")
    
    # 将已有的安排记录按照日期分组
    records_by_date = {}
    for record in existing_records:
        if record.date not in records_by_date:
            records_by_date[record.date] = []
        records_by_date[record.date].append(record)
    
    # 获取所有活跃任务
    active_tasks = db.query(Task).filter(Task.status == "active").all()
    
    print(f"活跃任务数量: {len(active_tasks)}")
    
    # 为日期范围内的每一天生成或获取安排记录
    result = []
    
    # 计算日期范围内的所有日期
    current_date_iter = start_date
    while current_date_iter <= end_date:
        print(f"\n处理日期: {current_date_iter} (星期 {current_date_iter.weekday() + 1})")
        
        # 添加当天已有的安排记录
        if current_date_iter in records_by_date:
            print(f"  已有 {len(records_by_date[current_date_iter])} 个安排")
            for record in records_by_date[current_date_iter]:
                result.append(record)
                print(f"    - {record.title}")
        else:
            print(f"  当前日期无已有安排")
        
        # 获取当天需要根据任务规则自动创建的安排记录
        if current_date_iter >= current_date:  # 只为今天及未来日期自动创建
            print(f"  当前日期 >= 今天, 进行自动创建检查")
            
            # 根据重复任务规则创建安排
            for task in active_tasks:
                print(f"    检查任务 {task.id} ({task.title}):")
                print(f"      类型: {task.type}")
                print(f"      重复规则: {task.repeat_weekdays}")
                
                should_add = False
                
                # 检查是否应该为当前日期添加此任务
                if task.type == "regular":
                    # regular类型任务只在特定日期添加
                    if task.start_date and current_date_iter == task.start_date:
                        should_add = True
                        print(f"      Regular任务: 日期匹配 {task.start_date}")
                elif task.type in ["recurring", "progress"]:
                    # recurring和progress类型任务根据重复规则添加
                    start_condition = (not task.start_date or current_date_iter >= task.start_date)
                    end_condition = (not task.end_date or current_date_iter <= task.end_date)
                    print(f"      日期条件检查: 开始={start_condition}, 结束={end_condition}")
                    
                    if start_condition and end_condition:
                        if task.repeat_weekdays:
                            try:
                                repeat_days = json.loads(task.repeat_weekdays)
                                current_weekday = current_date_iter.weekday() + 1  # 转换为1-7格式（周一到周日）
                                print(f"      重复规则: {repeat_days}, 今天是星期 {current_weekday}")
                                if current_weekday in repeat_days:
                                    should_add = True
                                    print(f"      星期匹配，应添加任务")
                                else:
                                    print(f"      星期不匹配，跳过")
                            except json.JSONDecodeError:
                                # 如果解析失败，跳过此任务
                                print(f"      JSON解析失败，跳过")
                                continue
                        else:
                            print(f"      无重复规则，跳过")
                    else:
                        print(f"      日期范围不满足，跳过")
                
                # 检查这个任务在当天是否已存在安排
                task_exists_today = any(
                    record.task_id == task.id for record in records_by_date.get(current_date_iter, [])
                )
                
                print(f"      任务在当天已存在安排: {task_exists_today}")
                
                if should_add and not task_exists_today:
                    print(f"      ✓ 创建新安排记录")
                    # 创建新的日程安排记录
                    new_record = {
                        'task_id': task.id,
                        'date': current_date_iter,
                        'start_time': task.start_time or timedelta(hours=9),  # 默认9点
                        'end_time': task.end_time or timedelta(hours=10),    # 默认10点
                        'title': task.title,
                        'theme_color': task.theme_color,
                        'is_completed': task.is_completed,
                        'description': task.description
                    }
                    result.append(new_record)
                    print(f"        - 添加: {new_record['title']}")
                elif should_add and task_exists_today:
                    print(f"      - 任务已存在，无需创建")
                elif not should_add:
                    print(f"      - 任务不应添加，跳过")
        
        current_date_iter += timedelta(days=1)
    
    print(f"\n最终结果数量: {len(result)}")
    for item in result:
        if isinstance(item, dict):
            print(f"  - NEW: {item['title']} (虚拟记录)")
        else:
            print(f"  - EXISTING: {item.title} at {item.start_time}")
    
    db.close()

if __name__ == "__main__":
    debug_schedule_logic()