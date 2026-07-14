import sqlite3

class Database:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Foydalanuvchilar jadvalini yaratish
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                full_name TEXT,
                referrer_id INTEGER DEFAULT NULL,
                referral_count INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def add_user(self, telegram_id, full_name, referrer_id=None):
        # Foydalanuvchini bazaga qo'shish
        try:
            self.cursor.execute(
                "INSERT INTO users (telegram_id, full_name, referrer_id) VALUES (?, ?, ?)",
                (telegram_id, full_name, referrer_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Agar foydalanuvchi allaqachon bazada bo'lsa
            return False

    def user_exists(self, telegram_id):
        self.cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,))
        return self.cursor.fetchone() is not None

    def get_referral_count(self, telegram_id):
        self.cursor.execute("SELECT referral_count FROM users WHERE telegram_id = ?", (telegram_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def increment_referral(self, referrer_id):
        # Taklif qilgan odamning hisoblagichini 1 taga oshirish
        self.cursor.execute(
            "UPDATE users SET referral_count = referral_count + 1 WHERE telegram_id = ?",
            (referrer_id,)
        )
        self.conn.commit()