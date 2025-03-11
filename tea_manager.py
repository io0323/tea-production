from datetime import datetime
import pandas as pd
from database import create_connection

class TeaProductionManager:
    """
    茶生産管理システムのメインクラス
    生産、出荷、在庫管理の機能を提供する
    """
    
    def __init__(self):
        """
        TeaProductionManagerの初期化
        データベース接続を確立する
        """
        self.conn = create_connection()
        
    def add_production(self, tea_type: str, quantity: float, production_date: str = None, quality_check: str = None):
        """
        新しい生産データを追加する
        
        :param tea_type: 茶葉の種類
        :param quantity: 生産量
        :param production_date: 生産日 (YYYY-MM-DD)
        :param quality_check: 品質チェック結果
        :return: 追加された生産データのID
        """
        if production_date is None:
            production_date = datetime.now().strftime('%Y-%m-%d')
            
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO production (tea_type, production_date, quantity, quality_check)
            VALUES (?, ?, ?, ?)
        ''', (tea_type, production_date, quantity, quality_check))
        
        # 在庫テーブルも更新
        production_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO inventory (production_id, quantity)
            VALUES (?, ?)
        ''', (production_id, quantity))
        
        self.conn.commit()
        return production_id
        
    def record_shipment(self, production_id: int, quantity: float, customer_name: str,
                       shipment_date: str = None, customer_contact: str = None):
        """
        出荷データを記録する
        
        :param production_id: 生産データID
        :param quantity: 出荷量
        :param customer_name: 顧客名
        :param shipment_date: 出荷日 (YYYY-MM-DD)
        :param customer_contact: 顧客連絡先
        :return: 追加された出荷データのID
        """
        if shipment_date is None:
            shipment_date = datetime.now().strftime('%Y-%m-%d')
            
        cursor = self.conn.cursor()
        
        # 在庫チェック
        cursor.execute('SELECT quantity FROM inventory WHERE production_id = ?', (production_id,))
        current_stock = cursor.fetchone()
        
        if not current_stock or current_stock[0] < quantity:
            raise ValueError("在庫が不足しています")
            
        # 出荷データを記録
        cursor.execute('''
            INSERT INTO shipment (production_id, shipment_date, quantity, customer_name, customer_contact)
            VALUES (?, ?, ?, ?, ?)
        ''', (production_id, shipment_date, quantity, customer_name, customer_contact))
        
        # 在庫を更新
        cursor.execute('''
            UPDATE inventory
            SET quantity = quantity - ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE production_id = ?
        ''', (quantity, production_id))
        
        self.conn.commit()
        return cursor.lastrowid
        
    def get_inventory_report(self):
        """
        現在の在庫状況レポートを取得する
        
        :return: 在庫状況のDataFrame
        """
        query = '''
            SELECT 
                p.tea_type,
                p.production_date,
                i.quantity as current_stock,
                p.quality_check,
                i.last_updated
            FROM inventory i
            JOIN production p ON i.production_id = p.id
            WHERE i.quantity > 0
        '''
        return pd.read_sql_query(query, self.conn)
        
    def get_shipment_history(self, start_date: str = None, end_date: str = None):
        """
        出荷履歴を取得する
        
        :param start_date: 開始日 (YYYY-MM-DD)
        :param end_date: 終了日 (YYYY-MM-DD)
        :return: 出荷履歴のDataFrame
        """
        query = '''
            SELECT 
                s.shipment_date,
                p.tea_type,
                s.quantity,
                s.customer_name,
                s.customer_contact
            FROM shipment s
            JOIN production p ON s.production_id = p.id
        '''
        
        if start_date and end_date:
            query += f" WHERE s.shipment_date BETWEEN '{start_date}' AND '{end_date}'"
            
        return pd.read_sql_query(query, self.conn)
        
    def update_quality_check(self, production_id: int, quality_check: str, notes: str = None):
        """
        品質チェック結果を更新する
        
        :param production_id: 生産データID
        :param quality_check: 品質チェック結果（A級、B級、C級）
        :param notes: 品質チェックに関する備考
        :return: 更新された行数
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE production
            SET quality_check = ?,
                quality_notes = ?
            WHERE id = ?
        ''', (quality_check, notes, production_id))
        
        self.conn.commit()
        return cursor.rowcount
        
    def get_quality_report(self, start_date: str = None, end_date: str = None):
        """
        品質チェック結果のレポートを取得する
        
        :param start_date: 開始日 (YYYY-MM-DD)
        :param end_date: 終了日 (YYYY-MM-DD)
        :return: 品質チェック結果のDataFrame
        """
        query = '''
            SELECT 
                p.production_date,
                p.tea_type,
                p.quantity,
                p.quality_check,
                p.quality_notes,
                i.quantity as current_stock
            FROM production p
            LEFT JOIN inventory i ON p.id = i.production_id
        '''
        
        if start_date and end_date:
            query += f" WHERE p.production_date BETWEEN '{start_date}' AND '{end_date}'"
            
        return pd.read_sql_query(query, self.conn)
        
    def export_data(self, file_path: str):
        """
        データをCSVファイルにエクスポートする
        
        :param file_path: エクスポート先のファイルパス
        """
        # 生産データのエクスポート
        production_df = pd.read_sql_query('SELECT * FROM production', self.conn)
        production_df.to_csv(f"{file_path}/production.csv", index=False)
        
        # 出荷データのエクスポート
        shipment_df = pd.read_sql_query('SELECT * FROM shipment', self.conn)
        shipment_df.to_csv(f"{file_path}/shipment.csv", index=False)
        
        # 在庫データのエクスポート
        inventory_df = pd.read_sql_query('SELECT * FROM inventory', self.conn)
        inventory_df.to_csv(f"{file_path}/inventory.csv", index=False)
        
    def get_summary_report(self):
        """
        生産、出荷、在庫のサマリーレポートを取得する
        
        :return: サマリーレポートのDataFrame
        """
        query = '''
            SELECT 
                p.tea_type,
                COUNT(DISTINCT p.id) as total_productions,
                SUM(p.quantity) as total_production_quantity,
                COUNT(DISTINCT s.id) as total_shipments,
                SUM(s.quantity) as total_shipment_quantity,
                SUM(i.quantity) as current_stock,
                AVG(CASE WHEN p.quality_check = 'A級' THEN 1 ELSE 0 END) * 100 as quality_a_percentage
            FROM production p
            LEFT JOIN shipment s ON p.id = s.production_id
            LEFT JOIN inventory i ON p.id = i.production_id
            GROUP BY p.tea_type
        '''
        return pd.read_sql_query(query, self.conn)
        
    def __del__(self):
        """
        デストラクタ：データベース接続を閉じる
        """
        if self.conn:
            self.conn.close() 