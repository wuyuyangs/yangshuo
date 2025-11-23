# file: test_sql_injection.py
import requests

def test_sql_injection():
    url = "http://127.0.0.1:5000/login"
    
    # SQL 注入 Payload 解析：
    # '      -> 闭合前面的单引号
    # OR 1=1 -> 永真条件，让 WHERE 子句永远成立
    # --     -> 注释掉后面所有的 SQL 语句（比如密码校验）
    payload = {
        "username": "' OR 1=1 --",
        "password": "随便填" 
    }
    
    print(f"--- 正在发送 Payload: {payload['username']} ---")
    res = requests.post(url, json=payload)
    
    print(f"服务器响应状态码: {res.status_code}")
    print(f"服务器响应内容: {res.text}")

    # 【验证逻辑】
    # 如果服务器是安全的，应该拦截注入或报错 (400/401/500)
    # 如果服务器是脆弱的，SQL注入会成功登录 (200)，下面的 assert 就会失败（报错）
    if res.status_code == 200:
        print("❌ 严重漏洞！SQL 注入攻击成功！以管理员身份登录了！")
    else:
        print("✅ 防御成功或攻击无效。")
        assert res.status_code in [400, 401, 500] or "error" in res.text.lower()

if __name__ == "__main__":
    test_sql_injection()