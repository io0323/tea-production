import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget,
                           QVBoxLayout, QHBoxLayout, QFormLayout, 
                           QPushButton, QLineEdit, QLabel, QDateEdit,
                           QTableWidget, QTableWidgetItem, QMessageBox,
                           QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit)
from PyQt5.QtCore import Qt, QDate
from tea_manager import TeaProductionManager
import pandas as pd

class TeaProductionApp(QMainWindow):
    """
    茶生産管理システムのメインウィンドウ
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('茶生産管理システム')
        self.setGeometry(100, 100, 1200, 800)
        
        # TeaProductionManagerのインスタンスを作成
        self.manager = TeaProductionManager()
        
        # メインウィジェットとレイアウトの設定
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # タブウィジェットの作成
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # 各タブの作成
        self.production_tab = ProductionTab(self.manager)
        self.shipment_tab = ShipmentTab(self.manager)
        self.inventory_tab = InventoryTab(self.manager)
        self.report_tab = ReportTab(self.manager)
        
        # タブの追加
        tabs.addTab(self.production_tab, '生産管理')
        tabs.addTab(self.shipment_tab, '出荷管理')
        tabs.addTab(self.inventory_tab, '在庫管理')
        tabs.addTab(self.report_tab, 'レポート')
        
        # 更新ボタン
        update_button = QPushButton('データ更新')
        update_button.clicked.connect(self.update_all_tabs)
        layout.addWidget(update_button)

    def update_all_tabs(self):
        """全タブのデータを更新する"""
        self.production_tab.update_data()
        self.shipment_tab.update_data()
        self.inventory_tab.update_data()
        self.report_tab.update_data()

class ProductionTab(QWidget):
    """生産管理タブ"""
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 入力フォーム
        form_layout = QFormLayout()
        
        self.tea_type = QComboBox()
        self.tea_type.addItems(['煎茶', '玉露', '抹茶', 'ほうじ茶'])
        
        self.quantity = QDoubleSpinBox()
        self.quantity.setRange(0, 10000)
        self.quantity.setSuffix(' kg')
        
        self.production_date = QDateEdit()
        self.production_date.setDate(QDate.currentDate())
        
        self.quality_check = QComboBox()
        self.quality_check.addItems(['A級', 'B級', 'C級'])
        
        self.quality_notes = QTextEdit()
        
        form_layout.addRow('茶葉の種類:', self.tea_type)
        form_layout.addRow('生産量:', self.quantity)
        form_layout.addRow('生産日:', self.production_date)
        form_layout.addRow('品質評価:', self.quality_check)
        form_layout.addRow('品質メモ:', self.quality_notes)
        
        # 登録ボタン
        submit_button = QPushButton('生産データ登録')
        submit_button.clicked.connect(self.register_production)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', '茶葉の種類', '生産日', '数量', '品質評価', '品質メモ'])
        
        layout.addLayout(form_layout)
        layout.addWidget(submit_button)
        layout.addWidget(self.table)
        
        self.update_data()
        
    def register_production(self):
        """生産データを登録する"""
        try:
            production_id = self.manager.add_production(
                tea_type=self.tea_type.currentText(),
                quantity=self.quantity.value(),
                production_date=self.production_date.date().toString('yyyy-MM-dd'),
                quality_check=self.quality_check.currentText()
            )
            
            # 品質メモの更新
            self.manager.update_quality_check(
                production_id=production_id,
                quality_check=self.quality_check.currentText(),
                notes=self.quality_notes.toPlainText()
            )
            
            QMessageBox.information(self, '成功', '生産データを登録しました')
            self.update_data()
            
        except Exception as e:
            QMessageBox.warning(self, 'エラー', f'登録に失敗しました: {str(e)}')
    
    def update_data(self):
        """テーブルのデータを更新する"""
        df = self.manager.get_quality_report()
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['tea_type'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['production_date'])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['quantity']} kg"))
            self.table.setItem(i, 4, QTableWidgetItem(str(row['quality_check'])))
            self.table.setItem(i, 5, QTableWidgetItem(str(row['quality_notes'])))

class ShipmentTab(QWidget):
    """出荷管理タブ"""
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 入力フォーム
        form_layout = QFormLayout()
        
        self.production_id = QSpinBox()
        self.quantity = QDoubleSpinBox()
        self.quantity.setRange(0, 10000)
        self.quantity.setSuffix(' kg')
        
        self.customer_name = QLineEdit()
        self.customer_contact = QLineEdit()
        self.shipment_date = QDateEdit()
        self.shipment_date.setDate(QDate.currentDate())
        
        form_layout.addRow('生産ID:', self.production_id)
        form_layout.addRow('出荷量:', self.quantity)
        form_layout.addRow('顧客名:', self.customer_name)
        form_layout.addRow('連絡先:', self.customer_contact)
        form_layout.addRow('出荷日:', self.shipment_date)
        
        # 登録ボタン
        submit_button = QPushButton('出荷データ登録')
        submit_button.clicked.connect(self.register_shipment)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['出荷日', '茶葉の種類', '数量', '顧客名', '連絡先'])
        
        layout.addLayout(form_layout)
        layout.addWidget(submit_button)
        layout.addWidget(self.table)
        
        self.update_data()
        
    def register_shipment(self):
        """出荷データを登録する"""
        try:
            self.manager.record_shipment(
                production_id=self.production_id.value(),
                quantity=self.quantity.value(),
                customer_name=self.customer_name.text(),
                customer_contact=self.customer_contact.text(),
                shipment_date=self.shipment_date.date().toString('yyyy-MM-dd')
            )
            
            QMessageBox.information(self, '成功', '出荷データを登録しました')
            self.update_data()
            
        except Exception as e:
            QMessageBox.warning(self, 'エラー', f'登録に失敗しました: {str(e)}')
    
    def update_data(self):
        """テーブルのデータを更新する"""
        df = self.manager.get_shipment_history()
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['shipment_date'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['tea_type'])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row['quantity']} kg"))
            self.table.setItem(i, 3, QTableWidgetItem(str(row['customer_name'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(row['customer_contact'])))

class InventoryTab(QWidget):
    """在庫管理タブ"""
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['茶葉の種類', '生産日', '在庫量', '品質評価', '最終更新'])
        
        layout.addWidget(self.table)
        
        self.update_data()
    
    def update_data(self):
        """テーブルのデータを更新する"""
        df = self.manager.get_inventory_report()
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['tea_type'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['production_date'])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row['current_stock']} kg"))
            self.table.setItem(i, 3, QTableWidgetItem(str(row['quality_check'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(row['last_updated'])))

class ReportTab(QWidget):
    """レポートタブ"""
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            '茶葉の種類', '総生産回数', '総生産量', '総出荷回数',
            '総出荷量', '現在庫', 'A級品率(%)'
        ])
        
        # エクスポートボタン
        export_button = QPushButton('データをエクスポート')
        export_button.clicked.connect(self.export_data)
        
        layout.addWidget(self.table)
        layout.addWidget(export_button)
        
        self.update_data()
    
    def update_data(self):
        """テーブルのデータを更新する"""
        df = self.manager.get_summary_report()
        self.table.setRowCount(len(df))
        
        for i, row in df.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['tea_type'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['total_productions'])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row['total_production_quantity']} kg"))
            self.table.setItem(i, 3, QTableWidgetItem(str(row['total_shipments'])))
            self.table.setItem(i, 4, QTableWidgetItem(f"{row['total_shipment_quantity']} kg"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{row['current_stock']} kg"))
            self.table.setItem(i, 6, QTableWidgetItem(f"{row['quality_a_percentage']:.1f}%"))
    
    def export_data(self):
        """データをエクスポートする"""
        try:
            self.manager.export_data('exports')
            QMessageBox.information(self, '成功', 'データをエクスポートしました')
        except Exception as e:
            QMessageBox.warning(self, 'エラー', f'エクスポートに失敗しました: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = TeaProductionApp()
    window.show()
    sys.exit(app.exec_()) 