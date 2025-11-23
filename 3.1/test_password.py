import pytest
from password import isValidPassword

@pytest.mark.parametrize("test_input, expected", [
    ("abc123", True),              # TC1：长度6合法，字母+数字
    ("a1b2c3d4", True),            # TC2：正常合法
    ("abcd", False),               # TC3：长度不足
    ("abcdefghijklm", False),      # TC4：长度超限
    ("abcdefg", False),            # TC5：只有字母
    ("1234567", False),            # TC6：只有数字
    ("!!!!@@@", False),            # TC7：无字母无数字
    ("abc12", False),              # TC8：边界长度5
    ("abcd1234xyz99", False),      # TC9：边界长度13
    ("ab12cd34ef56", True),        # TC10：边界长度12
])
def test_isValidPassword(test_input, expected):
    assert isValidPassword(test_input) == expected
