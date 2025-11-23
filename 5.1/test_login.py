import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- 1. 测试夹具 (Setup/Teardown) ---
@pytest.fixture
def driver():
    # 自动下载并设置 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(5) # 隐式等待5秒
    
    # 打开目标网站
    driver.get("https://www.saucedemo.com/")
    
    yield driver # 这里开始执行测试函数
    
    # 测试结束后关闭浏览器
    driver.quit()

# --- 2. 测试逻辑 ---

# 用例 1: 登录成功
def test_login_success(driver):
    # 定位元素并操作
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 验证（断言）
    assert "inventory.html" in driver.current_url
    print("\n[通过] 标准用户登录成功")

# 用例 2: 密码错误
def test_login_password_failure(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_pass")
    driver.find_element(By.ID, "login-button").click()
    
    # 获取错误提示文本
    error_msg = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    assert "Username and password do not match" in error_msg
    print("\n[通过] 密码错误拦截成功")

# 用例 3: 锁定用户 (演示发现 Bug 或特定逻辑)
def test_locked_out_user(driver):
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    error_msg = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    assert "locked out" in error_msg
    print("\n[通过] 锁定用户提示正确")

# 用例 4: 空字段 (演示一个故意失败的测试，用于生成缺陷报告)
def test_empty_fields(driver):
    driver.find_element(By.ID, "login-button").click()
    
    error_msg = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    # 假设我们预期错误信息是中文，但实际是英文，这里断言会失败
    # 注意：这里是为了演示生成“失败报告”，实际代码中不要故意写错
    try:
        assert "用户名是必填项" in error_msg 
    except AssertionError:
        print("\n[失败] 错误信息语言不匹配")
        raise # 重新抛出异常以便 pytest 捕捉