@echo off
echo 开始恢复系统...

:: 检查环境
echo 检查环境要求...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未安装Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未安装Node.js，请先安装Node.js 12.0.0或更高版本
    pause
    exit /b 1
)

:: 恢复后端
echo 恢复后端环境...
cd ..\backend
python -m venv .venv
call .venv\Scripts\activate
pip install -r ..\backup\requirements.txt

:: 恢复前端
echo 恢复前端环境...
cd ..\frontend
npm install

:: 恢复数据库
echo 恢复数据库...
if exist "..\backup\database_backup\lottery_data.csv" (
    if not exist "..\backend\data" mkdir "..\backend\data"
    copy /Y "..\backup\database_backup\lottery_data.csv" "..\backend\data\lottery_data.csv"
)

echo 系统恢复完成！
echo 请运行 start_services.bat 启动服务

pause 