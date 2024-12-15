import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QPushButton, QLineEdit, QMessageBox, QInputDialog,
                             QScrollArea, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QFormLayout, QTextEdit, QMainWindow, QComboBox)
from PyQt6.QtGui import QPixmap


# Подключение к базе данных (создание, если не существует)
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT
        )
    ''')

    # Create orders table if it doesn't exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_details TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def add_user_id_column():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Add user_id column to the orders table (if it doesn't already exist)
    try:
        cursor.execute('''ALTER TABLE orders ADD COLUMN user_id INTEGER''')
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists or another error occurs

    conn.close()


# Класс для меню
class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


# Главное окно приложения
class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Меню Макдональдса")

        # Элементы меню
        self.menu_items = [
            MenuItem("🍔Чизбургер🍔", 180),
            MenuItem("🍟Картошка фри🍟", 100),
            MenuItem("🥤Напиток🥤", 50),
            MenuItem("🥟Наггетсы🥟", 200),
            MenuItem("🥗Салат Цезарь🥗", 250),
            MenuItem("🥛Молочный коктейль🥛", 120),
            MenuItem("🍔Фишбургеры🍔", 160),
            MenuItem("🥮Пирожок с вишней🥮", 70),
            MenuItem("☕Кофе☕", 90)
        ]

        self.cart = []
        self.order_history = []
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        button_cart = QPushButton("Выход с аккаунта")
        button_cart.clicked.connect(self.open_login)
        layout.addWidget(button_cart)

        button_cart = QPushButton("Настройки")
        button_cart.clicked.connect(self.open_setting)
        layout.addWidget(button_cart)

        # Создаем прокрутку
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # Меню
        for item in self.menu_items:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"{item.name} - {item.price} ₽"))
            button = QPushButton("+")
            button.clicked.connect(lambda checked, item=item: self.add_to_cart(item))
            h_layout.addWidget(button)
            scroll_layout.addLayout(h_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)

        layout.addWidget(scroll)

        # Кнопки корзины и истории заказов
        button_cart = QPushButton("Корзина")
        button_cart.clicked.connect(self.open_cart)
        layout.addWidget(button_cart)

        button_history = QPushButton("История заказов")
        button_history.clicked.connect(self.open_order_history)
        layout.addWidget(button_history)

        self.setLayout(layout)

    def open_login(self):
        self.close()
        self.login_window = Login()
        self.login_window.show()

    def add_to_cart(self, item):
        self.cart.append(item)
        QMessageBox.information(self, "Добавлено в корзину", f"{item.name} добавлено в корзину!")

    def open_cart(self):
        if not self.cart:
            QMessageBox.information(self, "Корзина пуста", "Ваша корзина пуста!")
            return
        self.cart_window = CartWindow(self.cart, self.order_history, self.user_id)
        self.cart_window.show()

    def open_setting(self):
        self.open_setting = Setting()
        self.open_setting.show()

    def open_order_history(self):
        self.history_window = OrderHistoryWindow(self.user_id)
        self.history_window.show()


class Setting(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_open_setting = QPushButton('Обновление 2.0')
        btn_open_setting.clicked.connect(self.open_obnov)
        layout.addWidget(btn_open_setting)

        btn_open_setting1 = QPushButton('Версия 1.0')
        btn_open_setting1.clicked.connect(self.open_obnov1)
        layout.addWidget(btn_open_setting1)

        btn_open_setting1 = QPushButton('Рестораны')
        btn_open_setting1.clicked.connect(self.open_restaurant)
        layout.addWidget(btn_open_setting1)

        open_license_window = QPushButton('Открыть лицензионное соглашение')
        open_license_window.clicked.connect(self.open_license)
        layout.addWidget(open_license_window)

        btn = QPushButton('Назад')
        btn.clicked.connect(self.open_men)
        layout.addWidget(btn)

        self.setLayout(layout)

    def open_license(self):
        self.close()
        self.license_window = LicenseWindow()
        self.license_window.show()

    def open_men(self):
        self.close()
        self.menu_window = MainWindow(self)



    def open_obnov(self):
        self.close()
        self.obnov_window = Obnov()
        self.obnov_window.show()

    def open_obnov1(self):
        self.close()
        self.obnov_window1 = Obnov1()
        self.obnov_window1.show()

    def open_restaurant(self):
        self.close()
        self.restaurant_window = Restaurant()
        self.restaurant_window.show()


class LicenseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лицензионное соглашение")
        self.setGeometry(450, 175, 400, 300)

        layout = QVBoxLayout()

        # Чтение лицензионного соглашения из файла
        with open('license_agreement.txt', 'r', encoding='utf-8') as file:
            license_text = file.read()

        # Текстовое поле для отображения лицензионного соглашения
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(license_text)
        self.text_edit.setReadOnly(True)  # Делаем текстовое поле только для чтения

        layout.addWidget(self.text_edit)
        self.setLayout(layout)


class Restaurant(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поиск ресторанов в Санкт-Петербурге")
        self.setGeometry(450, 175, 300, 550)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.btn = QPushButton('Назад')
        self.btn.clicked.connect(self.open_setting)
        self.layout.addWidget(self.btn)

        self.region_label = QLabel("Выберите район:")
        self.region_combo = QComboBox()
        self.region_combo.addItems([
            "Не выбран",
            "Адмиралтейский",
            "Василеостровский",
            "Выборгский",
            "Калининский",
            "Кировский",
            "Колпинский",
            "Красногвардейский",
            "Красносельский",
            "Кронштадтский",
            "Курортный",
            "Московский",
            "Невский",
            "Петроградский",
            "Приморский",
            "Пушкинский",
            "Фрунзенский",
            "Центральный"
        ])
        self.layout.addWidget(self.region_label)
        self.layout.addWidget(self.region_combo)

        self.address_label = QLabel("Введите адрес:")
        self.address_input = QLineEdit()
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_input)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Адрес", "Район"])
        self.layout.addWidget(self.table)

        self.address_input.textChanged.connect(self.update_table)
        self.region_combo.currentIndexChanged.connect(self.update_table)

        # Подключаемся к существующей базе данных
        self.conn = sqlite3.connect("restaurant.db")
        self.update_table()  # Начальный вызов обновления таблицы

    def update_table(self):
        region = self.region_combo.currentText()
        address = self.address_input.text()

        cursor = self.conn.cursor()

        # Подготовка запроса
        if region == "Не выбран":
            query = "SELECT address, region FROM restaurants WHERE address LIKE ?"
            cursor.execute(query, (f"%{address}%",))
        else:
            query = "SELECT address, region FROM restaurants WHERE region = ? AND address LIKE ?"
            cursor.execute(query, (region, f"%{address}%"))

        results = cursor.fetchall()
        self.table.setRowCount(len(results))

        for row_idx, (address, region) in enumerate(results):
            self.table.setItem(row_idx, 0, QTableWidgetItem(address))
            self.table.setItem(row_idx, 1, QTableWidgetItem(region))

    def open_setting(self):
        self.close()
        self.open_setting = Setting()
        self.open_setting.show()


class Obnov(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Устанавливаем параметры окна
        self.setGeometry(450, 175, 400, 400)
        self.setWindowTitle('Обновление 2.0')

        # Создаем кнопку "Назад"
        self.btn = QPushButton('Назад', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(165, 365)
        self.btn.clicked.connect(self.open_setting)

        # Создаем метку заголовка
        self.label = QLabel(self)
        self.label.setText("Список изменений или добавлений в обновлении 2.0")
        self.label.move(100, 15)

        # Создаем текстовую область для отображения изменений
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setPlainText(self.get_text_content())
        self.text_area.setGeometry(15, 40, 370, 320)  # Положение и размер текстовой области

    def get_text_content(self):
        return (
            "Обновление 2.0:\n\n"
            "1. Добавить галочку оставаться в аккаунте при выходе.\n"
            "2. Добавить промокоды для привлечения новых клиентов и поощрения существующих.\n"
            "3. Нарисовать новую иконку.\n"
            "4. Добавить возможность делать промокоды на определенное количество раз.\n"
            "5. Добавить реальное время и во сколько был создан заказ.\n"
            "6. Историю заказов сделать базой данных, плюс добавить время заказа.\n"
            "7. Сделать заставку.\n"
            "8. Сделать более сложное создание паролей для повышения безопасности аккаунтов пользователей.\n"
            "9. Сделать поддержку для оперативного решения возникающих вопросов и проблем.\n"
            "10. Добавить пасхалки для создания уникального пользовательского опыта и повышения лояльности.\n"
            "11. Возможность банить аккаунты для предотвращения мошенничества.\n"
            "12. Кнопка выхода из аккаунта для быстрого выхода из приложения.\n"
            "13. Кнопка «Подробнее» для предоставления дополнительной информации о товарах или услугах.\n"
            "14. Картинки для улучшения визуального восприятия и привлечения внимания пользователей.\n"
            "15. Цифр для подтверждения карты увеличить до 16 для повышения безопасности при вводе данных карты.\n"
            "16. Реклама для генерации дохода и продвижения продуктов.\n"
            "17. Приветствие пользователя для создания дружелюбной атмосферы.\n"
            "18. Сохранение любимых заказов для удобства пользователей.\n"
            "19. Кнопка настройки и смену языка для адаптации приложения.\n"
            "20. Поддержка клавиатуры: таб — корзина, на цифры — добавление товаров.\n"
            "21. Розыгрыши еды для привлечения новых пользователей.\n"
            "22. Мини-игры для развлечения пользователей.\n"
            "23. Увеличить меню.\n"
            "24. Полная переработка интерфейса, добавление новых функций.\n"
            "\n"
            "Дополнительные функции:\n"
            "25. Уведомления о готовности заказа, чтобы пользователи знали, когда их заказ будет готов.\n"
            "26. Персонализированные предложения по питанию на основе предпочтений и здоровья.\n"
            "27. Оплата через счет внутри приложения для современных способов оплаты.\n"
            "28. Пополнять счет внутри приложения .\n"
            "29. Карта лояльности с накопительными баллами за каждое действие.\n"
            "30. Онлайн-меню на нескольких языках для удобства пользователей.\n"
            "31. История заказов с фотографиями для визуального подтверждения.\n"
            "32. Рекомендации по блюдам с учетом времени суток.\n"
            "33. Онлайн-обучение по приготовлению блюд с рецептом.\n"
            "34. Обратная связь по качеству обслуживания для улучшения услуг.\n"
            "35. Персонализированные рекомендации по напиткам.\n"
            "36. Интеграция с фитнес-трекерами для достижения целей.\n"
            "37. Уведомления о скидках на определенные дни недели.\n"

            # Добавьте более подробно все изменения или дополнения, которые хотите отобразить.
        )

    def open_setting(self):
        self.close()
        self.open_setting = Setting()  # Убедитесь, что класс Setting определен
        self.open_setting.show()


class Obnov1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Устанавливаем параметры окна
        self.setGeometry(450, 175, 400, 400)
        self.setWindowTitle('Обновление 1.0')

        # Создаем кнопку "Назад"
        self.btn = QPushButton('Назад', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 365)
        self.btn.clicked.connect(self.open_setting)

        # Создаем метку заголовка
        self.label = QLabel(self)
        self.label.setText("Список того что было реализованно в версии 1.0")
        self.label.move(100, 15)

        # Создаем текстовую область для отображения изменений
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setPlainText(self.get_text_content1())
        self.text_area.setGeometry(15, 40, 370, 320)  # Положение и размер текстовой области

    def get_text_content1(self):
        return (
            "Проект представляет собой приложение для онлайн-заказа еды, которое позволяет пользователю просматривать меню, добавлять товары в корзину, оформлять заказы и сохранять историю заказов. Идея проекта заключается в создании удобного и интуитивно понятного интерфейса для пользователей, которые хотят заказать еду с помощью мобильного устройства или компьютера, при этом имея возможность использовать различные дополнительные функции, такие как промокоды, история заказов и настройки аккаунта.\n\n"

            "Описание реализации:\n\n"

            "Основной функционал приложения включает в себя несколько ключевых компонентов. Для реализации этого функционала использовались различные классы и функции, каждая из которых отвечает за определенный аспект работы программы.\n\n"

            "Классы и их роль:\n\n"

            "Класс Product:\n"
            "Этот класс представляет собой отдельное блюдо в меню. Он хранит информацию о названии блюда, его цене и описании. Класс имеет конструктор, который принимает данные о блюде, а также метод для получения информации о блюде. Это позволяет организовать меню и управлять данными о каждом товаре.\n"
            "class Product:\n"
            "    def __init__(self, name, price, description):\n"
            "        self.name = name\n"
            "        self.price = price\n"
            "        self.description = description\n\n"
            "    def get_info(self):\n"
            "        return f'{self.name}: {self.description}, Price: {self.price}'\n\n"

            "Класс Cart:\n"
            "Этот класс управляет корзиной покупок, куда пользователи могут добавлять продукты. Он хранит список товаров, выбранных пользователем, и предоставляет методы для добавления товаров в корзину, удаления товаров и расчета общей стоимости. Также здесь реализована возможность применения скидок, если промокод является действительным.\n"
            "class Cart:\n"
            "    def __init__(self):\n"
            "        self.items = []\n"
            "        self.total_price = 0\n\n"
            "    def add_item(self, product):\n"
            "        self.items.append(product)\n"
            "        self.total_price += product.price\n\n"
            "    def remove_item(self, product):\n"
            "        self.items.remove(product)\n"
            "        self.total_price -= product.price\n\n"

            "Класс Order:\n"
            "Этот класс отвечает за оформление заказа. Он включает информацию о заказанных продуктах, общей стоимости, а также о состоянии заказа (например, 'в процессе', 'доставлен' и т. д.). Класс сохраняет заказ в базе данных после его оформления, чтобы пользователи могли видеть историю своих заказов.\n"
            "class Order:\n"
            "    def __init__(self, cart, user):\n"
            "        self.cart = cart\n"
            "        self.user = user\n"
            "        self.status = 'in progress'\n"
            "        self.total = cart.total_price\n\n"
            "    def save_order(self):\n"
            "        # Логика для сохранения заказа в базе данных\n"
            "        pass\n\n"

            "Класс User:\n"
            "Класс User представляет собой учетную запись пользователя. Он хранит информацию о пользователе, такую как имя, адрес электронной почты, пароль и историю заказов. Этот класс включает методы для регистрации, авторизации и сохранения информации о пользователе в базе данных.\n"
            "class User:\n"
            "    def __init__(self, username, password):\n"
            "        self.username = username\n"
            "        self.password = password\n"
            "        self.orders_history = []\n\n"
            "    def register(self):\n"
            "        # Логика регистрации пользователя\n"
            "        pass\n\n"
            "    def login(self):\n"
            "        # Логика авторизации пользователя\n"
            "        pass\n\n"

            "Класс Database:\n"
            "Класс, управляющий базой данных, используется для хранения информации о пользователях, заказах и других данных, таких как продукты и промокоды. Он реализует основные операции, такие как добавление и извлечение данных.\n"
            "class Database:\n"
            "    def __init__(self):\n"
            "        self.users = []\n"
            "        self.orders = []\n\n"
            "    def add_user(self, user):\n"
            "        self.users.append(user)\n\n"
            "    def add_order(self, order):\n"
            "        self.orders.append(order)\n\n"

            "Взаимодействие классов и функции:\n\n"

            "-Основной поток:\n"
            "Когда пользователь выбирает продукты и добавляет их в корзину, происходит взаимодействие с классом Cart, который управляет всеми товарами в корзине. После того как пользователь завершает выбор, он может применить промокод (если он есть), используя класс PromoCode. После этого создается заказ с помощью класса Order, который сохраняется в базе данных для последующего использования.\n\n"

            "-История заказов:\n"
            "Каждый заказ сохраняется в базе данных с помощью класса Database. Пользователь может просматривать свою историю заказов, благодаря методу orders_history в классе User.\n\n"

            "-База данных:\n"
            "Для хранения данных о пользователях, заказах, блюдах и промокодах используется класс Database. Этот класс реализует операции добавления, извлечения и обновления данных в базе данных.\n\n"

            "Заключение:\n\n"
            "Проект представляет собой полноценное приложение для онлайн-заказа еды с широким набором функций, включая корзину, историю заказов, промокоды и настройки пользователя. Классы, такие как Product, Cart, Order, User, PromoCode и Database, взаимодействуют друг с другом, создавая удобный и функциональный интерфейс для пользователей.\n\n"

            "Возможности для доработки и развития включают расширение функционала, например, добавление новых способов оплаты, улучшение интерфейса с использованием изображений и анимаций, а также интеграцию с другими сервисами для улучшения пользовательского опыта. В дальнейшем можно реализовать поддержку многопользовательских учетных записей, добавление отзывов о блюдах и внедрение системы лояльности для постоянных клиентов.\n"
        )

    def open_setting(self):
        self.close()
        self.open_setting = Setting()  # Убедитесь, что класс Setting определен
        self.open_setting.show()


# Окно для корзины
class CartWindow(QWidget):
    def __init__(self, cart, order_history, user_id):
        super().__init__()
        self.setWindowTitle("Корзина")
        self.cart = cart
        self.order_history = order_history
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.cart_table = QTableWidget()
        self.cart_table.setRowCount(len(self.cart))
        self.cart_table.setColumnCount(3)
        self.cart_table.setHorizontalHeaderLabels(["Наименование", "Цена (руб)", "Удалить"])

        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item.name))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(item.price)))
            remove_button = QPushButton("Убрать")
            remove_button.clicked.connect(lambda checked, row=row: self.remove_item(row))
            self.cart_table.setCellWidget(row, 2, remove_button)

        layout.addWidget(self.cart_table)

        # Кнопки заказа и возврата в меню
        order_button = QPushButton("Заказать")
        order_button.clicked.connect(self.open_order_dialog)
        layout.addWidget(order_button)

        back_button = QPushButton("Назад в меню")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def remove_item(self, row):
        item_name = self.cart[row].name
        self.cart.pop(row)  # Удаляем товар из корзины
        QMessageBox.information(self, "Удалено из корзины", f"{item_name} убрано из корзины!")
        self.refresh_cart()

    def refresh_cart(self):
        self.cart_table.setRowCount(len(self.cart))
        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item.name))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(item.price)))
            remove_button = QPushButton("Убрать")
            remove_button.clicked.connect(lambda checked, row=row: self.remove_item(row))
            self.cart_table.setCellWidget(row, 2, remove_button)

    def open_order_dialog(self):
        if not self.cart:
            QMessageBox.information(self, "Корзина пуста", "Добавьте товары в корзину для оформления заказа.")
            return
        self.order_dialog = OrderDialog(self.cart, self.user_id)
        self.order_dialog.show()
        self.close()


# Окно для ввода данных карты
class OrderDialog(QWidget):
    def __init__(self, cart, user_id):
        super().__init__()
        self.setWindowTitle("Введите данные карты")
        self.cart = cart
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Введите 16 цифр номера карты")
        layout.addWidget(self.card_number_input)

        pay_button = QPushButton("Оплатить")
        pay_button.clicked.connect(self.confirm_order)
        layout.addWidget(pay_button)

        self.setLayout(layout)

    def confirm_order(self):
        valid_promo_codes = ["DISCOUNT10", "FREESHIP", "WELCOME50", "NEWYEAR15", "пж100баллов", "NEWYEAR", "MACMENU",
                             "1"]
        card_number = self.card_number_input.text()
        if len(card_number) == 16 and card_number.isdigit() or card_number in valid_promo_codes:
            # Save the order in the database
            order_details = ', '.join([item.name for item in self.cart])
            self.save_order(order_details)
            self.cart.clear()  # Empty the cart
            QMessageBox.information(self, "Заказ подтвержден", "Ваш заказ успешно оплачен!")
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный номер карты или промокод. Введите корректные данные.")

    def save_order(self, order_details):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Insert order into orders table
        cursor.execute('INSERT INTO orders (user_id, order_details, status) VALUES (?, ?, ?)',
                       (self.user_id, order_details, "Оплачен"))

        conn.commit()
        conn.close()


# Окно истории заказов
class OrderHistoryWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("История заказов")
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.history_table = QTableWidget()
        self.history_table.setRowCount(0)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Заказ", "Статус"])

        # Fetch order history from the database
        self.load_order_history()

        layout.addWidget(self.history_table)

        back_button = QPushButton("Назад в меню")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_order_history(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Fetch orders for the current user
        cursor.execute('SELECT order_details, status FROM orders WHERE user_id=?', (self.user_id,))
        orders = cursor.fetchall()

        conn.close()

        # Add each order to the table
        for order in orders:
            order_details, status = order
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(order_details))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(status))


# Главное окно с функциями регистрации и входа
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в аккаунт")
        self.layout = QVBoxLayout()

        self.pixmap = QPixmap('icons8-знак-чередования-эмоджи-48.jpg')
        self.image = QLabel(self)
        self.image.move(10, 0)
        self.image.resize(270, 140)
        self.image.setPixmap(self.pixmap)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.open_registration)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def open_registration(self):
        self.close()
        self.registration_window = Registration(self)
        self.registration_window.show()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute('SELECT id, name FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id, name = result
            self.close()
            self.main_window = MainWindow(user_id)
            self.main_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")


# Окно регистрации
class Registration(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Регистрация")
        self.layout = QVBoxLayout()

        self.pixmap = QPixmap('icons8-знак-чередования-эмоджи-48.jpg')
        self.image = QLabel(self)
        self.image.move(10, 0)
        self.image.resize(270, 140)
        self.image.setPixmap(self.pixmap)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.register_button = QPushButton("Войти")
        self.register_button.clicked.connect(self.open_login)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def open_login(self):
        self.close()
        self.login_window = Login()
        self.login_window.show()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя и пароль обязательны!")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            QMessageBox.information(self, "Успех", "Учетная запись успешно создана!")
            self.close()
            self.login_window.show()  # Open login window after successful registration
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Это имя пользователя уже занято.")
        finally:
            conn.close()


if __name__ == "__main__":
    init_db()  # Инициализация базы данных
    add_user_id_column()  # Add user_id column if it's missing
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec())  # Запуск приложения
