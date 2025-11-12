-- 创建任务表
CREATE TABLE tasks (
    id VARCHAR(255) PRIMARY KEY,
    type ENUM('regular', 'recurring', 'progress') NOT NULL,
    title VARCHAR(255) NOT NULL,
    theme_color VARCHAR(7) NOT NULL COMMENT '十六进制颜色值，如#ffcc00',
    progress INT DEFAULT NULL CHECK (progress >= 0 AND progress <= 100) COMMENT '进度百分比，仅用于progress类型',
    is_completed BOOLEAN DEFAULT FALSE,
    description TEXT,
    repeat_weekdays JSON COMMENT '重复星期几，JSON格式存储数组，如[1,2,3,4,5]表示周一到周五',
    start_date DATE,
    end_date DATE,
    start_time TIME COMMENT '任务默认开始时间',
    end_time TIME COMMENT '任务默认结束时间',
    status ENUM('active', 'deleted') DEFAULT 'active' COMMENT '任务状态，支持软删除',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建时间安排记录表
CREATE TABLE schedule_records (
    id VARCHAR(255) PRIMARY KEY,
    task_id VARCHAR(255) COMMENT '关联的任务ID，对于临时任务可为空',
    date DATE NOT NULL COMMENT '安排的日期',
    start_time TIME NOT NULL COMMENT '开始时间',
    end_time TIME NOT NULL COMMENT '结束时间',
    title VARCHAR(255) NOT NULL COMMENT '任务标题，用于临时任务或作为任务表的冗余字段',
    theme_color VARCHAR(7) NOT NULL COMMENT '十六进制颜色值，用于临时任务或作为任务表的冗余字段',
    is_completed BOOLEAN DEFAULT FALSE COMMENT '完成状态',
    description TEXT COMMENT '任务描述，用于临时任务或作为任务表的冗余字段',
    status ENUM('active', 'deleted') DEFAULT 'active' COMMENT '记录状态，支持软删除',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 为常用查询创建索引
CREATE INDEX idx_schedule_records_task_date ON schedule_records(task_id, date);
CREATE INDEX idx_schedule_records_date_time ON schedule_records(date, start_time);
CREATE INDEX idx_tasks_type ON tasks(type);
CREATE INDEX idx_schedule_records_status ON schedule_records(status);