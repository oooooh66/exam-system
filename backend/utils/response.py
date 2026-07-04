"""
统一响应格式模块（Response 层）
========================
在整个请求链路中的位置：【最终出口 —— 把数据打包返回给前端】

调用链（以成功响应为例）：
  1. View 层处理完业务逻辑
  2. 调用 APIResponse.success(data=..., message='操作成功')
  3. APIResponse.__init__() 把数据包装成统一格式
  4. DRF Response.__init__() 把字典转成 JSON 字符串
  5. Django HttpResponse 把 JSON 包装成 HTTP 响应
  6. 中间件层添加 CORS 头等
  7. 浏览器收到 HTTP Response，解析 JSON

统一响应格式（所有接口都返回这个结构）：
  成功响应：
    {
      "code": 200,
      "message": "success",
      "data": {"id": 1, "username": "admin", ...}
    }
  错误响应：
    {
      "code": 400,
      "message": "用户名已存在",
      "data": null
    }

为什么需要统一格式？
  - 前端只需一套解析逻辑（Axios 拦截器里统一取 res.data.data）
  - 错误信息始终在 message 字段，前端直接弹窗显示
  - code 对应 HTTP 状态码，方便前端判断成功/失败
"""

from rest_framework.response import Response     # DRF 的响应基类
from rest_framework import status                   # HTTP 状态码常量


class APIResponse(Response):
    """
    【统一 API 响应类】继承 DRF 的 Response，自动包装为 {code, message, data} 格式

    包装逻辑（以 success 为例）：
      APIResponse.success(data={"name": "test"}, message="创建成功")
        ↓
      __init__() 构造 response_data = {
        "code": 200,
        "message": "创建成功",
        "data": {"name": "test"}
      }
        ↓
      父类 Response.__init__() 把字典序列化为 JSON 字符串
        ↓
      HTTP 响应正文：'{"code":200,"message":"创建成功","data":{"name":"test"}}'
    """

    def __init__(
        self,
        data=None,           # 要返回的数据（可以是 dict、list、None）
        code=200,            # 业务状态码（默认 200 成功）
        message='success',   # 提示信息
        http_status=None,    # HTTP 协议状态码（如 200、201、400）
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        **kwargs
    ):
        """
        构造统一响应体

        参数说明：
          data:    业务数据（如查询结果、创建的对象信息）
          code:    业务层面的状态码（200=成功，201=创建成功，400=请求错误，500=服务器错误）
          message: 给前端的提示信息（如"登录成功"、"用户名已存在"）
          http_status: HTTP 协议状态码，如果不传则根据 code 自动推算
        """
        # 1. 构造统一的三段式响应体
        response_data = {
            'code': code,
            'message': message,
            'data': data if data is not None else {},
        }

        # 2. 自动推导 HTTP 状态码（如果调用方没有显式指定）
        if http_status is None:
            http_status = self._code_to_http_status(code)

        # 3. 调用父类 Response 的构造函数
        #    DRF 内部会：
        #      a. 用 JSONRenderer 把 response_data 序列化为 JSON 字符串
        #      b. 设置 Content-Type: application/json
        #      c. 包装成标准 HTTP Response 对象
        super().__init__(
            data=response_data,
            status=http_status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )

    def _code_to_http_status(self, code):
        """根据业务状态码自动推导对应的 HTTP 状态码"""
        mapping = {
            200: status.HTTP_200_OK,              # 200 → HTTP 200
            201: status.HTTP_201_CREATED,         # 201 → HTTP 201
            400: status.HTTP_400_BAD_REQUEST,     # 400 → HTTP 400
            401: status.HTTP_401_UNAUTHORIZED,    # 401 → HTTP 401
            403: status.HTTP_403_FORBIDDEN,       # 403 → HTTP 403
            404: status.HTTP_404_NOT_FOUND,       # 404 → HTTP 404
            500: status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 → HTTP 500
        }
        return mapping.get(code, status.HTTP_200_OK)

    # ==================== 便捷类方法 ====================

    @classmethod
    def success(cls, data=None, message='success', code=200):
        """
        【操作成功响应】最常用的方法

        用法：return APIResponse.success(data=result, message='登录成功')

        等价于：
          return APIResponse(data=result, code=200, message='登录成功')

        前端 Axios 接收后：
          response.data = { code: 200, message: '登录成功', data: result }
        """
        return cls(data=data, code=code, message=message)

    @classmethod
    def created(cls, data=None, message='创建成功'):
        """
        【创建成功响应】常用于 POST 接口返回新创建的对象

        用法：return APIResponse.created(data=new_user, message='注册成功')

        等价于：
          return APIResponse(data=new_user, code=201, message='注册成功')

        HTTP 状态码 201 Created 告诉浏览器"一个新的资源被创建了"
        """
        return cls(data=data, code=201, message=message)

    @classmethod
    def error(cls, code=400, message='操作失败', data=None):
        """
        【操作失败响应】通用的错误响应

        用法：
          return APIResponse.error(code=400, message='用户名已存在')
          return APIResponse.error(code=404, message='用户不存在')
          return APIResponse.error(code=403, message='没有权限')
        """
        return cls(data=data, code=code, message=message)

    @classmethod
    def bad_request(cls, message='请求参数错误', data=None):
        """HTTP 400 错误（客户端参数问题）"""
        return cls(data=data, code=400, message=message)

    @classmethod
    def unauthorized(cls, message='未登录或 Token 已过期', data=None):
        """HTTP 401 错误（需要登录）"""
        return cls(data=data, code=401, message=message)

    @classmethod
    def forbidden(cls, message='无权限访问', data=None):
        """HTTP 403 错误（权限不足）"""
        return cls(data=data, code=403, message=message)

    @classmethod
    def not_found(cls, message='资源不存在', data=None):
        """HTTP 404 错误（资源不存在）"""
        return cls(data=data, code=404, message=message)

    @classmethod
    def server_error(cls, message='服务器内部错误', data=None):
        """HTTP 500 错误（服务器异常）"""
        return cls(data=data, code=500, message=message)
