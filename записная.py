import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QListWidget, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt


class NotebookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Блокнот и Записная книжка")
        self.setGeometry(300, 100, 600, 400)

        self.notes_file = "notes.txt"  # Файл для хранения записей
        self.init_ui()
        self.load_notes()

    def init_ui(self):
        layout = QVBoxLayout()

        # Список записей
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_note)
        layout.addWidget(self.notes_list)

        # Текстовое поле для редактирования записей
        self.note_editor = QTextEdit()
        layout.addWidget(self.note_editor)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_note)
        button_layout.addWidget(self.add_button)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_note)
        button_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_note)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # Главный виджет
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_notes(self):
        """Загружает записи из файла."""
        try:
            with open(self.notes_file, "r", encoding="utf-8") as file:
                for line in file:
                    if "::" in line:
                        title, content = line.strip().split("::", 1)
                        item = self.notes_list.addItem(title)
                        self.notes_list.item(self.notes_list.count() - 1).setData(Qt.ItemDataRole.UserRole, content)
        except FileNotFoundError:
            pass

    def save_notes_to_file(self):
        """Сохраняет все записи в файл."""
        with open(self.notes_file, "w", encoding="utf-8") as file:
            for index in range(self.notes_list.count()):
                title = self.notes_list.item(index).text()
                content = self.notes_list.item(index).data(Qt.ItemDataRole.UserRole)
                file.write(f"{title}::{content}\n")

    def add_note(self):
        """Добавляет новую запись."""
        title = f"Заметка {self.notes_list.count() + 1}"
        self.notes_list.addItem(title)
        self.notes_list.item(self.notes_list.count() - 1).setData(Qt.ItemDataRole.UserRole, "")
        self.save_notes_to_file()

    def load_note(self, item):
        """Загружает содержимое выбранной записи в редактор."""
        content = item.data(Qt.ItemDataRole.UserRole)
        self.note_editor.setPlainText(content)

    def save_note(self):
        """Сохраняет текущую запись."""
        current_item = self.notes_list.currentItem()
        if current_item:
            content = self.note_editor.toPlainText()
            current_item.setData(Qt.ItemDataRole.UserRole, content)
            self.save_notes_to_file()

    def delete_note(self):
        """Удаляет текущую запись."""
        current_item = self.notes_list.currentItem()
        if current_item:
            reply = QMessageBox.question(
                self, "Подтверждение",
                "Вы уверены, что хотите удалить эту запись?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.notes_list.takeItem(self.notes_list.row(current_item))
                self.save_notes_to_file()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotebookApp()
    window.show()
    sys.exit(app.exec())
