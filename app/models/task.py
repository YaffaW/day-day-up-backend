from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Time, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from app.database import Base
import enum
import uuid
from datetime import datetime


class TaskType(enum.Enum):
    regular = "regular"
    recurring = "recurring"
    progress = "progress"


class TaskStatus(enum.Enum):
    active = "active"
    deleted = "deleted"


class ScheduleRecordStatus(enum.Enum):
    active = "active"
    deleted = "deleted"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(ENUM(TaskType, name='task_type_enum'), nullable=False)
    title = Column(String(255), nullable=False)
    theme_color = Column(String(7), nullable=False)  # 十六进制颜色值，如#ffcc00
    progress = Column(Integer, CheckConstraint("progress >= 0 AND progress <= 100"))  # 进度百分比，仅用于progress类型
    is_completed = Column(Boolean, default=False)
    description = Column(Text)
    repeat_weekdays = Column(String)  # 重复星期几，JSON格式存储数组，如[1,2,3,4,5]表示周一到周五
    start_date = Column(Date)
    end_date = Column(Date)
    start_time = Column(Time)  # 任务默认开始时间
    end_time = Column(Time)  # 任务默认结束时间
    status = Column(ENUM(TaskStatus, name='task_status_enum'), default=TaskStatus.active)  # 任务状态，支持软删除
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScheduleRecord(Base):
    __tablename__ = "schedule_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id"))  # 关联的任务ID，对于临时任务可为空
    date = Column(Date, nullable=False)  # 安排的日期
    start_time = Column(Time, nullable=False)  # 开始时间
    end_time = Column(Time, nullable=False)  # 结束时间
    title = Column(String(255), nullable=False)  # 任务标题，用于临时任务或作为任务表的冗余字段
    theme_color = Column(String(7), nullable=False)  # 十六进制颜色值，用于临时任务或作为任务表的冗余字段
    is_completed = Column(Boolean, default=False)  # 完成状态
    description = Column(Text)  # 任务描述，用于临时任务或作为任务表的冗余字段
    status = Column(ENUM(ScheduleRecordStatus, name='schedule_record_status_enum'), default=ScheduleRecordStatus.active)  # 记录状态，支持软删除
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)