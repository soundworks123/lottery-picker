# API 文档

## 基础信息

- 基础URL: `http://localhost:5000/api`
- 所有请求和响应均使用 JSON 格式
- 时间格式：ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ)

## 认证

所有需要认证的接口都需要在请求头中携带 token：

```
Authorization: Bearer <your_token>
```

## 接口列表

### 1. 选号相关

#### 1.1 获取选号结果
- 请求方法：`POST`
- 路径：`/lottery/generate`
- 请求参数：
  ```json
  {
    "type": "双色球",  // 彩票类型
    "count": 5,       // 生成数量
    "conditions": {   // 选号条件（可选）
      "red_min": 1,
      "red_max": 33,
      "blue_min": 1,
      "blue_max": 16
    }
  }
  ```
- 响应示例：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {
      "numbers": [
        ["01", "05", "12", "15", "22", "28", "06"],
        ["03", "08", "11", "17", "25", "31", "09"]
      ]
    }
  }
  ```

### 2. 数据分析

#### 2.1 获取历史数据
- 请求方法：`GET`
- 路径：`/analysis/history`
- 查询参数：
  - `type`: 彩票类型
  - `start_date`: 开始日期
  - `end_date`: 结束日期
- 响应示例：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {
      "dates": ["2025-01-01", "2025-01-03"],
      "numbers": [
        ["01", "05", "12", "15", "22", "28", "06"],
        ["03", "08", "11", "17", "25", "31", "09"]
      ]
    }
  }
  ```

#### 2.2 获取统计数据
- 请求方法：`GET`
- 路径：`/analysis/statistics`
- 查询参数：
  - `type`: 彩票类型
  - `period`: 统计周期（day/week/month/year）
- 响应示例：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {
      "red_stats": {
        "01": 100,
        "02": 95,
        // ... 其他号码
      },
      "blue_stats": {
        "01": 50,
        "02": 45,
        // ... 其他号码
      }
    }
  }
  ```

### 3. 预测系统

#### 3.1 获取预测结果
- 请求方法：`GET`
- 路径：`/prediction/next`
- 查询参数：
  - `type`: 彩票类型
- 响应示例：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {
      "numbers": ["01", "05", "12", "15", "22", "28", "06"],
      "confidence": 0.85,
      "factors": {
        "historical": 0.6,
        "pattern": 0.3,
        "random": 0.1
      }
    }
  }
  ```

### 4. 社区讨论

#### 4.1 获取帖子列表
- 请求方法：`GET`
- 路径：`/discussion/posts`
- 查询参数：
  - `page`: 页码
  - `size`: 每页数量
  - `category`: 分类（可选）
- 响应示例：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {
      "total": 100,
      "posts": [
        {
          "id": 1,
          "title": "分享我的选号经验",
          "author": "user123",
          "createTime": "2025-03-19T10:00:00Z",
          "views": 100,
          "comments": 5,
          "likes": 10
        }
      ]
    }
  }
  ```

#### 4.2 发布新帖子
- 请求方法：`POST`
- 路径：`/discussion/posts`
- 请求参数：
  ```json
  {
    "title": "分享我的选号经验",
    "content": "这是我的选号经验...",
    "category": "experience"
  }
  ```
- 响应示例：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {
      "id": 1,
      "title": "分享我的选号经验",
      "author": "user123",
      "createTime": "2025-03-19T10:00:00Z"
    }
  }
  ```

## 错误码说明

- 200: 成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器内部错误

## 更新日志

### v1.0.0 (2025-03-19)
- 初始版本发布
- 实现基础选号功能
- 实现数据分析功能
- 实现预测系统
- 实现社区讨论功能 