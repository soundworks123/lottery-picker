@echo off
echo 开始备份数据库...

:: 创建备份目录
set BACKUP_DIR=%~dp0database_backup
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

:: 设置备份文件名（使用当前日期时间）
set BACKUP_FILE=%BACKUP_DIR%\lottery_data_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.csv

:: 复制数据文件
copy /Y "..\backend\data\lottery_data.csv" "%BACKUP_FILE%"

echo 数据库备份完成！
echo 备份文件位置：%BACKUP_FILE%

pause 