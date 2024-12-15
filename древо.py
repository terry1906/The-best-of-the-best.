import sqlite3
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from graphviz import Digraph
import csv


# Подключение к базе данных SQLite
def connect_db():
    return sqlite3.connect('genealogy.db')


# Создание таблицы в базе данных
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('male', 'female')) NOT NULL,
        father_id INTEGER,
        mother_id INTEGER,
        birthdate TEXT,
        deathdate TEXT,
        FOREIGN KEY(father_id) REFERENCES people(id),
        FOREIGN KEY(mother_id) REFERENCES people(id)
    );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_father_id ON people(father_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mother_id ON people(mother_id);")
    conn.commit()
    conn.close()


# Добавление нового человека в базу данных
def add_person(name, gender, birthdate=None, deathdate=None, father_id=None, mother_id=None):
    conn = connect_db()
    cursor = conn.cursor()

    # Проверка на наличие родителей
    if father_id:
        cursor.execute("SELECT id FROM people WHERE id = ?", (father_id,))
        if cursor.fetchone() is None:
            print(f"Ошибка: отец с ID {father_id} не найден.")
            return

    if mother_id:
        cursor.execute("SELECT id FROM people WHERE id = ?", (mother_id,))
        if cursor.fetchone() is None:
            print(f"Ошибка: мать с ID {mother_id} не найдена.")
            return

    cursor.execute("""
    INSERT INTO people (name, gender, birthdate, deathdate, father_id, mother_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, gender, birthdate, deathdate, father_id, mother_id))

    conn.commit()
    conn.close()


# Получение родителей человека по ID
def get_parents(person_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT father_id, mother_id FROM people WHERE id = ?", (person_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[1]
    return None, None


# Получение братьев и сестер человека по ID
def get_siblings(person_id):
    father, mother = get_parents(person_id)
    if father and mother:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name FROM people
        WHERE father_id = ? AND mother_id = ? AND id != ?
        """, (father, mother, person_id))
        siblings = cursor.fetchall()
        conn.close()
        return [sibling[1] for sibling in siblings]
    return []


# Визуализация родословного древа с помощью Graphviz
def visualize_family_tree(person_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    person = cursor.fetchone()
    conn.close()

    if not person:
        print("Человек не найден.")
        return

    dot = Digraph(comment=f'Family Tree of {person[1]}')

    # Рекурсивная функция для добавления всех родственных связей
    def add_family_member(id, dot):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people WHERE id = ?", (id,))
        member = cursor.fetchone()
        conn.close()

        if member:
            dot.node(str(member[0]), member[1])  # Добавляем человека в граф
            father, mother = get_parents(member[0])

            if father:
                dot.edge(str(father), str(member[0]), label="father")
                add_family_member(father, dot)

            if mother:
                dot.edge(str(mother), str(member[0]), label="mother")
                add_family_member(mother, dot)

    add_family_member(person_id, dot)
    dot.render('family_tree', format='png', view=True)


# Экспорт данных из базы данных в CSV
def export_to_csv():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()

    with open('family_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Gender", "Father ID", "Mother ID", "Birthdate", "Deathdate"])
        writer.writerows(rows)

    conn.close()
    print("Данные успешно экспортированы в family_data.csv.")


# Графический интерфейс приложения с помощью PyQt6
class GenealogyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genealogy Application")

        # Главное окно
        self.layout = QtWidgets.QVBoxLayout(self)

        # Поля для ввода данных о человеке
        self.form_layout = QtWidgets.QFormLayout()

        self.entry_name = QtWidgets.QLineEdit()
        self.form_layout.addRow("Name:", self.entry_name)

        self.gender_group = QtWidgets.QButtonGroup(self)
        self.male_radio = QtWidgets.QRadioButton("Male")
        self.female_radio = QtWidgets.QRadioButton("Female")
        self.male_radio.setChecked(True)
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        gender_layout = QtWidgets.QHBoxLayout()
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        self.form_layout.addRow("Gender:", gender_layout)

        self.entry_birthdate = QtWidgets.QLineEdit()
        self.form_layout.addRow("Birthdate (YYYY-MM-DD):", self.entry_birthdate)

        self.entry_father = QtWidgets.QLineEdit()
        self.form_layout.addRow("Father ID:", self.entry_father)

        self.entry_mother = QtWidgets.QLineEdit()
        self.form_layout.addRow("Mother ID:", self.entry_mother)

        self.layout.addLayout(self.form_layout)

        # Кнопки
        self.add_button = QtWidgets.QPushButton("Add Person")
        self.add_button.clicked.connect(self.add_person)
        self.layout.addWidget(self.add_button)

        self.visualize_button = QtWidgets.QPushButton("Visualize Family Tree")
        self.visualize_button.clicked.connect(self.visualize_tree)
        self.layout.addWidget(self.visualize_button)

        self.export_button = QtWidgets.QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_data)
        self.layout.addWidget(self.export_button)

        self.setLayout(self.layout)

    def add_person(self):
        name = self.entry_name.text()
        gender = "male" if self.male_radio.isChecked() else "female"
        birthdate = self.entry_birthdate.text()
        father_id = self.entry_father.text()
        mother_id = self.entry_mother.text()

        try:
            father_id = int(father_id) if father_id else None
            mother_id = int(mother_id) if mother_id else None
            add_person(name, gender, birthdate, father_id=father_id, mother_id=mother_id)
            QtWidgets.QMessageBox.information(self, "Success", "Person added successfully!")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid input for parent IDs.")

    def visualize_tree(self):
        person_id, ok = QtWidgets.QInputDialog.getInt(self, "Enter ID",
                                                      "Enter the ID of the person to visualize the family tree:")
        if ok and person_id:
            visualize_family_tree(person_id)

    def export_data(self):
        export_to_csv()
        QtWidgets.QMessageBox.information(self, "Export", "Data has been successfully exported to CSV.")


# Запуск приложения
def main():
    create_table()

    app = QtWidgets.QApplication(sys.argv)
    window = GenealogyApp()
    window.setGeometry(100, 100, 500, 400)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
