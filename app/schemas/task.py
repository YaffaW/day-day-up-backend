from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime
import uuid


class TaskBase(BaseModel):
    type: str
    title: str
    theme_color: str = Field(alias='themeColor')
    progress: Optional[int] = None
    is_completed: Optional[bool] = Field(default=False, alias='isCompleted')
    description: Optional[str] = None
    repeat_weekdays: Optional[str] = Field(default=None, alias='repeatWeekdays')
    start_date: Optional[date] = Field(default=None, alias='startDate')
    end_date: Optional[date] = Field(default=None, alias='endDate')
    start_time: Optional[time] = Field(default=None, alias='startTime')
    end_time: Optional[time] = Field(default=None, alias='endTime')

    class Config:
        from_attributes = True
        populate_by_name = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: str
    status: str
    created_at: Optional[datetime] = Field(default=None, alias='createdAt')
    updated_at: Optional[datetime] = Field(default=None, alias='updatedAt')

    class Config:
        from_attributes = True
        populate_by_name = True


class ScheduleRecordBase(BaseModel):
    task_id: Optional[str] = Field(default=None, alias='taskId')
    date: date
    start_time: time = Field(alias='startTime')
    end_time: time = Field(alias='endTime')
    title: str
    theme_color: str = Field(alias='themeColor')
    is_completed: Optional[bool] = Field(default=False, alias='isCompleted')
    description: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class ScheduleRecordCreate(ScheduleRecordBase):
    pass


class ScheduleRecordUpdate(BaseModel):
    start_time: Optional[time] = Field(default=None, alias='startTime')
    end_time: Optional[time] = Field(default=None, alias='endTime')
    title: Optional[str] = None
    theme_color: Optional[str] = Field(default=None, alias='themeColor')
    is_completed: Optional[bool] = Field(default=None, alias='isCompleted')
    description: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class ScheduleRecordInDB(ScheduleRecordBase):
    id: str
    status: str
    created_at: Optional[datetime] = Field(default=None, alias='createdAt')
    updated_at: Optional[datetime] = Field(default=None, alias='updatedAt')

    class Config:
        from_attributes = True
        populate_by_name = True


class ScheduleQuery(BaseModel):
    start_date: date = Field(alias='startDate')
    end_date: Optional[date] = Field(default=None, alias='endDate')  # 如果不提供，则只查询start_date当天的数据

    class Config:
        from_attributes = True
        populate_by_name = True