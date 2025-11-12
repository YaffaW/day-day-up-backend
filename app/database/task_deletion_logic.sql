-- 创建存储过程来处理任务删除逻辑
-- 该存储过程将未来的时间安排记录状态改为'deleted'
DELIMITER //

CREATE PROCEDURE DeleteTaskWithScheduleRecords(IN task_id_param VARCHAR(255))
BEGIN
    DECLARE current_date DATE DEFAULT CURDATE();
    
    -- 开始事务
    START TRANSACTION;
    
    -- 将未来日期的安排记录状态改为'deleted'
    UPDATE schedule_records 
    SET status = 'deleted'
    WHERE task_id = task_id_param 
    AND DATE(date) > DATE(current_date);
    
    -- 更新任务状态为'deleted'
    UPDATE tasks 
    SET status = 'deleted'
    WHERE id = task_id_param;
    
    COMMIT;
END //

DELIMITER ;

-- 创建另一个存储过程，专门用于硬删除任务及其所有关联的安排记录
CREATE PROCEDURE HardDeleteTask(IN task_id_param VARCHAR(255))
BEGIN
    START TRANSACTION;
    
    -- 删除所有关联的时间安排记录
    DELETE FROM schedule_records WHERE task_id = task_id_param;
    
    -- 删除任务本身
    DELETE FROM tasks WHERE id = task_id_param;
    
    COMMIT;
END //

DELIMITER ;

-- 创建查询某个日期范围内的所有安排（包括临时任务）的视图
CREATE VIEW schedule_view AS
SELECT 
    sr.id,
    sr.task_id,
    COALESCE(t.title, sr.title) as title,
    COALESCE(t.theme_color, sr.theme_color) as theme_color,
    COALESCE(t.description, sr.description) as description,
    sr.date,
    sr.start_time,
    sr.end_time,
    COALESCE(t.is_completed, sr.is_completed) as is_completed,
    sr.status
FROM schedule_records sr
LEFT JOIN tasks t ON sr.task_id = t.id
WHERE sr.status = 'active';