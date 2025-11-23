# file: vulnerable_app.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# 初始化一个内存数据库，并插入一个管理员账号
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'super_secret_password')")
    conn.commit()
    return conn

conn = init_db()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # ⚠️【危险】这里演示了 SQL 注入漏洞的根源：直接字符串拼接 ⚠️
    # 如果输入 username 是: ' OR 1=1 --
    # SQL 就会变成: SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = '...'
    sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"执行的 SQL 语句: {sql}")  # 打印出来让你在终端看到注入效果

    cursor = conn.cursor()
    try:
        # execute_script 允许执行多条语句，更危险，但在本例中我们用 standard execute 即可
        cursor.execute(sql)
        user = cursor.fetchone()
        
        if user:
            # 如果注入成功，找到了用户（通常是第一个用户 admin），返回 200
            return jsonify({"status": "success", "msg": f"登录成功！欢迎用户: {user[1]}"}), 200
        else:
            return jsonify({"status": "error", "msg": "用户名或密码错误"}), 401
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)