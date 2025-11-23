# file: test_library.py
import pytest
from library_system import LibrarySystem

# --- Fixture: 测试夹具 ---
# 它的作用是为每个测试函数提供一个全新的 LibrarySystem 实例
@pytest.fixture
def library():
    return LibrarySystem()

# --- 单元测试用例 (5个) ---

# 用例 1: 正常借书流程
def test_borrow_success(library):
    # Alice 借一本有库存的书
    result = library.borrow_book("Alice", "Python编程")
    assert result is True

# 用例 2: 验证库存减少逻辑
def test_inventory_decrease(library):
    # "数据结构" 只有 1 本
    initial_stock = library.books["数据结构"]
    library.borrow_book("Bob", "数据结构")
    
    # 断言：借完后库存应该少 1
    assert library.books["数据结构"] == initial_stock - 1
    # 断言：现在库存应该是 0
    assert library.books["数据结构"] == 0

# 用例 3: 异常测试 - 用户不存在
def test_user_not_found(library):
    # 使用 pytest.raises 捕获预期的异常
    with pytest.raises(ValueError, match="用户 'Hacker' 不存在"):
        library.borrow_book("Hacker", "Python编程")

# 用例 4: 异常测试 - 图书不存在
def test_book_not_found(library):
    with pytest.raises(ValueError, match="图书 '哈利波特' 未收录"):
        library.borrow_book("Alice", "哈利波特")

# 用例 5: 异常测试 - 库存不足
def test_book_out_of_stock(library):
    # "绝版古籍" 初始化库存为 0
    with pytest.raises(ValueError, match="库存不足"):
        library.borrow_book("Charlie", "绝版古籍")

# (可选) 用例 6: 边界测试 - 借走最后一本书后再借
def test_borrow_until_empty(library):
    # 先借走唯一的 "数据结构"
    library.borrow_book("Alice", "数据结构")
    assert library.books["数据结构"] == 0
    
    # 第二个人再来借同一本书，应该报错
    with pytest.raises(ValueError, match="库存不足"):
        library.borrow_book("Bob", "数据结构")