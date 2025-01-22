import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QInputDialog, QMessageBox, QWidget, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
import pandas as pd

# --- Ventana de Login ---
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 350, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #003366;
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #cccccc;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #004488;
            }
        """)
        self.setWindowIcon(QIcon('PJF.ico'))  # Asumiendo que tienes un archivo de icono
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.check_credentials)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def check_credentials(self):
        if self.username_input.text() == "admin" and self.password_input.text() == "admin":
            self.accept()
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
            self.username_label.setText("¡Usuario o contraseña inválidos!")

# --- Ventana Principal y CRUD (Crear, Modificar, Buscar, Eliminar) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestión de Productos')
        self.setGeometry(100, 100, 900, 600)
        self.create_database()
        self.setWindowIcon(QIcon('PJF.ico'))  # Asignar icono a la ventana principal
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e6e6e6;
            }
            QPushButton {
                background-color: #005b96;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                min-width: 140px;  
                text-align: center;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #004080;
            }
            QPushButton:pressed {
                background-color: #003060;
            }
        """)

        self.layout = QVBoxLayout()

        # Logo en el centro de la ventana principal
        logo_label = QLabel(self)
        pixmap = QPixmap('PJF.png')  # Asegúrate de tener un archivo de logo
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Botones de acciones con un tamaño más pequeño y mejor alineados
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Espaciado entre botones

        self.create_button = self.create_button_with_icon('Crear Producto', 'PJFS.ico', self.create_product)
        self.update_button = self.create_button_with_icon('Modificar Producto', 'PJFS.ico', self.update_product)
        self.search_button = self.create_button_with_icon('Buscar Producto', 'PJFS.ico', self.search_product)
        self.delete_button = self.create_button_with_icon('Eliminar Producto', 'PJFS.ico', self.delete_product)
        self.export_button = self.create_button_with_icon('Generar Reporte', 'PJFS.ico', self.export_to_excel)

        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.export_button)

        self.layout.addWidget(logo_label)  # Añadimos el logo al layout
        self.layout.addLayout(button_layout)  # Añadimos los botones a la ventana principal

        # Contenedor principal
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def create_button_with_icon(self, text, icon_name, action):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_name))  # Asignar icono
        button.clicked.connect(action)
        return button

    def create_database(self):
        try:
            self.conn = sqlite3.connect('products.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT,
                                    description TEXT,
                                    code TEXT UNIQUE,
                                    category TEXT,
                                    location TEXT
                                )''')
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error de Conexión', f'Error al crear la base de datos: {e}')
            self.close()

    def execute_db_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error de Base de Datos', f'Error al ejecutar la consulta: {e}')

    def insert_product(self, product_data):
        query = '''INSERT INTO products (name, description, code, category, location)
                   VALUES (?, ?, ?, ?, ?)'''
        self.execute_db_query(query, product_data)

    def update_product_in_db(self, product_data, code):
        query = '''UPDATE products
                   SET name = ?, description = ?, code=?, category = ?, location = ?
                   WHERE code = ?'''
        
        # Asegúrate de que estamos pasando los parámetros correctamente
        self.execute_db_query(query, (*product_data, code))

    def create_product(self):
        dialog = ProductFormDialog(self, 'Crear Producto')
        if dialog.exec_():
            product_data = dialog.get_product_data()
            self.insert_product(product_data)
            QMessageBox.information(self, 'Éxito', 'Producto creado exitosamente')

    def update_product(self):
        code, ok = self.get_code_from_user('Modificar Producto')
        if ok:
            self.cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
            result = self.cursor.fetchone()
            if result:
                dialog = ProductFormDialog(self, 'Modificar Producto', product_data=result)
                if dialog.exec_():
                    updated_data = dialog.get_product_data()
                    self.update_product_in_db(updated_data, code)
                    QMessageBox.information(self, 'Éxito', 'Producto modificado exitosamente')
            else:
                QMessageBox.warning(self, 'Error', 'Producto no encontrado')

    def search_product(self):
        dialog = SearchProductDialog(self)
        dialog.exec_()

    def delete_product(self):
        code, ok = self.get_code_from_user('Eliminar Producto')
        if ok:
            self.cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
            result = self.cursor.fetchone()
            if result:
                reply = QMessageBox.question(self, 'Confirmar', '¿Estás seguro de eliminar este producto?', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.cursor.execute('DELETE FROM products WHERE code = ?', (code,))
                    self.conn.commit()
                    QMessageBox.information(self, 'Éxito', 'Producto eliminado exitosamente')
            else:
                QMessageBox.warning(self, 'Error', 'Producto no encontrado')

    def export_to_excel(self):
        products = pd.read_sql_query("SELECT * FROM products", self.conn)
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            products.to_excel(file_name, index=False)
            QMessageBox.information(self, 'Éxito', 'Reporte generado exitosamente')

    def get_code_from_user(self, action):
        code, ok = QInputDialog.getText(self, action, 'Ingresa el código del producto:')
        return code, ok

# --- Formulario de Producto (Formulario para Crear/Modificar) ---
class ProductFormDialog(QDialog):
    def __init__(self, parent, action, product_data=None):
        super().__init__(parent)
        self.setWindowTitle(action)
        self.setGeometry(200, 200, 450, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #004488;
            }
        """)
        self.setWindowIcon(QIcon('PJF.ico'))  # Asignar icono
        self.product_data = product_data
        self.initUI()

    def initUI(self):
        self.layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.code_input = QLineEdit(self)
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Computación", "Papelería", "Muebles", "Herramientas"])
        self.location_input = QLineEdit(self)

        if self.product_data:
            self.name_input.setText(self.product_data[1])
            self.description_input.setText(self.product_data[2])
            self.code_input.setText(self.product_data[3])
            self.category_input.setCurrentText(self.product_data[4])
            self.location_input.setText(self.product_data[5])
            self.code_input.setReadOnly(True)

        self.layout.addRow("Nombre:", self.name_input)
        self.layout.addRow("Descripción:", self.description_input)
        self.layout.addRow("Código:", self.code_input)
        self.layout.addRow("Categoría:", self.category_input)
        self.layout.addRow("Ubicación:", self.location_input)

        self.save_button = QPushButton('Guardar', self)
        self.save_button.setIcon(QIcon('PJF.ico'))  # Icono en el botón
        self.save_button.clicked.connect(self.save_product)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_product(self):
        name = self.name_input.text()
        description = self.description_input.text()
        code = self.code_input.text()
        category = self.category_input.currentText()
        location = self.location_input.text()

        if not name or not description or not code or not category or not location:
            QMessageBox.warning(self, 'Error', 'Por favor, completa todos los campos.')
            return

        self.accept()

    def get_product_data(self):
        return (self.name_input.text(), self.description_input.text(), self.code_input.text(), self.category_input.currentText(), self.location_input.text())

# --- Ventana de Búsqueda ---
class SearchProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Buscar Producto")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QTableWidget {
                border: 1px solid #ccc;
                font-size: 14px;
            }
            QPushButton {
                background-color: #003366;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #004488;
            }
        """)
        self.setWindowIcon(QIcon('PJF.ico'))  # Asumiendo que tienes un archivo de icono
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar por código o nombre...")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Código", "Categoría", "Ubicación"])
        self.result_table.setRowCount(0)

        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.result_table)

        # Botón para mostrar todos los productos
        self.show_all_button = QPushButton("Mostrar Todo", self)
        self.show_all_button.clicked.connect(self.show_all_products)
        self.layout.addWidget(self.show_all_button)

        # Botón para cerrar la ventana de búsqueda
        self.close_button = QPushButton("Cerrar", self)
        self.close_button.clicked.connect(self.accept)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def on_search_text_changed(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.result_table.setRowCount(0)  # Limpiar los resultados si no hay texto
        else:
            self.search_products("name", search_text)

    def search_products(self, column, search_text):
        query = f"SELECT * FROM products WHERE {column} LIKE ?"
        self.parent().cursor.execute(query, ('%' + search_text + '%',))
        results = self.parent().cursor.fetchall()

        # Limpiar la tabla de resultados antes de agregar nuevos datos
        self.result_table.setRowCount(0)

        # Mostrar los resultados en la tabla
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def show_all_products(self):
        query = "SELECT * FROM products"
        self.parent().cursor.execute(query)
        results = self.parent().cursor.fetchall()

        # Limpiar la tabla de resultados antes de agregar nuevos datos
        self.result_table.setRowCount(0)

        # Mostrar todos los productos en la tabla
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Mostrar ventana de login
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        # Si el login es correcto, mostrar la ventana principal
        main_window = MainWindow()
        main_window.show()
    
    sys.exit(app.exec_())