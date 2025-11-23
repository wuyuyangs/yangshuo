# file: app_simulation.py
import time
from flask import Flask, jsonify

app = Flask(__name__)

# 模拟数据库状态：False 代表正常，True 代表挂了
is_db_down = False

@app.route('/order', methods=['POST'])
def create_order():
    global is_db_down
    # 模拟：如果数据库标记为挂了，直接抛出异常或返回 503
    if is_db_down:
        return jsonify({"status": "error", "msg": "数据库连接超时"}), 503
    
    # 正常业务
    return jsonify({"status": "success", "msg": "订单已创建"}), 200

# --- 增加两个“上帝模式”接口，用来控制故障 ---
@app.route('/admin/kill_db', methods=['POST'])
def kill_db():
    global is_db_down
    is_db_down = True
    return "数据库已模拟崩溃", 200

@app.route('/admin/fix_db', methods=['POST'])
def fix_db():
    global is_db_down
    is_db_down = False
    return "数据库已模拟恢复", 200

if __name__ == '__main__':
    app.run(port=5000)