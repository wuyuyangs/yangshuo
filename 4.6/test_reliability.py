# file: test_reliability.py
import time
import requests

def test_reliability():
    url = "http://127.0.0.1:5000/order"
    total_requests = 1000
    success_count = 0
    fail_count = 0
    
    print(f"--- 开始可靠性测试: 计划执行 {total_requests} 次请求 ---")
    start = time.time()
    
    for i in range(total_requests):
        try:
            res = requests.post(url, json={"item": "book", "qty": 1})
            if res.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
                print(f"请求 #{i} 失败: {res.status_code}")
        except Exception as e:
            fail_count += 1
            print(f"请求 #{i} 异常: {e}")
            
        # 每 100 次打印一下进度
        if (i + 1) % 100 == 0:
            print(f"已完成 {i + 1} 次...")

    end = time.time()
    duration = end - start
    
    print("\n--- 测试报告 ---")
    print(f"总耗时: {duration:.2f} 秒")
    print(f"平均TPS: {total_requests / duration:.2f}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    
    assert fail_count == 0, "可靠性测试未通过，存在失败请求"

if __name__ == "__main__":
    test_reliability()