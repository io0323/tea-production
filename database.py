import sqlite3
from sqlite3 import Error

def create_connection():
    """
    SQLiteデータベースへの接続を作成する
    :return: Connection オブジェクト
    """
    try:
        conn = sqlite3.connect('tea_production.db')
        return conn
    except Error as e:
        print(f"データベース接続エラー: {e}")
        return None

def create_tables(conn):
    """
    必要なテーブルを作成する
    :param conn: データベース接続オブジェクト
    """
    try:
        cursor = conn.cursor()
        
        # 茶葉の生産テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tea_type TEXT NOT NULL,
                production_date DATE NOT NULL,
                quantity REAL NOT NULL,
                quality_check TEXT,
                quality_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 出荷テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                production_id INTEGER,
                shipment_date DATE NOT NULL,
                quantity REAL NOT NULL,
                customer_name TEXT NOT NULL,
                customer_contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (production_id) REFERENCES production (id)
            )
        ''')
        
        # 在庫テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                production_id INTEGER,
                quantity REAL NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (production_id) REFERENCES production (id)
            )
        ''')
        
        conn.commit()
    except Error as e:
        print(f"テーブル作成エラー: {e}")

if __name__ == '__main__':
    # データベース接続とテーブル作成
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
        conn.close()
    else:
        print("データベース接続を確立できませんでした。") 