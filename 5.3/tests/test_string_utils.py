"""
Unit tests for string_utils module
"""
import sys
import os
import pytest

# 将 src 目录添加到系统路径，确保能导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from string_utils import is_palindrome

class TestPalindrome:
    """测试回文判断函数的类"""

    def test_basic_palindrome(self):
        """测试标准回文字符串"""
        assert is_palindrome("madam") is True
        assert is_palindrome("racecar") is True

    def test_mixed_case_punctuation(self):
        """测试包含大小写和标点的复杂回文"""
        # "Able was I ere I saw Elba"
        assert is_palindrome("Able was I ere I saw Elba") is True
        # "Madam, I'm Adam"
        assert is_palindrome("Madam, I'm Adam") is True

    def test_not_palindrome(self):
        """测试非回文字符串"""
        assert is_palindrome("hello") is False
        assert is_palindrome("python") is False

    def test_empty_string(self):
        """测试空字符串（通常视为空回文）"""
        assert is_palindrome("") is True

    def test_invalid_input(self):
        """测试非字符串输入"""
        assert is_palindrome(12345) is False
        assert is_palindrome(None) is False