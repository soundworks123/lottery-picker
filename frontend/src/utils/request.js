import axios from 'axios'
import { Message } from 'element-ui'

/**
 * 创建 axios 实例
 */
const service = axios.create({
  baseURL: 'http://127.0.0.1:5000', // API 基础URL
  timeout: 15000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

/**
 * 请求拦截器
 */
service.interceptors.request.use(
  config => {
    // 在这里可以添加认证信息等
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 */
service.interceptors.response.use(
  response => {
    const res = response.data
    // 这里可以根据后端返回的状态码进行统一处理
    return res
  },
  error => {
    console.error('响应错误:', error)
    Message({
      message: error.message || '请求失败，请稍后重试',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service 