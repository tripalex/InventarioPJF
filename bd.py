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
                                entry_date DATE   -- Cambiado a tipo DATE
                            )''')
        self.conn.commit()
    except sqlite3.Error as e:
        QMessageBox.critical(self, 'Error de Conexión', f'Error al crear la base de datos: {e}')
        self.close()

create_database()