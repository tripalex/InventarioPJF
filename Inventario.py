import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QInputDialog, QMessageBox, QWidget, QFileDialog, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap
import pandas as pd

# --- Ventana de Login ---
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrada")
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
        self.setWindowIcon(QIcon('PJF.ico'))
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

# --- Ventana Principal y CRUD ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de inventario v1')
        self.setGeometry(100, 100, 900, 600)
        self.create_database()
        self.setWindowIcon(QIcon('Iconos/PJF.ico'))  # Asignar icono a la ventana principal
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
            #exitButton {
                background-color: #ff3333;  /* Rojo */
                color: white;  /* Texto blanco */
            }
            #exitButton:hover {
                background-color: #ff6666;  /* Rojo más claro al pasar el mouse */
            }
            #exitButton:pressed {
                background-color: #cc0000;  /* Rojo oscuro al presionar */
            }
        """)

        self.layout = QVBoxLayout()

        # Logo en el centro de la ventana principal
        logo_label = QLabel(self)
        pixmap = QPixmap('Imagenes/PJF.png')  # Asegúrate de tener un archivo de logo
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Botones de acciones con un tamaño más pequeño y mejor alineados
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Espaciado entre botones

        self.create_button = self.create_button_with_icon('Crear Producto', 'Iconos/Crear.ico', self.create_product)
        self.update_button = self.create_button_with_icon('Modificar Producto', 'Iconos/Actualizar.ico', self.update_product)
        self.search_button = self.create_button_with_icon('Buscar Producto', 'Iconos/Buscar.ico', self.search_product)
        self.delete_button = self.create_button_with_icon('Eliminar Producto', 'Iconos/Eliminar.ico', self.delete_product)
        self.export_button = self.create_button_with_icon('Generar Reporte', 'Iconos/Generar.ico', self.export_report)
        self.exit_button = self.create_button_with_icon('Salir', 'Iconos/Salir.ico', self.exit_application)  # Botón para salir

        # Aplicamos el ID de estilo para el botón de salir
        self.exit_button.setObjectName("exitButton")

        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.exit_button)  # Añadimos el botón de salir

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

    def exit_application(self):
        self.close()

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
                                    location TEXT,
                                    supplier TEXT,
                                    entry_date TEXT,
                                    quantity INTEGER
                                )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS product_movements (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    code TEXT,
                                    area TEXT,
                                    requester TEXT,
                                    date_out TEXT,
                                    quantity INTEGER
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
        query = '''INSERT INTO products (name, description, code, category, location, supplier, entry_date, quantity)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute_db_query(query, product_data)
    
    def update_product_in_db(self, product_data, code):
        query = '''UPDATE products
                   SET name = ?, description = ?, code=?, category = ?, location = ?, supplier=?, entry_date=?, quantity=?
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
        # Pedir el código del producto que se quiere eliminar
        code, ok = self.get_code_from_user('Eliminar Producto')
        if ok:
            # Verificar si el producto existe en la base de datos
            self.cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
            result = self.cursor.fetchone()
            
            if result:
                # Solicitar al usuario la cantidad a retirar
                quantity, ok_quantity = QInputDialog.getInt(self, 'Cantidad', 'Ingrese la cantidad a retirar:')
                
                if ok_quantity and quantity > 0 and quantity <= result[8]:
                    # Solicitar al usuario el área, solicitante y la fecha de salida
                    area, ok_area = QInputDialog.getText(self, 'Área', 'Ingrese el área solicitante:')
                    requester, ok_requester = QInputDialog.getText(self, 'Solicitante', 'Ingrese el nombre del solicitante:')
                    date_out, ok_date_out = QInputDialog.getText(self, 'Fecha de Salida', 'Ingrese la fecha de salida (YYYY-MM-DD):')

                    if ok_area and ok_requester and ok_date_out:
                        # Insertar un registro en el historial de movimientos (tabla product_movements)
                        query = '''INSERT INTO product_movements (code, area, requester, date_out, quantity)
                                   VALUES (?, ?, ?, ?, ?)'''
                        self.execute_db_query(query, (code, area, requester, date_out, quantity))
                        
                        # Restar la cantidad del inventario
                        new_quantity = result[8] - quantity
                        self.cursor.execute('UPDATE products SET quantity = ? WHERE code = ?', (new_quantity, code))
                        self.conn.commit()
                        
                        # Verificar si la cantidad llega a 0 y eliminar el producto si es necesario
                        if new_quantity == 0:
                            self.cursor.execute('DELETE FROM products WHERE code = ?', (code,))
                            self.conn.commit()

                        QMessageBox.information(self, 'Éxito', 'Producto eliminado y movimiento registrado exitosamente')
                    else:
                        QMessageBox.warning(self, 'Error de Entrada', 'Debe ingresar todos los datos para el historial de movimiento.')
                else:
                    QMessageBox.warning(self, 'Error de Cantidad', 'Cantidad inválida. Asegúrese de que sea menor o igual a la cantidad disponible.')
            else:
                QMessageBox.warning(self, 'Error', 'Producto no encontrado')

    def export_report(self):
        dialog = ExportReportDialog(self)
        dialog.exec_()

    def get_code_from_user(self, action):
        code, ok = QInputDialog.getText(self, action, 'Ingresa el código del producto:')
        return code, ok

# --- Formulario de Producto ---
class ProductFormDialog(QDialog):
    def __init__(self, parent, action, product_data=None):
        super().__init__(parent)
        self.setWindowTitle(action)
        self.setGeometry(200, 200, 450, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004d99;
            }
        """)

        self.product_data = product_data
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.code_input = QLineEdit(self)
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Papelería", "Computacion", "Muebles","Herramienta" ])  # Añadimos categorías predeterminadas
        self.location_input = QLineEdit(self)
        self.supplier_input = QLineEdit(self)
        self.entry_date_input = QDateEdit(self)
        self.entry_date_input.setDate(QDate.currentDate())
        self.quantity_input = QLineEdit(self)

        if self.product_data:
            # Rellenar los campos con la información existente del producto
            self.name_input.setText(self.product_data[1])
            self.description_input.setText(self.product_data[2])
            self.code_input.setText(self.product_data[3])
            self.category_input.setCurrentText(self.product_data[4])
            self.location_input.setText(self.product_data[5])
            self.supplier_input.setText(self.product_data[6])
            self.entry_date_input.setDate(QDate.fromString(self.product_data[7], "yyyy-MM-dd"))
            self.quantity_input.setText(str(self.product_data[8]))  # Rellenar la cantidad

        layout.addRow("Nombre", self.name_input)
        layout.addRow("Descripción", self.description_input)
        layout.addRow("Código", self.code_input)
        layout.addRow("Categoría", self.category_input)
        layout.addRow("Ubicación", self.location_input)
        layout.addRow("Proveedor", self.supplier_input)
        layout.addRow("Fecha de Entrada", self.entry_date_input)
        layout.addRow("Cantidad", self.quantity_input)

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_product)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def save_product(self):
        product_data = (
            self.name_input.text(),
            self.description_input.text(),
            self.code_input.text(),
            self.category_input.currentText(),
            self.location_input.text(),
            self.supplier_input.text(),
            self.entry_date_input.date().toString("yyyy-MM-dd"),
            int(self.quantity_input.text())
        )
        self.accept()

    def get_product_data(self):
        return (
            self.name_input.text(),
            self.description_input.text(),
            self.code_input.text(),
            self.category_input.currentText(),
            self.location_input.text(),
            self.supplier_input.text(),
            self.entry_date_input.date().toString("yyyy-MM-dd"),
            int(self.quantity_input.text())
        )

# --- Dialogo para Buscar Productos ---
class SearchProductDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Buscar Producto")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f9f9f9;
            }
            QLabel {
                font-size: 14px;
            }
            QTableWidget {
                font-size: 14px;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar producto por nombre o código")
        self.search_input.textChanged.connect(self.update_search_results)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_product)

        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Nombre", "Descripción", "Código", "Categoría", "Ubicación", "Proveedor", "Fecha Entrada", "Cantidad"])

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def search_product(self):
        search_term = self.search_input.text()

        self.parent().cursor.execute('SELECT * FROM products WHERE name LIKE ? OR code LIKE ?', (f'%{search_term}%', f'%{search_term}%'))
        results = self.parent().cursor.fetchall()

        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            for col, value in enumerate(result[1:]):  # Excluyendo el ID
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def update_search_results(self):
        self.search_product()

# --- Diálogo para Generar Reportes ---
class ExportReportDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Generar Reporte")
        self.setGeometry(300, 300, 300, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #004d99;
            }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.export_inventory_button = QPushButton("Generar Inventario General")
        self.export_inventory_button.clicked.connect(self.export_inventory_report)

        self.export_movements_button = QPushButton("Generar Historial de Movimientos")
        self.export_movements_button.clicked.connect(self.export_movements_report)

        layout.addWidget(self.export_inventory_button)
        layout.addWidget(self.export_movements_button)

        self.setLayout(layout)

    def export_inventory_report(self):
        query = 'SELECT * FROM products'
        df = pd.read_sql_query(query, self.parent().conn)
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Excel Files (*.xlsx)")

        if filename:
            df.to_excel(filename, index=False)
            QMessageBox.information(self, 'Éxito', 'Reporte de Inventario General generado exitosamente.')

    def export_movements_report(self):
        query = 'SELECT * FROM product_movements'
        df = pd.read_sql_query(query, self.parent().conn)
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Excel Files (*.xlsx)")

        if filename:
            df.to_excel(filename, index=False)
            QMessageBox.information(self, 'Éxito', 'Reporte de Movimientos generado exitosamente.')

# --- Ejecutar la aplicación ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()

    if login_window.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
