import pytest
from bank import transfer

def test_transfer_normal():
    """
    测试点：跨用户正常转账
    """
    a = {"balance": 100}
    b = {"balance": 50}
    
    # 执行转账
    result = transfer(a, b, 30)
    
    # 断言返回值和余额变化
    assert result == True
    assert a["balance"] == 70
    assert b["balance"] == 80

def test_transfer_negative():
    """
    测试点：负数金额 (边界条件)
    """
    a, b = {"balance": 100}, {"balance": 50}
    
    # 验证是否抛出 ValueError
    with pytest.raises(ValueError, match="转账金额必须为正数"):
        transfer(a, b, -10)

def test_transfer_insufficient_balance():
    """
    测试点：余额不足 (异常处理)
    """
    a, b = {"balance": 20}, {"balance": 50}
    
    # 验证是否抛出 ValueError
    with pytest.raises(ValueError, match="余额不足"):
        transfer(a, b, 50)