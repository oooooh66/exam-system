"""
全局异常处理模块

统一处理所有未捕获的异常，返回统一格式的 JSON 响应。
"""
import logging
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    ParseError,
    MethodNotAllowed,
)
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger('apps')


def custom_exception_handler(exc, context):
    """
    自定义异常处理器

    将 DRF 异常和 Django 异常统一转换为标准响应格式：
    { "code": xxx, "message": "xxx", "data": null }
    """
    # 先调用 DRF 默认的异常处理器，获取标准 DRF 异常响应
    response = drf_exception_handler(exc, context)

    if response is not None:
        # DRF 能处理的异常，统一格式
        error_message = _get_error_message(response.data)
        return _build_error_response(
            code=response.status_code,
            message=error_message,
        )

    # DRF 无法处理的异常（如非 API 视图的异常）
    if isinstance(exc, Http404):
        return _build_error_response(
            code=status.HTTP_404_NOT_FOUND,
            message='请求的资源不存在',
        )

    if isinstance(exc, PermissionDenied):
        return _build_error_response(
            code=status.HTTP_403_FORBIDDEN,
            message='没有权限执行此操作',
        )

    if isinstance(exc, ValidationError):
        return _build_error_response(
            code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
        )

    # 未预期的异常：记录日志并返回 500
    logger.exception(f'未处理的异常: {type(exc).__name__}: {str(exc)}')
    return _build_error_response(
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message='服务器内部错误，请联系管理员',
    )


def _get_error_message(data):
    """
    从 DRF 异常响应中提取用户友好的错误信息。
    支持 validated_data 错误格式的嵌套提取。
    """
    if isinstance(data, dict):
        # 取第一个字段的错误信息
        for key, value in data.items():
            if isinstance(value, list):
                return str(value[0]) if value else '请求参数错误'
            if isinstance(value, str):
                return value
        return '请求参数错误'
    if isinstance(data, list):
        return str(data[0]) if data else '请求参数错误'
    return str(data)


def _build_error_response(code, message):
    """构造统一格式的错误响应"""
    from rest_framework.response import Response
    return Response(
        data={
            'code': code,
            'message': message,
            'data': None,
        },
        status=code,
    )
