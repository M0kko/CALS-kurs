import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QLabel, QTabWidget, QHeaderView, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
import psycopg2
from datetime import datetime

# --- КОНФИГУРАЦИЯ ПОДКЛЮЧЕНИЯ ---
DB_CONFIG = {
    "dbname": "ControlInstruments",       # Имя вашей базы данных
    "user": "postgres",       # Ваш пользователь
    "password": "1",   # Ваш пароль
    "host": "localhost",
    "port": "5432"
}

class DatabaseManager:
    """Класс для управления подключением к БД"""
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

    def fetch_query(self, query, params=None):
        if not self.conn: return []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка SQL: {e}")
            self.conn.rollback() # Откат транзакции при ошибке
            return []

    def execute_query(self, query, params=None):
        if not self.conn: return
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()
        except Exception as e:
            print(f"Ошибка SQL Execution: {e}")
            self.conn.rollback()

class KPA_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        if not self.db.conn:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных!")

        self.setWindowTitle("СУБД: Управление жизненным циклом КИПиА")
        self.resize(1200, 700)

        # Основной виджет и Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Создание вкладок
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # --- Вкладка 1: Все приборы (Главная таблица) ---
        self.tab_devices = QWidget()
        self.init_devices_tab()
        self.tabs.addTab(self.tab_devices, "Реестр оборудования")

        # --- Вкладка 2: График поверки (Макрос 1) ---
        self.tab_verification = QWidget()
        self.init_verification_tab()
        self.tabs.addTab(self.tab_verification, "Контроль поверки")

        # --- Вкладка 3: Амортизация (Макрос 2) ---
        self.tab_depreciation = QWidget()
        self.init_depreciation_tab()
        self.tabs.addTab(self.tab_depreciation, "Амортизация и стоимость")

        # Загрузка данных при старте
        self.load_devices_data()
        self.load_verification_data()
        self.load_depreciation_data()

    def init_devices_tab(self):
        layout = QVBoxLayout()
        
        # Фильтры
        filter_layout = QHBoxLayout()
        self.search_input = QComboBox() # Для примера можно сделать поиск
        self.search_input.setPlaceholderText("Поиск...") 
        btn_refresh = QPushButton("Обновить данные")
        btn_refresh.clicked.connect(self.load_devices_data)
        filter_layout.addWidget(QLabel("База данных приборов:"))
        filter_layout.addStretch()
        filter_layout.addWidget(btn_refresh)
        layout.addLayout(filter_layout)

        # Таблица
        self.table_devices = QTableWidget()
        self.table_devices.setColumnCount(8)
        self.table_devices.setHorizontalHeaderLabels([
            "Инв. №", "Тип", "Серийный №", "Место", "Ответственный", "Статус", "Характеристики", "Срок поверки"
        ])
        header = self.table_devices.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_devices)
        
        self.tab_devices.setLayout(layout)

    def init_verification_tab(self):
        layout = QVBoxLayout()
        
        info_label = QLabel("Красным выделены приборы с просроченной поверкой или поверкой в текущем месяце.")
        info_label.setStyleSheet("color: darkred; font-weight: bold;")
        layout.addWidget(info_label)

        self.table_verification = QTableWidget()
        self.table_verification.setColumnCount(6)
        self.table_verification.setHorizontalHeaderLabels([
            "Инв. №", "Тип", "Ответственный", "Локация", "Дата след. поверки", "Статус поверки"
        ])
        header = self.table_verification.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_verification)
        
        btn_calc = QPushButton("Пересчитать график")
        btn_calc.clicked.connect(self.load_verification_data)
        layout.addWidget(btn_calc)
        
        self.tab_verification.setLayout(layout)

    def init_depreciation_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Расчет текущей остаточной стоимости оборудования:"))
        
        self.table_depr = QTableWidget()
        self.table_depr.setColumnCount(6)
        self.table_depr.setHorizontalHeaderLabels([
            "Инв. №", "Тип", "Дата покупки", "Срок (мес)", "Исп. (мес)", "Ост. Стоимость (Руб)"
        ])
        header = self.table_depr.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_depr)
        
        self.tab_depreciation.setLayout(layout)

    # --- ЛОГИКА ЗАГРУЗКИ ДАННЫХ ---

    def load_devices_data(self):
        """Загрузка всех приборов с JOIN таблицами"""
        query = """
            SELECT 
                d.inventory_number, dt.type_name, d.serial_number, 
                l.name, e.last_name || ' ' || left(e.first_name, 1) || '.', 
                d.status, d.passport_data, d.last_verification_date
            FROM devices d
            JOIN device_types dt ON d.type_id = dt.type_id
            JOIN locations l ON d.location_id = l.location_id
            JOIN employees e ON d.responsible_id = e.employee_id
            ORDER BY d.device_id;
        """
        rows = self.db.fetch_query(query)
        self.fill_table(self.table_devices, rows)

    def load_verification_data(self):
        """Использование SQL VIEW для расчета поверки"""
        query = "SELECT * FROM view_verification_schedule ORDER BY next_verification_date ASC"
        rows = self.db.fetch_query(query)
        
        self.table_verification.setRowCount(0)
        current_date = datetime.now().date()
        
        for row_idx, row_data in enumerate(rows):
            # row_data: id, inv, type, last_date, interval, NEXT_DATE, loc, resp
            self.table_verification.insertRow(row_idx)
            
            # Отображаем нужные поля (Инв, Тип, Отв, Локация, Дата след.)
            display_data = [row_data[1], row_data[2], row_data[7], row_data[6], str(row_data[5])]
            
            next_ver_date = row_data[5]
            days_left = (next_ver_date - current_date).days
            
            status_text = "OK"
            color = None
            
            if days_left < 0:
                status_text = f"Просрочено ({abs(days_left)} дн.)"
                color = Qt.GlobalColor.red
            elif days_left < 30:
                status_text = f"Поверить в этом месяце"
                color = Qt.GlobalColor.yellow
            else:
                status_text = f"Через {days_left} дн."

            display_data.append(status_text)

            for col_idx, val in enumerate(display_data):
                item = QTableWidgetItem(str(val))
                if color:
                    item.setBackground(color)
                self.table_verification.setItem(row_idx, col_idx, item)

    def load_depreciation_data(self):
        """Использование SQL VIEW для расчета стоимости"""
        query = "SELECT * FROM view_depreciation"
        rows = self.db.fetch_query(query)
        self.fill_table(self.table_depr, rows)

    def fill_table(self, table_widget, data):
        table_widget.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            table_widget.insertRow(row_idx)
            for col_idx, val in enumerate(row_data):
                # Если это JSON (паспорт), конвертируем в строку красиво
                if isinstance(val, dict):
                    val = ", ".join([f"{k}: {v}" for k, v in val.items()])
                
                item = QTableWidgetItem(str(val))
                table_widget.setItem(row_idx, col_idx, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Стилизация (Dark Theme подобная Fusion)
    app.setStyle("Fusion")
    
    window = KPA_App()
    window.show()
    sys.exit(app.exec())