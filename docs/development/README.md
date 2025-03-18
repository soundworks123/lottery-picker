# 开发环境搭建指南

## 环境要求

### 基础环境
- Node.js >= 12.0.0
- Python >= 3.8
- Git
- Nginx >= 1.18

### 开发工具推荐
- VS Code
- PyCharm
- Postman (API测试)
- Git GUI (如 SourceTree)

## 前端开发环境

### 1. 安装 Node.js
1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载并安装 LTS 版本
3. 验证安装：
   ```bash
   node --version
   npm --version
   ```

### 2. 安装项目依赖
```bash
cd frontend
npm install
```

### 3. 开发服务器
```bash
npm run serve
```

### 4. 代码规范
- 使用 ESLint 进行代码检查
- 使用 Prettier 进行代码格式化
- 遵循 Vue.js 风格指南

### 5. 构建生产版本
```bash
npm run build
```

## 后端开发环境

### 1. 安装 Python
1. 访问 [Python 官网](https://www.python.org/)
2. 下载并安装 Python 3.8 或更高版本
3. 验证安装：
   ```bash
   python --version
   pip --version
   ```

### 2. 创建虚拟环境
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 开发服务器
```bash
python app.py
```

### 5. 代码规范
- 使用 PEP 8 编码规范
- 使用 Black 进行代码格式化
- 使用 Flake8 进行代码检查

## 数据库

### 1. 初始化数据库
```bash
cd backend
flask db init
flask db migrate
flask db upgrade
```

### 2. 导入测试数据
```bash
python scripts/import_test_data.py
```

## 开发流程

### 1. 获取最新代码
```bash
git pull origin main
```

### 2. 创建特性分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 开发新功能
- 遵循代码规范
- 编写单元测试
- 更新文档

### 4. 提交更改
```bash
git add .
git commit -m "描述你的更改"
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request
1. 访问 GitHub 仓库
2. 点击 "New Pull Request"
3. 选择你的特性分支
4. 填写 PR 描述
5. 等待代码审查

## 调试技巧

### 前端调试
1. 使用 Vue Devtools
2. 使用浏览器开发者工具
3. 使用 console.log() 和 Vue 的 $log 方法

### 后端调试
1. 使用 Flask 调试模式
2. 使用 Python 调试器 (pdb)
3. 使用日志记录

## 常见问题

### 1. 前端依赖安装失败
- 清除 npm 缓存：`npm cache clean --force`
- 删除 node_modules 目录
- 重新安装依赖

### 2. 后端依赖安装失败
- 更新 pip：`python -m pip install --upgrade pip`
- 使用国内镜像源
- 检查 Python 版本兼容性

### 3. 数据库连接问题
- 检查数据库服务是否运行
- 验证连接字符串
- 检查数据库用户权限

## 性能优化

### 前端优化
1. 使用 Vue 异步组件
2. 路由懒加载
3. 图片资源优化
4. 代码分割

### 后端优化
1. 使用缓存
2. 数据库索引优化
3. 异步任务处理
4. 连接池管理

## 部署指南

详细的部署说明请参考 [部署文档](../README.md) 