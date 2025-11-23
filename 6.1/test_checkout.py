import pytest
from checkout_app import app  # 导入被测应用

@pytest.fixture
def client():
    """
    Pytest 夹具：创建一个测试客户端。
    它模拟了一个真实的服务器环境，允许我们在不启动实际服务器的情况下发送 HTTP 请求。
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_checkout_normal_single_item(client):
    """TC01: 测试单个商品的正常结账"""
    payload = {
        "items": [
            {"price": 100, "quantity": 2}
        ]
    }
    # 模拟 POST 请求
    response = client.post("/checkout", json=payload)
    data = response.get_json()

    # 断言：检查状态码和业务逻辑
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["total"] == 200

def test_checkout_normal_multiple_items(client):
    """TC02: 测试多个商品的累加计算"""
    payload = {
        "items": [
            {"price": 10, "quantity": 1},  # 10
            {"price": 20, "quantity": 2},  # 40
            {"price": 5, "quantity": 2}    # 10
        ]
    }
    response = client.post("/checkout", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["total"] == 60  # 10 + 40 + 10 = 60

def test_checkout_empty_cart(client):
    """TC03: 测试空购物车的异常处理"""
    payload = {"items": []}
    
    response = client.post("/checkout", json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "empty cart"

def test_checkout_missing_key(client):
    """TC04: 测试请求中缺少 'items' 键的情况"""
    payload = {}  # 空字典
    
    response = client.post("/checkout", json=payload)
    data = response.get_json()

    # 根据代码逻辑，get("items", []) 会返回空列表，进而触发 400 error
    assert response.status_code == 400
    assert data["error"] == "empty cart"

def test_checkout_float_prices(client):
    """额外测试: 测试浮点数价格（真实场景常见）"""
    payload = {
        "items": [
            {"price": 10.5, "quantity": 2}
        ]
    }
    response = client.post("/checkout", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["total"] == 21.0