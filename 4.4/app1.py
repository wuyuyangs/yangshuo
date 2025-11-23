# file: app.py
from flask import Flask

app = Flask(__name__)

@app.route('/login')
def login():
    # 返回一段简单的 HTML，包含 "用户登录" 字样供测试脚本检测
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Login Page</title></head>
    <body>
        <h1>用户登录系统</h1>
        <form>
            用户名: <input type="text" name="username"><br>
            密码: <input type="password" name="password"><br>
            <button type="submit">登录</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(port=5000)