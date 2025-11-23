# file: app_with_db.py
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
    # 尝试连接 Docker 里的 MySQL
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        connect_timeout=1 # 设置超时时间短一点，方便测试
    )

@app.route('/order', methods=['POST'])
def create_order():
    try:
        # 1. 尝试连接数据库
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 执行一个简单的查询，证明数据库是活着的
            cursor.execute("SELECT 1")
        conn.close()
        
        # 2. 业务逻辑成功
        return jsonify({"status": "success", "msg": "订单已创建"}), 200
        
    except pymysql.MySQLError as e:
        # 3. 【关键】如果数据库连不上，捕获异常，返回 503 (Service Unavailable)
        # 这样前端就知道是服务器繁忙，而不是代码写错了
        print(f"数据库连接失败: {e}")
        return jsonify({"status": "error", "msg": "数据库服务不可用"}), 503

if __name__ == '__main__':
    app.run(port=5000)