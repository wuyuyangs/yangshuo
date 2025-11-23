# file: library_system.py

class LibrarySystem:
    def __init__(self):
        # 初始化一些模拟数据
        # 用户列表 (Set集合，模拟数据库)
        self.users = {"Alice", "Bob", "Charlie"}
        
        # 图书库存 (字典: 书名 -> 库存数量)
        self.books = {
            "Python编程": 5,
            "数据结构": 1,
            "绝版古籍": 0  # 库存为 0，不可借
        }

    def borrow_book(self, username, book_name):
        """
        执行借书操作
        :param username: 借书人姓名
        :param book_name: 书名
        :return: 成功返回 True，失败抛出异常
        """
        # 1. 校验用户是否存在
        if username not in self.users:
            raise ValueError(f"用户 '{username}' 不存在")

        # 2. 校验图书是否存在
        if book_name not in self.books:
            raise ValueError(f"图书 '{book_name}' 未收录")

        # 3. 校验库存是否充足
        if self.books[book_name] <= 0:
            raise ValueError(f"图书 '{book_name}' 库存不足")

        # 4. 执行借书逻辑（库存减少）
        self.books[book_name] -= 1
        print(f"✅ {username} 成功借阅 《{book_name}》，剩余库存: {self.books[book_name]}")
        return True