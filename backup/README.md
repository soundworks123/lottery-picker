# 彩票选号系统部署说明

## 项目结构
```
彩票选号/
├── frontend/          # 前端项目
│   ├── src/          # 源代码
│   ├── public/       # 静态资源
│   └── nginx.conf    # Nginx配置
├── backend/          # 后端项目
│   ├── app.py       # 主程序
│   └── .venv/       # Python虚拟环境
└── backup/          # 备份文件
    ├── database_backup/  # 数据库备份
    ├── README.md        # 说明文档
    ├── requirements.txt # Python依赖
    ├── package.json    # 前端依赖
    ├── start_services.bat    # 启动服务
    ├── backup_database.bat   # 数据库备份
    └── restore_system.bat    # 系统恢复
```

## 环境要求
- Node.js >= 12.0.0
- Python >= 3.8
- Nginx >= 1.18

## 部署步骤

### 1. 前端部署
```bash
cd frontend
npm install
npm run build
```

### 2. 后端部署
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install flask flask-cors pandas numpy scikit-learn
python app.py
```

### 3. Nginx配置
- 配置文件位置：`frontend/nginx.conf`
- 主要配置：
  - 开启gzip压缩
  - 配置静态资源缓存
  - 配置API代理
  - 支持前端路由

## 性能优化配置
1. Element UI按需加载
2. 路由组件预加载
3. Webpack生产环境优化
4. 图片资源优化

## 访问地址
- 前端：http://localhost:8080
- 后端API：http://localhost:5000

## 注意事项
1. 确保后端服务正常运行
2. 检查Nginx配置是否正确
3. 确保所有依赖包已正确安装
4. 生产环境部署时注意关闭调试模式

## 备份和恢复

### 备份系统
1. 运行 `backup_database.bat` 备份数据库
2. 复制整个项目目录到安全位置
3. 定期更新 `requirements.txt` 和 `package.json`

### 恢复系统
1. 运行 `restore_system.bat` 恢复系统环境
2. 运行 `start_services.bat` 启动服务

### 备份说明
- 备份时间：2025-03-18
- 备份内容：完整项目代码和配置文件
- 备份目的：系统恢复和版本管理

## 维护建议
1. 每周进行一次数据库备份
2. 每月更新一次依赖包版本
3. 定期检查系统日志
4. 保持系统安全更新 