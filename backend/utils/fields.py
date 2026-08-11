"""
自定义 JSON 字段（标记类型）。
实际中文编码由 utils.apps.ChineseJsonConfig 在 MySQL 后端层修复。
此字段保持与 models.JSONField 完全一致，仅作为可识别的标记。
"""

from django.db import models


class ChineseJSONField(models.JSONField):
    """标记为中文 JSON 字段，序列化行为由 MySQL 后端补丁控制"""
