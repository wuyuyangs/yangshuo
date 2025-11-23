import requests
import pytest
# 注意：运行此测试前，必须先在终端运行 'python app.py' 启动服务

BASE_URL = "http://127.0.0.1:5000/order"

def test_order_success():
    """
    场景1: 正常下单流程
    购买 2 本书，支付 40 元
    """
    payload = {
        "item": "book",
        "qty": 2,
        "payment": 40.0
    }
    
    res = requests.post(BASE_URL, json=payload)
    
    # 断言 HTTP 状态码
    assert res.status_code == 200
    
    data = res.json()
    # 断言业务逻辑
    assert data["success"] == True
    assert data["deducted_qty"] == 2
    # 初始是10，买了2，应该剩8 (假设这是第一次运行)
    # 注意：集成测试由于状态持久化(内存变量)，连续运行可能需要重置服务
    assert "remaining_stock" in data

def test_order_out_of_stock():
    """
    场景2: 库存不足
    """
    payload = {
        "item": "book",
        "qty": 100,
        "payment": 2000
    }
    res = requests.post(BASE_URL, json=payload)
    
    assert res.status_code == 400
    assert res.json()["success"] == False
    assert res.json()["error"] == "库存不足"

def test_order_payment_failed():
    """
    场景3: 支付金额不足
    """
    payload = {
        "item": "book",
        "qty": 1,
        "payment": 1.0 # 书价是20
    }
    res = requests.post(BASE_URL, json=payload)
    
    assert res.status_code == 402
    assert res.json()["success"] == False
    assert "支付金额不足" in res.json()["error"]

if __name__ == "__main__":
    # 允许直接运行此脚本进行测试
    print("正在运行集成测试... (请确保 app.py 已启动)")
    try:
        test_order_success()
        print("✅ test_order_success 通过")
        test_order_out_of_stock()
        print("✅ test_order_out_of_stock 通过")
        test_order_payment_failed()
        print("✅ test_order_payment_failed 通过")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请先运行 'python app.py'")