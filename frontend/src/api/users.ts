/**
 * 用户管理 API
 */
import request from '@/utils/request'

/** 获取用户列表（管理员） */
export function getUsersApi(params?: any) {
  return request.get('/users/', { params })
}

/** 创建用户 */
export function createUserApi(data: any) {
  return request.post('/users/', data)
}

/** 修改用户 */
export function updateUserApi(id: number, data: any) {
  return request.put(`/users/${id}/`, data)
}

/** 删除用户 */
export function deleteUserApi(id: number) {
  return request.delete(`/users/${id}/`)
}
