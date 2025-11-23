# file: test_browser.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_login_page(browser_type="chrome"):
    print(f"--- 正在启动 {browser_type} 浏览器进行测试 ---")
    
    driver = None
    try:
        # 1. 根据参数启动不同的浏览器
        if browser_type == "chrome":
            # Selenium 4.6+ 会自动下载匹配的 ChromeDriver，无需手动配置路径
            driver = webdriver.Chrome() 
        elif browser_type == "firefox":
            driver = webdriver.Firefox()
        elif browser_type == "edge":
            driver = webdriver.Edge()
            
        # 2. 访问页面
        driver.get("http://127.0.0.1:5000/login")
        
        # 3. 观察：暂停 2 秒让你看清楚浏览器打开了
        time.sleep(2)
        
        # 4. 断言验证：检查页面源代码中是否有 "用户登录"
        page_source = driver.page_source
        if "用户登录" in page_source:
            print(f"✅ [{browser_type}] 测试通过：找到了登录关键字。")
        else:
            print(f"❌ [{browser_type}] 测试失败：未找到关键字。")
            
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        
    finally:
        # 5. 清理：无论成功失败，务必关闭浏览器
        if driver:
            driver.quit()

if __name__ == "__main__":
    # 你可以在这里切换测试不同的浏览器
    test_login_page("chrome")
