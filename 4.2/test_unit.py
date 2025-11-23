import unittest
from app import check_and_lock_inventory, process_payment, inventory, prices

class TestOrderSystemUnits(unittest.TestCase):
    """
    单元测试：只测试 Python 函数逻辑，不涉及 HTTP 请求
    """

    def setUp(self):
        # 每个测试前重置库存，防止测试相互干扰
        inventory["book"] = 10
        inventory["pen"] = 50

    def test_inventory_check_success(self):
        """测试库存充足"""
        self.assertTrue(check_and_lock_inventory("book", 5))

    def test_inventory_check_fail_item(self):
        """测试商品不存在"""
        with self.assertRaises(ValueError):
            check_and_lock_inventory("iphone", 1)

    def test_inventory_check_fail_qty(self):
        """测试库存不足"""
        with self.assertRaises(ValueError):
            check_and_lock_inventory("book", 100)

    def test_payment_success(self):
        """测试支付成功 (单价20 * 2 = 40)"""
        success, msg = process_payment("book", 2, 40)
        self.assertTrue(success)
        self.assertEqual(msg, "支付成功")

    def test_payment_fail(self):
        """测试支付金额不足"""
        success, msg = process_payment("book", 2, 10) # 应该是40
        self.assertFalse(success)
        self.assertIn("支付金额不足", msg)

if __name__ == '__main__':
    unittest.main()