"""
AppConfig: 启动时覆盖所有 JSON 序列化，确保中文直存、直出，不做 \\uXXXX 转义。

只替换 json.dumps —— json.dump 底层也调用 json.dumps，但需保持参数兼容。
"""
import json
from django.apps import AppConfig

_original_dumps = json.dumps


def _patched_json_dumps(obj, *, skipkeys=False, ensure_ascii=False, check_circular=True,
                         allow_nan=True, cls=None, indent=None, separators=None,
                         default=None, sort_keys=False, **kw):
    """全局替换：ensure_ascii 默认改为 False"""
    return _original_dumps(
        obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan,
        cls=cls, indent=indent, separators=separators,
        default=default, sort_keys=sort_keys, **kw)


class ChineseJsonConfig(AppConfig):
    name = 'utils'
    verbose_name = '全局中文JSON'

    def ready(self):
        json.dumps = _patched_json_dumps
