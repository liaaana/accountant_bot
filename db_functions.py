import sqlite3


class Accountant:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def does_user_exist(self, user_id):
        """find out if the user exists"""
        ans = self.cursor.execute("""SELECT id FROM users WHERE user_id = ?""", (user_id,)).fetchone()
        return ans

    def add_user(self, user_id):
        """Adding a user to the database"""
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        self.connect.commit()

    def delete_user(self, user_id):
        """Deleting a user from the database"""
        self.cursor.execute("DELETE FROM users WHERE id = ?", (self.get_id_by_user_id(user_id),))
        self.connect.commit()

    def get_id_by_user_id(self, user_id):
        """Getting id by user_id"""
        ans = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return ans.fetchone()[0]

    def get_categories_by_user_id(self, user_id):
        """Getting categories by user_id"""
        ans = self.cursor.execute("SELECT * FROM categories WHERE user_id = ?", (self.get_id_by_user_id(user_id),))
        return ans.fetchall()

    def get_category_by_id(self, category_id):
        """Getting category by id"""
        ans = self.cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        return ans.fetchone()

    def add_category(self, user_id, name):
        """Adding a category to the database"""
        self.cursor.execute("INSERT INTO categories (user_id, name) VALUES (?, ?)",
                            (self.get_id_by_user_id(user_id), name))
        self.connect.commit()

    def delete_categories(self, user_id):
        """Deleting categories from the database"""
        self.cursor.execute("DELETE FROM categories WHERE user_id = ?", (self.get_id_by_user_id(user_id),))
        self.connect.commit()

    def add_revenue_or_expense(self, user_id, category_id, operation_type, amount):
        """Adding a revenue or expense to the database"""
        self.cursor.execute(
            "INSERT INTO revenues_and_expenses (user_id, category_id, type, amount) VALUES (?, ?, ?, ?)",
            (self.get_id_by_user_id(user_id), category_id, operation_type, amount))
        self.connect.commit()

    def get_revenues_and_expenses_by_user_id(self, user_id):
        """Getting revenues and expenses by user_id"""
        ans = self.cursor.execute("SELECT * FROM revenues_and_expenses WHERE user_id = ?",
                                  (self.get_id_by_user_id(user_id),))
        return ans.fetchall()

    def delete_all_revenues_and_expenses(self, user_id):
        """Deleting expenses and revenues from the database"""
        self.cursor.execute("DELETE FROM revenues_and_expenses WHERE user_id = ?", (self.get_id_by_user_id(user_id),))
        self.connect.commit()

    def close(self):
        """Close the database connection"""
        self.connect.close()
