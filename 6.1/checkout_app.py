from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Checkout API
    接收 JSON 格式的 items 列表，计算总价。
    格式: {"items": [{"price": 10, "quantity": 2}, ...]}
    """
    data = request.get_json()
    
    # 容错处理：如果 data 为 None（未发送JSON），或者没有 items 键，默认为空列表
    if not data:
        items = []
    else:
        items = data.get("items", [])
    
    # 业务规则：购物车不能为空
    if not items: 
        return jsonify({"error": "empty cart"}), 400
    
    try:
        # 计算总价
        total = sum(i["price"] * i["quantity"] for i in items)
        return jsonify({"total": total, "status": "ok"}), 200
    except KeyError:
        # 额外防护：如果 items 里缺少 price 或 quantity 字段
        return jsonify({"error": "invalid item format"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)