import pytest
from slugify import slugify

class TestSlugify:
    
    # 测试逻辑分支1：默认处理流程
    def test_basic_slugification(self):
        text = "Hello World! 2025"
        expected = "hello-world-2025"
        assert slugify(text) == expected

    # 测试逻辑分支2：自定义分隔符参数处理
    def test_custom_separator(self):
        text = "Python is great"
        expected = "python_is_great"
        assert slugify(text, separator="_") == expected

    # 测试逻辑分支3：条件判断（跳过小写转换）
    def test_preserve_casing(self):
        text = "MobileNetV3 Model"
        expected = "MobileNetV3-Model"
        assert slugify(text, lowercase=False) == expected