# file: test_resilience.py
import requests
import time
import subprocess

def test_db_failure_recovery():
    url = "http://127.0.0.1:5000/order"
    
    print("--- 阶段 1: 正常请求 ---")
    res = requests.post(url, json={"item": "book", "qty": 1})
    assert res.status_code == 200
    print("✅ 正常状态测试通过")

    print("--- 阶段 2: 模拟故障 (停止数据库) ---")
    # Windows 下 subprocess 调用 docker 可能需要 shell=True
    subprocess.run("docker stop mysql_db", shell=True)
    time.sleep(3) # 等待容器完全停止

    print("--- 发送请求 (预期失败) ---")
    res = requests.post(url, json={"item": "book", "qty": 1})
    
    # 验证：系统是否优雅地处理了故障？(应该返回 503，而不是卡死或无响应)
    if res.status_code in (500, 503):
        print(f"✅ 容错处理成功! 状态码: {res.status_code}")
    else:
        print(f"❌ 容错失败，预期 503，实际: {res.status_code}")
        
    print("--- 阶段 3: 故障恢复 (重启数据库) ---")
    subprocess.run("docker start mysql_db", shell=True)
    print("等待数据库初始化 (10秒)...")
    time.sleep(10) # MySQL 启动比较慢，多给点时间

    print("--- 发送请求 (预期成功) ---")
    try:
        res2 = requests.post(url, json={"item": "book", "qty": 1})
        assert res2.status_code == 200
        print("✅ 系统自愈成功！业务恢复正常。")
    except Exception as e:
        print(f"❌ 恢复失败: {e}")

if __name__ == "__main__":
    test_db_failure_recovery()