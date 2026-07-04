-- ============================================
-- 在线考试系统 - 数据库初始化脚本
-- 数据库: MariaDB / MySQL 8.0+
-- 字符集: utf8mb4
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS exam_system
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE exam_system;

-- 创建应用用户（可选，用于更细粒度的权限控制）
-- CREATE USER IF NOT EXISTS 'exam_user'@'localhost' IDENTIFIED BY 'exam_password_123';
-- GRANT ALL PRIVILEGES ON exam_system.* TO 'exam_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ============================================
-- 说明：
-- 具体的表结构由 Django ORM 通过 migrations 自动创建。
-- 运行以下命令生成并应用数据库迁移：
--   python manage.py makemigrations
--   python manage.py migrate
--
-- 如果需要手动建表，请参考各 app/models.py 中的模型定义。
-- ============================================
