from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, text
from app import models
from app.schemas import task as task_schemas
from app.database import get_db
from typing import List
from datetime import datetime, date as date_type, time, timedelta
import json
import uuid

router = APIRouter()


@router.get("/tasks/", response_model=List[task_schemas.TaskInDB])
def get_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    获取任务列表
    """
    try:
        tasks = db.query(models.Task).filter(models.Task.status == "active").offset(skip).limit(limit).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务列表时发生错误: {str(e)}")


@router.post("/tasks/", response_model=task_schemas.TaskInDB)
def create_task(task: task_schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    添加任务
    """
    db_task = models.Task(
        type=task.type,
        title=task.title,
        theme_color=task.theme_color,
        progress=task.progress,
        is_completed=task.is_completed,
        description=task.description,
        repeat_weekdays=task.repeat_weekdays,
        start_date=task.start_date,
        end_date=task.end_date,
        start_time=task.start_time,
        end_time=task.end_time
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}", response_model=task_schemas.TaskInDB)
def update_task(task_id: str, task: task_schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    编辑任务
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 更新任务信息
    update_data = task.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    删除任务（软删除）
    将未来日期的安排记录状态改为'deleted'
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 获取当前日期
    current_date = date_type.today()
    
    # 将未来日期的安排记录状态改为'deleted'
    db.query(models.ScheduleRecord).filter(
        and_(
            models.ScheduleRecord.task_id == task_id,
            models.ScheduleRecord.date > current_date,
            models.ScheduleRecord.status == "active"
        )
    ).update({models.ScheduleRecord.status: "deleted"})
    
    # 更新任务状态为'deleted'
    db_task.status = "deleted"
    
    db.commit()
    return {"message": "Task deleted successfully"}


@router.post("/schedule/", response_model=List[task_schemas.ScheduleRecordInDB])
def get_schedule_data(query: task_schemas.ScheduleQuery, db: Session = Depends(get_db)):
    """
    获取某一天或者某个时间段的时间表数据
    当前日期之前的记录不做修改，当前日期以及之后的，存在对应日期的，直接获取；
    不存在对应日期的，自动创建一条记录返回，创建的逻辑根据任务表的任务，自动填充对应重复日期的任务。
    """
    start_date = query.start_date
    end_date = query.end_date or start_date  # 如果没有提供结束日期，则只查询开始日期当天的数据
    
    # 获取当前日期
    current_date = date_type.today()
    
    # 查询在指定日期范围内已有的安排记录
    existing_records = db.query(models.ScheduleRecord).filter(
        and_(
            models.ScheduleRecord.date >= start_date,
            models.ScheduleRecord.date <= end_date,
            models.ScheduleRecord.status == "active"
        )
    ).all()
    
    # 将已有的安排记录按照日期分组
    records_by_date = {}
    for record in existing_records:
        if record.date not in records_by_date:
            records_by_date[record.date] = []
        records_by_date[record.date].append(record)
    
    # 获取所有活跃任务
    active_tasks = db.query(models.Task).filter(models.Task.status == "active").all()
    
    # 为日期范围内的每一天生成或获取安排记录
    result = []
    
    # 计算日期范围内的所有日期
    current_date_iter = start_date
    while current_date_iter <= end_date:
        # 添加当天已有的安排记录
        if current_date_iter in records_by_date:
            for record in records_by_date[current_date_iter]:
                result.append(record)
        
        # 获取当天需要根据任务规则自动创建的安排记录
        if current_date_iter >= current_date:  # 只为今天及未来日期自动创建
            # 根据重复任务规则创建安排
            for task in active_tasks:
                should_add = False
                
                # 检查是否应该为当前日期添加此任务
                if task.type == "regular":
                    # regular类型任务只在特定日期添加
                    if task.start_date and current_date_iter == task.start_date:
                        should_add = True
                elif task.type == "recurring":
                    # recurring类型任务根据重复规则添加
                    if (not task.start_date or current_date_iter >= task.start_date) and \
                       (not task.end_date or current_date_iter <= task.end_date):
                        if task.repeat_weekdays:
                            try:
                                repeat_days = json.loads(task.repeat_weekdays)
                                # Python中星期一为0，星期天为6
                                current_weekday = current_date_iter.weekday() + 1  # 转换为1-7格式（周一到周日）
                                if current_weekday in repeat_days:
                                    should_add = True
                            except json.JSONDecodeError:
                                # 如果解析失败，跳过此任务
                                continue
                elif task.type == "progress":
                    # progress类型任务根据重复规则添加
                    if (not task.start_date or current_date_iter >= task.start_date) and \
                       (not task.end_date or current_date_iter <= task.end_date):
                        if task.repeat_weekdays:
                            try:
                                repeat_days = json.loads(task.repeat_weekdays)
                                current_weekday = current_date_iter.weekday() + 1  # 转换为1-7格式（周一到周日）
                                if current_weekday in repeat_days:
                                    should_add = True
                            except json.JSONDecodeError:
                                # 如果解析失败，跳过此任务
                                continue
                
                # 检查这个任务在当天是否已存在安排
                task_exists_today = any(
                    record.task_id == task.id for record in records_by_date.get(current_date_iter, [])
                )
                
                if should_add and not task_exists_today:
                    # 创建新的日程安排记录
                    new_record = models.ScheduleRecord(
                        task_id=task.id,
                        date=current_date_iter,
                        start_time=task.start_time or time(9, 0),  # 默认9点
                        end_time=task.end_time or time(10, 0),    # 默认10点
                        title=task.title,
                        theme_color=task.theme_color,
                        is_completed=task.is_completed,
                        description=task.description
                    )
                    db.add(new_record)
                    result.append(new_record)
        
        current_date_iter += timedelta(days=1)
    
    # 提交可能的新创建的记录
    db.commit()
    
    return result