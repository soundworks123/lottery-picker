@echo off
echo 正在启动彩票选号系统...

:: 启动后端服务
start cmd /k "cd backend && .venv\Scripts\activate && python app.py"

:: 等待后端服务启动
timeout /t 5

:: 启动前端服务
start cmd /k "cd frontend && npm run serve"

echo 服务启动完成！
echo 前端访问地址：http://localhost:8080
echo 后端API地址：http://localhost:5000

pause 