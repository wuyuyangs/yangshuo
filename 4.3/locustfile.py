from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # 模拟用户在执行任务之间会思考 1 到 3 秒
    wait_time = between(1, 3)

    @task
    def order_book(self):
        # 发送 POST 请求到 /order
        self.client.post(
            "/order", 
            json={"item": "book", "qty": 1},
            name="Create Order" # 在统计表中显示的名称，方便聚合数据
        )