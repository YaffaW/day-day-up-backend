from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime
import uuid


class TaskBase(BaseModel):
    type: str
    title: str
    theme_color: str
    progress: Optional[int] = None
    is_completed: Optional[bool] = False
    description: Optional[str] = None
    repeat_weekdays: Optional[str] = None  # JSON格式存储数组
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    class Config:
        alias_generator = lambda field: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field.split('_')))
        allow_population_by_field_name = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        alias_generator = lambda field: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field.split('_')))
        allow_population_by_field_name = True


class ScheduleRecordBase(BaseModel):
    task_id: Optional[str] = None
    date: date
    start_time: time
    end_time: time
    title: str
    theme_color: str
    is_completed: Optional[bool] = False
    description: Optional[str] = None

    class Config:
        alias_generator = lambda field: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field.split('_')))
        allow_population_by_field_name = True


class ScheduleRecordCreate(ScheduleRecordBase):
    pass


from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime
import uuid
from pydantic import ConfigDict


class TaskBase(BaseModel):
    type: str
    title: str
    theme_color: str
    progress: Optional[int] = None
    is_completed: Optional[bool] = False
    description: Optional[str] = None
    repeat_weekdays: Optional[str] = None  # JSON格式存储数组
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_'))
        )
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_'))
        )
    )


class ScheduleRecordBase(BaseModel):
    task_id: Optional[str] = None
    date: date
    start_time: time
    end_time: time
    title: str
    theme_color: str
    is_completed: Optional[bool] = False
    description: Optional[str] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_'))
        )
    )


class ScheduleRecordCreate(ScheduleRecordBase):
    pass


class ScheduleRecordUpdate(BaseModel):
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    title: Optional[str] = None
    theme_color: Optional[str] = None
    is_completed: Optional[bool] = None
    description: Optional[str] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_'))
        )
    )


class ScheduleRecordInDB(ScheduleRecordBase):
    id: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_'))
        )
    )


class ScheduleQuery(BaseModel):
    start_date: date
    end_date: Optional[date] = None  # 如果不提供，则只查询start_date当天的数据
    
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_'))
        )
    )


class ScheduleRecordInDB(ScheduleRecordBase):
    id: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        alias_generator = lambda field: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field.split('_')))
        allow_population_by_field_name = True


class ScheduleQuery(BaseModel):
    start_date: date
    end_date: Optional[date] = None  # 如果不提供，则只查询start_date当天的数据

    class Config:
        alias_generator = lambda field: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field.split('_')))
        allow_population_by_field_name = True