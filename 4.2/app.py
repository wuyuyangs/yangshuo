from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 1. 模拟数据库 (内存中) ---
# 库存模块数据
inventory = {
    "book": 10,
    "pen": 50
}
# 商品价格 (用于支付模块)
prices = {
    "book": 20.0,
    "pen": 5.0
}

# --- 2. 核心业务逻辑 (模块化，便于单元测试) ---

def check_and_lock_inventory(item, qty):
    """
    库存模块：检查并锁定库存
    """
    if item not in inventory:
        raise ValueError("不存在的商品")
    if qty <= 0:
        raise ValueError("数量必须大于0")
    if inventory[item] < qty:
        raise ValueError("库存不足")
    return True

def process_payment(item, qty, payment_amount):
    """
    支付模块：计算总价并验证支付
    """
    if item not in prices:
        raise ValueError("无法计算价格")
    
    total_price = prices[item] * qty
    
    # 简单的模拟：如果支付金额小于总价，则失败
    if payment_amount < total_price:
        return False, f"支付金额不足，需支付: {total_price}"
    
    return True, "支付成功"

def decrease_inventory(item, qty):
    """
    库存模块：扣减库存 (在支付成功后调用)
    """
    inventory[item] -= qty
    return inventory[item]

# --- 3. API 接口层 ---

@app.route("/order", methods=["POST"])
def order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "无效的JSON数据"}), 400

        # 获取参数
        item = data.get("item")
        qty = data.get("qty", 1)
         # 默认购买1个
        payment = data.get("payment", 0) # 支付金额

        # 第一步：检查库存
        check_and_lock_inventory(item, qty)

        # 第二步：处理支付
        success, message = process_payment(item, qty, payment)
        if not success:
            return jsonify({"success": False, "error": message}), 402 # Payment Required

        # 第三步：正式扣减库存
        remaining = decrease_inventory(item, qty)

        return jsonify({
            "success": True,
            "message": "下单成功",
            "item": item,
            "deducted_qty": qty,
            "remaining_stock": remaining
        })

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "系统内部错误"}), 500

if __name__ == "__main__":
    print("启动订单系统服务...")
    print("当前库存:", inventory)
    app.run(debug=True, port=5000)