import sys
import sqlite3
from PyQt5.QtWidgets import QSpinBox,QCompleter,QSystemTrayIcon, QMenu, QAction,QCalendarWidget, QGridLayout, QApplication, QMainWindow, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QInputDialog, QDialogButtonBox,QMessageBox, QWidget, QFileDialog, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap, QColor
import pandas as pd

# --- Ventana de Login ---
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 350, 250)
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
                border-radius: 10px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #003366;
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                border-radius: 8px;
                border: 1px solid #cccccc;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #004d99;
            }
            QPushButton:pressed {
                background-color: #003366;
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
        self.setWindowTitle('Sistema de inventario v1.0')
        self.setGeometry(100, 100, 900, 700)
        self.create_database()
        self.setWindowIcon(QIcon('Iconos/PJF.ico')) 
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f4f4;
            }
            QPushButton {
                background-color: #005b96;
                color: white;
                padding: 12px 20px;
                border-radius: 10px;
                font-size: 16px;
                min-width: 180px;
                text-align: center;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #004080;
            }
            QPushButton:pressed {
                background-color: #003060;
            }
            #exitButton {
                background-color: #ff3333;
                color: white;
            }
            #exitButton:hover {
                background-color: #ff6666;
            }
            #exitButton:pressed {
                background-color: #cc0000;
            }
        """)

        self.layout = QVBoxLayout()

        # Logo en el centro de la ventana
        logo_label = QLabel(self)
        pixmap = QPixmap('Imagenes/PJF.png')  # Asegúrate de tener el logo
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Agregar texto debajo del logo
        text_label = QLabel("Control de Inventario", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
                color: #0066cc;
                margin-top: 5px;
                margin-bottom:10px
            }
        """)
        
        version_label = QLabel("Versión 1.0", self)
        version_label.setAlignment(Qt.AlignLeft)  # Alinearlo a la izquierda
        version_label.setStyleSheet("font-size: 14px; color: #888; padding: 10px; margin-top:10px;")  # Estilo

        area_label = QLabel("Recursos Materiales", self)
        area_label.setAlignment(Qt.AlignLeft)  # Alinearlo a la izquierda
        area_label.setStyleSheet("font-size: 14px; color: #888; padding: 10px; margin-top:0px; margin-bottom:10px;")  # Estilo

        # Botones de acciones en una cuadrícula
        button_layout = QGridLayout()
        button_layout.setSpacing(20)

      
        self.create_button = self.create_button_with_icon('Entrada Producto', 'Iconos/Crear.ico', self.create_product)
        self.update_button = self.create_button_with_icon('Modificar Producto', 'Iconos/Actualizar.ico', self.update_product)
        self.search_button = self.create_button_with_icon('Buscar Producto', 'Iconos/Buscar.ico', self.search_product)
        self.delete_button = self.create_button_with_icon('Salida Producto', 'Iconos/Eliminar.ico', self.delete_product)
        self.export_button = self.create_button_with_icon('Generar Reporte', 'Iconos/Generar.ico', self.export_report)
        self.exit_button = self.create_button_with_icon('Salir', 'Iconos/Salir.ico', self.exit_application)
        self.exit_button.setObjectName("exitButton")

        button_layout.addWidget(self.create_button, 0, 0)
        button_layout.addWidget(self.update_button, 0, 1)
        button_layout.addWidget(self.search_button, 1, 0)
        button_layout.addWidget(self.delete_button, 1, 1)
        button_layout.addWidget(self.export_button, 2, 0, 1, 2)  # Ocupa dos columnas
        button_layout.addWidget(self.exit_button, 3, 0, 1, 2)  # Ocupa dos columnas

        self.layout.addWidget(logo_label)  # Añadimos el logo
        self.layout.addWidget(text_label)  #Añadimos el titulo
        self.layout.addWidget(version_label) #Añadimos el versionado
        self.layout.addWidget(area_label) #Añadimos el area del inventario
        self.layout.addLayout(button_layout)  # Añadimos los botones

        # Contenedor principal
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def create_button_with_icon(self, text, icon_name, action):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_name))  # Asignar icono
        button.clicked.connect(action)
        button.setMinimumHeight(50)  # Aseguramos que los botones tengan una altura mínima adecuada
        return button

    def exit_application(self):
        self.close()

    def create_database(self):
        try:
            self.conn = sqlite3.connect('products.db')
            self.cursor = self.conn.cursor()

            # Crear la tabla de productos con la nueva columna "unidad_medida"
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT,
                                    description TEXT,
                                    code TEXT UNIQUE,
                                    category TEXT,
                                    location TEXT,
                                    supplier TEXT,
                                    entry_date TEXT,
                                    quantity INTEGER,
                                    unidad_medida TEXT,
                                    is_available BOOLEAN DEFAULT 1
                                )''')
            
            # Crear la tabla de movimientos de productos si no existe
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
            print(str(e))
            #QMessageBox.critical(self, 'Error de Base de Datos', f'Error al ejecutar la consulta: {e}')

    def insert_product(self, product_data):
        query = '''INSERT INTO products (name, description, code, category, location, supplier, entry_date, quantity,unidad_medida)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute_db_query(query, product_data)
    
    def update_product_in_db(self, product_data, code):
        query = '''UPDATE products
                   SET name = ?, description = ?, code=?, category = ?, location = ?, supplier=?, entry_date=?, quantity=?,unidad_medida=?
                   WHERE code = ?'''
        
        # Asegúrate de que estamos pasando los parámetros correctamente
        self.execute_db_query(query, (*product_data, code))

    def create_product(self):
        dialog = ProductFormDialog(self, 'Entrada Producto')
        if dialog.exec_():
            product_data = dialog.get_product_data()
            self.insert_product(product_data)
            #QMessageBox.information(self, 'Éxito', 'Producto creado exitosamente')      

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
        dialog = ProductExitDialog(self)
        dialog.exec_()

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
        self.code_input.setPlaceholderText("Ingrese código del producto")
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Papelería","Construcción","Mobiliario", "Herramienta","Plomería / Fontanería","Seguridad Industrial / Proteccion Civil","Tecnología / Electrónica","Limpieza / Mantenimiento","Repuestos / Consumibles", "Otra"])  # Categorías predeterminadas
        self.location_input = QLineEdit(self)
        self.supplier_input = QLineEdit(self)
        self.entry_date_input = QDateEdit(self)
        self.entry_date_input.setDate(QDate.currentDate())
        self.quantity_input = QLineEdit(self)
        
        # Nueva lista de unidades de medida
        self.unit_input = QComboBox(self)
        self.unit_input.addItems(["Pieza","Caja", "Metro", "Millar","Block","Bola","Paquete","Rollo","Frasco","Tubo","Sobre","Juego"])  # Opciones de unidades de medida

        # Label para mostrar el estado del código
        self.code_status_label = QLabel(self)
        self.code_status_label.setAlignment(Qt.AlignCenter)
        self.code_status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                padding: 5px;
            }
        """)

        layout.addRow("Nombre", self.name_input)
        layout.addRow("Descripción", self.description_input)
        layout.addRow("Código", self.code_input)
        layout.addRow(self.code_status_label)  # Mostrar el estado del código
        layout.addRow("Categoría", self.category_input)
        layout.addRow("Ubicación", self.location_input)
        layout.addRow("Proveedor", self.supplier_input)
        layout.addRow("Fecha de Entrada", self.entry_date_input)
        layout.addRow("Cantidad", self.quantity_input)
        layout.addRow("Unidad de Medida", self.unit_input)  # Agregar campo de unidad de medida

        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_product)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)
        self.setLayout(layout)

        # Conectar el evento de cambio de texto en el código para verificar disponibilidad
        self.code_input.editingFinished.connect(self.check_code_availability)

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
            self.unit_input.setCurrentText(self.product_data[9])  # Rellenar la unidad de medida

            # Bloquear campos si el código ya existe
            self.code_input.setEnabled(False)  # Bloquear el código
            self.category_input.setEnabled(True)
            self.location_input.setEnabled(True)
            self.supplier_input.setEnabled(True)
            self.entry_date_input.setEnabled(False)
            self.quantity_input.setEnabled(False)

    def get_product_data(self):
        """Este método devuelve los datos ingresados del formulario."""
        return (
            self.name_input.text(),
            self.description_input.text(),
            self.code_input.text(),
            self.category_input.currentText(),
            self.location_input.text(),
            self.supplier_input.text(),
            self.entry_date_input.date().toString("yyyy-MM-dd"),
            int(self.quantity_input.text()),
            self.unit_input.currentText()  # Obtener la unidad de medida
        )

    def check_code_availability(self):
        code = self.code_input.text()

        if not code:
            return  # Si el código está vacío no hacemos nada

        self.parent().cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
        result = self.parent().cursor.fetchone()

        if result:
            # Si el código existe, mostrar mensaje en amarillo (utilizado) y cargar los datos existentes
            self.code_status_label.setText("Código Utilizado")
            self.code_status_label.setStyleSheet("background-color: yellow; color: black;")
            self.load_existing_product_data(result)
        else:
            # Si el código no existe, mostrar mensaje verde (disponible)
            self.code_status_label.setText("Código Disponible")
            self.code_status_label.setStyleSheet("background-color: green; color: white;")

    def load_existing_product_data(self, result):
        # Rellenar los campos con los datos existentes del producto
        self.name_input.setText(result[1])
        self.description_input.setText(result[2])
        self.category_input.setCurrentText(result[4])
        self.location_input.setText(result[5])
        self.supplier_input.setText(result[6])
        self.entry_date_input.setDate(QDate.fromString(result[7], "yyyy-MM-dd"))
        self.quantity_input.setText(str(result[8]))  # Rellenar la cantidad
        self.unit_input.setCurrentText(result[9])  # Rellenar la unidad de medida

        # Bloquear campos
        self.name_input.setEnabled(False)
        self.description_input.setEnabled(False)
        self.code_input.setEnabled(False)
        self.category_input.setEnabled(False)
        self.location_input.setEnabled(False)
        self.supplier_input.setEnabled(False)
        self.entry_date_input.setEnabled(False)

    def save_product(self):
        # Validar que el código no esté vacío
        if not self.code_input.text():
            QMessageBox.warning(self, 'Error', 'El código es obligatorio.')
            return

        # Validar la cantidad (debe ser un número entero positivo)
        try:
            quantity = int(self.quantity_input.text())
            if quantity < 0:
                raise ValueError("La cantidad no puede ser negativa.")
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))
            return

        # Obtener el código ingresado
        code = self.code_input.text()

        try:
            # Verificamos si ya existe un producto con ese código
            self.parent().cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
            result = self.parent().cursor.fetchone()

            if result:
                # Si el código ya existe, actualizamos la cantidad y la unidad de medida
                new_quantity = result[8] + quantity  # Asegúrate de que la posición 8 corresponde a "quantity"
                is_available = 1 if new_quantity > 0 else 0  # Marcarlo como disponible si la cantidad es mayor que 0
                self.parent().cursor.execute('UPDATE products SET quantity = ?, unidad_medida = ?, is_available = ? WHERE code = ?',
                                             (new_quantity, self.unit_input.currentText(), is_available, code))
                self.parent().conn.commit()  # Confirmamos los cambios en la base de datos
                QMessageBox.information(self, 'Éxito', 'Cantidad actualizada exitosamente.')
            else:
                # Si el código no existe, lo insertamos como un nuevo producto
                is_available = 1 if quantity > 0 else 0  # Si la cantidad es mayor que 0, lo marcamos como disponible
                product_data = (
                    self.name_input.text(),
                    self.description_input.text(),
                    self.code_input.text(),
                    self.category_input.currentText(),
                    self.location_input.text(),
                    self.supplier_input.text(),
                    self.entry_date_input.date().toString("yyyy-MM-dd"),
                    quantity,
                    self.unit_input.currentText(),  # Guardar la unidad de medida
                    is_available  # Guardar el estado de disponibilidad
                )

                self.parent().cursor.execute('INSERT INTO products (name, description, code, category, location, supplier, entry_date, quantity, unidad_medida, is_available) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', product_data)
                self.parent().conn.commit()  # Confirmamos los cambios en la base de datos
                QMessageBox.information(self, 'Éxito', 'Producto creado exitosamente.')

        except sqlite3.IntegrityError as e:
            print(f"Error de Integridad: {e}")
            QMessageBox.warning(self, 'Error', 'El código ya está registrado en la base de datos.')

        except Exception as e:
            print(f"Error inesperado: {e}")
            QMessageBox.warning(self, 'Error', 'Ha ocurrido un error inesperado.')

        finally:
            self.parent().conn.commit()  # Confirmar siempre los cambios finales
            self.accept()


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

        # Cuadro de texto para buscar por código o nombre
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar por nombre o código...")
        self.search_input.textChanged.connect(self.update_search_results)

        # Filtro de categoría
        self.category_filter = QComboBox(self)
        self.category_filter.addItem("Todas las Categorías")
        self.category_filter.addItem("Papelería")
        self.category_filter.addItem("Construcción")
        self.category_filter.addItem("Mobiliario")
        self.category_filter.addItem("Herramienta")
        self.category_filter.addItem("Plomería / Fontanería")
        self.category_filter.addItem("Seguridad Industrial / Proteccion Civil")
        self.category_filter.addItem("Tecnología / Electrónica")
        self.category_filter.addItem("Limpieza / Mantenimiento")
        self.category_filter.addItem("Repuestos y consumibles")
        self.category_filter.addItem("Otra")
        self.category_filter.currentIndexChanged.connect(self.update_search_results)

        # Tabla para mostrar los productos
        self.table = QTableWidget(self)
        self.table.setColumnCount(9)  # 9 columnas para mostrar todos los detalles
        self.table.setHorizontalHeaderLabels(
            ["Nombre", "Descripción", "Código", "Categoría", "Ubicación", "Proveedor", 
             "Fecha Alta", "Cantidad Disponible", "Unidad de Medida"])  # Nueva columna

        layout.addWidget(self.search_input)
        layout.addWidget(self.category_filter)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_search_results(self):
        # Obtenemos el texto ingresado en el cuadro de búsqueda
        search_term = self.search_input.text()

        # Obtenemos la categoría seleccionada en el filtro
        selected_category = self.category_filter.currentText()

        # Si no se ha ingresado texto en el cuadro de búsqueda, realizamos la búsqueda de acuerdo a la categoría
        if not search_term and selected_category == "Todas las Categorías":
            self.search_product()
        elif not search_term:  # Si no hay texto de búsqueda pero se ha seleccionado una categoría
            self.search_product_by_category(selected_category)
        else:
            # Realizamos la búsqueda con el término de búsqueda y la categoría seleccionada
            self.search_product_by_name_or_code(search_term, selected_category)

    def search_product(self):
        # Realizamos la búsqueda sin filtrar por categoría ni por búsqueda de texto
        self.parent().cursor.execute('''SELECT name, description, code, category, location, supplier, entry_date, quantity, unidad_medida, is_available 
                                        FROM products''')
        
        results = self.parent().cursor.fetchall()

        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            for col, value in enumerate(result[:9]):  # Incluimos "Unidad de Medida" en los resultados
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

            # Verificamos si el producto está disponible
            if result[7] == 0:  # quantity == 0
                # Cambiar el color de fondo a gris si no está disponible
                for col in range(9):
                    item = self.table.item(row, col)
                    item.setBackground(QColor(200, 200, 200))  # Gris claro
                self.table.setItem(row, 7, QTableWidgetItem("No Disponible"))  # Mostrar "No Disponible" en la columna de cantidad

    def search_product_by_category(self, category):
        # Realizamos la búsqueda filtrando por la categoría seleccionada
        self.parent().cursor.execute('''SELECT name, description, code, category, location, supplier, entry_date, quantity, unidad_medida, is_available 
                                        FROM products WHERE category = ?''', (category,))
        
        results = self.parent().cursor.fetchall()

        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            for col, value in enumerate(result[:9]):  # Incluimos "Unidad de Medida" en los resultados
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

            # Verificamos si el producto está disponible
            if result[7] == 0:  # quantity == 0
                # Cambiar el color de fondo a gris si no está disponible
                for col in range(9):
                    item = self.table.item(row, col)
                    item.setBackground(QColor(200, 200, 200))  # Gris claro
                self.table.setItem(row, 7, QTableWidgetItem("No Disponible"))  # Mostrar "No Disponible" en la columna de cantidad

    def search_product_by_name_or_code(self, search_term, category):
        # Realizamos la búsqueda filtrando por nombre o código y por la categoría seleccionada (si corresponde)
        query = '''
            SELECT name, description, code, category, location, supplier, entry_date, quantity, unidad_medida, is_available 
            FROM products
            WHERE (name LIKE ? OR code LIKE ?)
        '''
        
        # Si hay una categoría seleccionada distinta de "Todas las Categorías", la filtramos también
        if category != "Todas las Categorías":
            query += ' AND category = ?'

        # Ejecutamos la consulta con los parámetros
        if category != "Todas las Categorías":
            self.parent().cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', category))
        else:
            self.parent().cursor.execute(query, (f'%{search_term}%', f'%{search_term}%',))

        results = self.parent().cursor.fetchall()

        self.table.setRowCount(len(results))

        for row, result in enumerate(results):
            for col, value in enumerate(result[:9]):  # Incluimos "Unidad de Medida" en los resultados
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

            # Verificamos si el producto está disponible
            if result[7] == 0:  # quantity == 0
                # Cambiar el color de fondo a gris si no está disponible
                for col in range(9):
                    item = self.table.item(row, col)
                    item.setBackground(QColor(200, 200, 200))  # Gris claro
                self.table.setItem(row, 7, QTableWidgetItem("No Disponible"))  # Mostrar "No Disponible" en la columna de cantidad

#--- Ventana para seleccionar el rango de fechas ---
class SelectDateRangeDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Rango de Fechas")
        self.setGeometry(200, 200, 400, 200)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Crear las listas desplegables para mes y año
        self.month_combo = QComboBox(self)
        self.month_combo.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.month_combo.setCurrentIndex(QDate.currentDate().month() - 1)  # Preseleccionar el mes actual

        self.year_combo = QComboBox(self)
        current_year = QDate.currentDate().year()
        # Agregar un rango de años (por ejemplo, los últimos 10 años)
        self.year_combo.addItems([str(year) for year in range(current_year - 5, current_year + 1)])
        self.year_combo.setCurrentIndex(self.year_combo.count() - 1)  # Preseleccionar el año actual

        # Etiquetas para mostrar las selecciones
        self.date_range_label = QLabel("Selecciona el mes y el año para el reporte:", self)
        layout.addWidget(self.date_range_label)
        layout.addWidget(self.month_combo)
        layout.addWidget(self.year_combo)

        # Botones para aplicar el rango o generar el reporte completo
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Aplicar Rango de Fechas", self)
        self.apply_button.clicked.connect(self.apply_date_range)

        self.full_report_button = QPushButton("Generar Reporte Completo", self)
        self.full_report_button.clicked.connect(self.generate_full_report)

        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.full_report_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def apply_date_range(self):
        # Obtener el mes y el año seleccionados
        selected_month = self.month_combo.currentIndex() + 1  # Los meses van de 1 a 12
        selected_year = self.year_combo.currentText()

        # Generar las fechas de inicio y fin del mes seleccionado
        start_date = f"{selected_year}-{selected_month:02d}-01"
        # Para obtener el último día del mes, vamos a crear una fecha con el próximo mes y restar un día
        next_month = selected_month % 12 + 1
        next_month_year = selected_year if selected_month < 12 else str(int(selected_year) + 1)
        end_date = f"{next_month_year}-{next_month:02d}-01"
        end_date = QDate.fromString(end_date, "yyyy-MM-dd").addDays(-1).toString("yyyy-MM-dd")

        # Llamar al método de generación de reporte con las fechas
        self.parent().generate_report(start_date, end_date)

        # Cerrar la ventana de selección de fechas
        self.accept()

    def generate_full_report(self):
        # Generar el reporte sin restricción de fechas
        self.parent().generate_report(None, None)

        # Cerrar la ventana de selección de fechas
        self.accept()
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
        self.export_movements_button.clicked.connect(self.open_date_range_dialog)

        layout.addWidget(self.export_inventory_button)
        layout.addWidget(self.export_movements_button)

        self.setLayout(layout)

    def open_date_range_dialog(self):
        # Abrir el diálogo de selección de mes y año
        date_range_dialog = SelectDateRangeDialog(self)
        date_range_dialog.exec_()

    def generate_report(self, start_date, end_date):
        if start_date and end_date:
            # Generar el reporte de movimientos en el rango de fechas seleccionado
            self.export_movements_report(start_date, end_date)
        else:
            # Si no se seleccionó un rango de fechas, generar el reporte completo
            self.export_movements_report()

    def export_inventory_report(self):
        query = 'SELECT * FROM products'
        df = pd.read_sql_query(query, self.parent().conn)

        # Cambiar nombres de columnas
        df.columns = ["ID", "Nombre", "Descripción", "Código", "Categoría", "Ubicación", "Proveedor", "Fecha de Entrada", "Cantidad", "Unidad Medida", "Disponible"]

        # Abrir diálogo para guardar archivo
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Excel Files (*.xlsx)")

        if filename:
            try:
                # Crear el archivo Excel con múltiples hojas (una por categoría)
                with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                    # Agrupar por categoría
                    for category, group_df in df.groupby("Categoría"):
                        # Escribir cada categoría en una hoja diferente
                        sheet_name = category[:31]  # Excel no permite nombres de hoja >31 caracteres
                        group_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                QMessageBox.information(self, 'Éxito', 'Reporte de Inventario General generado exitosamente.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Ocurrió un error al generar el reporte: {str(e)}')


    def export_movements_report(self, start_date=None, end_date=None):
        # Modificar la consulta para incluir el nombre del producto
        if start_date and end_date:
            query = '''SELECT pm.code, p.name, pm.area, pm.requester, pm.date_out, pm.quantity, p.unidad_medida
                       FROM product_movements pm
                       JOIN products p ON pm.code = p.code
                       WHERE pm.date_out BETWEEN ? AND ?'''

            params = (start_date, end_date)
        else:
            query = '''SELECT pm.code, p.name, pm.area, pm.requester, pm.date_out, pm.quantity, p.unidad_medida
                       FROM product_movements pm
                       JOIN products p ON pm.code = p.code'''
            params = ()

        df = pd.read_sql_query(query, self.parent().conn, params=params)

        # Cambiar los encabezados a español
        df.columns = ["Código", "Nombre del Producto", "Área", "Solicitante", "Fecha de Salida", "Cantidad", "Unidad Medida"]

        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Excel Files (*.xlsx)")

        if filename:
            try:
                df.to_excel(filename, index=False)
                QMessageBox.information(self, 'Éxito', 'Reporte de Movimientos generado exitosamente.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Ocurrió un error al generar el reporte: {str(e)}')
        else:
            QMessageBox.warning(self, 'Cancelado', 'No se seleccionó ningún archivo para guardar.')

class ProductExitDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.conn = parent.conn
        self.cursor = parent.cursor
        self.setWindowTitle("Salida múltiple de productos")
        self.setGeometry(300, 300, 800, 450)

        self.products_cache = {}  # código -> dict(producto) para autocompletar y validación
        self.selected_products = {}

        self.initUI()
        self.load_products_for_autocomplete()

    def initUI(self):
        layout = QVBoxLayout()

        # Área y solicitante
        area_layout = QHBoxLayout()
        area_layout.addWidget(QLabel("Área:"))
        self.area_input = QLineEdit()
        area_layout.addWidget(self.area_input)

        area_layout.addWidget(QLabel("Solicitante:"))
        self.requester_input = QLineEdit()
        area_layout.addWidget(self.requester_input)

        layout.addLayout(area_layout)

        # Campo para ingresar producto con autocompletado
        product_layout = QHBoxLayout()
        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Código o nombre del producto")
        product_layout.addWidget(self.product_input)

        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self.add_product)
        product_layout.addWidget(self.add_button)

        layout.addLayout(product_layout)

        # Tabla productos para salida
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Código", "Nombre", "Cantidad Disponible", "Unidad", "Cantidad a Salir"])
        layout.addWidget(self.table)

        # Botón registrar salida
        self.exit_button = QPushButton("Registrar Salida")
        self.exit_button.clicked.connect(self.register_exit)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def load_products_for_autocomplete(self):
        # Carga todos los productos disponibles para autocompletar
        self.cursor.execute("SELECT code, name, quantity, unidad_medida FROM products WHERE is_available=1")
        products = self.cursor.fetchall()

        self.products_cache = {}
        items = []
        for code, name, qty, unit in products:
            display = f"{code} - {name}"
            items.append(display)
            self.products_cache[display] = {
                'code': code,
                'name': name,
                'quantity': qty,
                'unit': unit
            }
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.product_input.setCompleter(completer)

    def add_product(self):
        text = self.product_input.text().strip()
        if text not in self.products_cache:
            QMessageBox.warning(self, "Producto no encontrado", "Por favor seleccione un producto válido del autocompletado.")
            return

        product = self.products_cache[text]
        code = product['code']

        if code in self.selected_products:
            QMessageBox.warning(self, "Producto ya agregado", "Este producto ya está en la lista.")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(product['code']))
        self.table.setItem(row, 1, QTableWidgetItem(product['name']))
        self.table.setItem(row, 2, QTableWidgetItem(str(product['quantity'])))
        self.table.setItem(row, 3, QTableWidgetItem(product['unit']))

        spin = QSpinBox()
        spin.setRange(1, product['quantity'])
        spin.setValue(1)
        self.table.setCellWidget(row, 4, spin)

        self.selected_products[code] = product
        self.product_input.clear()

    def register_exit(self):
        area = self.area_input.text().strip()
        requester = self.requester_input.text().strip()
        if not area or not requester:
            QMessageBox.warning(self, "Error", "Debe ingresar área y solicitante.")
            return

        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "No hay productos para salida.")
            return

        try:
            for row in range(self.table.rowCount()):
                code = self.table.item(row, 0).text()
                qty_disponible = int(self.table.item(row, 2).text())
                spin = self.table.cellWidget(row, 4)
                qty_salida = spin.value()

                if qty_salida > qty_disponible:
                    QMessageBox.warning(self, "Error", f"La cantidad a salir para {code} supera la disponible.")
                    return

                nueva_cant = qty_disponible - qty_salida
                is_disp = 1 if nueva_cant > 0 else 0

                self.cursor.execute('UPDATE products SET quantity=?, is_available=? WHERE code=?',
                                    (nueva_cant, is_disp, code))

                self.cursor.execute('''INSERT INTO product_movements (code, area, requester, date_out, quantity)
                                       VALUES (?, ?, ?, DATE('now'), ?)''',
                                    (code, area, requester, qty_salida))

            self.conn.commit()
            QMessageBox.information(self, "Salida registrada", "La salida de productos se registró correctamente.")
            self.accept()

        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

# --- Ejecutar la aplicación ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()

    if login_window.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
        
        
        
