# Імпортуємо необхідні класи з PyQt5 для побудови графічного інтерфейсу
from PyQt5.QtCore import Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont # перевірка типів введених значень
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QGroupBox, QRadioButton,
    QPushButton, QLabel, QListWidget, QLineEdit)

# Імпортуємо модуль instr та final_win (передбачається, що вони існують у тому ж каталозі)
from instr import *
from final_win import *

# Клас, який представляє експеримент
class Experiment():
    def __init__(self, age, test1, test2, test3):
        self.age = age
        self.t1 = test1
        self.t2 = test2
        self.t3 = test3

# Головне вікно програми
class TestWin(QWidget):
    def __init__(self):
        ''' вікно, в якому проводиться опитування '''
        super().__init__()

        # створюємо та налаштовуємо графічні елементи:
        self.initUI()

        # Встановлюємо зв'язки між елементами
        self.connects()

        # Встановлюємо вигляд вікна (напис, розмір, місце)
        self.set_appear()

        # Запускаємо вікно:
        self.show()

    ''' Встановлює вигляд вікна (напис, розмір, місце) '''
    def set_appear(self):
        self.setWindowTitle(txt_title)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    ''' Створює графічні елементи '''
    def initUI(self):
        # Створюємо кнопки для різних тестів
        self.btn_next = QPushButton(txt_sendresults, self)
        self.btn_test1 = QPushButton(txt_starttest1, self)
        self.btn_test2 = QPushButton(txt_starttest2, self)
        self.btn_test3 = QPushButton(txt_starttest3, self)

        # Створюємо написи та поля вводу
        self.text_name = QLabel(txt_name)
        self.text_age = QLabel(txt_age)
        self.text_test1 = QLabel(txt_test1)
        self.text_test2 = QLabel(txt_test2)
        self.text_test3 = QLabel(txt_test3)
        self.text_timer = QLabel(txt_timer)
        self.text_timer.setFont(QFont("Times", 36, QFont.Bold))

        self.line_name = QLineEdit(txt_hintname)
        self.line_age = QLineEdit(txt_hintage)
        self.line_test1 = QLineEdit(txt_hinttest1)
        self.line_test2 = QLineEdit(txt_hinttest2)
        self.line_test3 = QLineEdit(txt_hinttest3)

        # Встановлюємо розмітку для елементів
        self.l_line = QVBoxLayout()
        self.r_line = QVBoxLayout()
        self.h_line = QHBoxLayout()

        # Додаємо елементи в розмітку
        self.r_line.addWidget(self.text_timer, alignment=Qt.AlignCenter)
        self.l_line.addWidget(self.text_name, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.line_name, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.text_age, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.line_age, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.text_test1, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.btn_test1, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.line_test1, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.text_test2, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.btn_test2, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.text_test3, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.btn_test3, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.line_test2, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.line_test3, alignment=Qt.AlignLeft)
        self.l_line.addWidget(self.btn_next, alignment=Qt.AlignCenter)
        self.h_line.addLayout(self.l_line)
        self.h_line.addLayout(self.r_line)
        self.setLayout(self.h_line)

    # Метод, який викликається після натискання кнопки "Далі"
    def next_click(self):
        self.hide()
        # Створюємо екземпляр класу Experiment з введеними даними
        self.exp = Experiment(int(self.line_age.text()), self.line_test1.text(), self.line_test2.text(), self.line_test3.text())
        # Створюємо і показуємо вікно з підсумковими результатами (клас FinalWin)
        self.fw = FinalWin(self.exp)

    # Метод для запуску таймера для першого тесту
    def timer_test(self):
        global time
        time = QTime(0, 0, 15)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer1Event)
        self.timer.start(1000)

    # Метод для запуску таймера для другого тесту
    def timer_sits(self):
        global time
        time = QTime(0, 0, 30)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer2Event)
        # Один цикл присідання триває 1.5 секунди
        self.timer.start(1500)

    # Метод для запуску таймера для третього тесту
    def timer_final(self):
        global time
        time = QTime(0, 1, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer3Event)
        self.timer.start(1000)

    # Обробник події таймера для першого тесту
    '''Ця функція викликається, коли таймер для першого тесту генерує подію.
      Зменшуємо значення глобальної змінної time на 1 секунду за допомогою time.addSecs(-1).
      Оновлюємо відображення часу на екрані з використанням методу setText.
      Налаштовуємо шрифт для надпису часу з використанням setFont.
      Встановлюємо колір шрифту на чорний за допомогою setStyleSheet.
      Якщо час досяг "00:00:00", зупиняємо таймер за допомогою self.timer.stop().'''
    def timer1Event(self):
        global time
        time = time.addSecs(-1)
        self.text_timer.setText(time.toString("hh:mm:ss"))
        self.text_timer.setFont(QFont("Times", 36, QFont.Bold))
        self.text_timer.setStyleSheet("color: rgb(0,0,0)")
        if time.toString("hh:mm:ss") == "00:00:00":
            self.timer.stop()

    # Обробник події таймера для другого тесту
    ''' (Обробник події таймера для другого тесту):

   Ця функція подібна до попередньої, але має інший підхід до відображення часу.
   Знову зменшуємо значення time на 1 секунду.
   Оновлюємо лише останні 2 символи відображення часу (хвилини та секунди) з використанням time.toString("hh:mm:ss")[6:8].
   Налаштовуємо шрифт та колір так, як і в попередньому випадку.
   При досягненні часу "00:00:00" зупиняємо таймер.'''
    def timer2Event(self):
        global time
        time = time.addSecs(-1)
        self.text_timer.setText(time.toString("hh:mm:ss")[6:8])
        self.text_timer.setStyleSheet("color: rgb(0,0,0)")
        self.text_timer.setFont(QFont("Times", 36, QFont.Bold))
        if time.toString("hh:mm:ss") == "00:00:00":
            self.timer.stop()

    # Обробник події таймера для третього тесту
    '''Ця функція також подібна до попередньої, але вона використовує різний підхід до зміни кольору тексту відображення часу.
   Знову зменшуємо значення time на 1 секунду.
   Оновлюємо відображення часу, встановлюючи його повністю.
   Залежно від значення секунд відображення часу, змінюємо колір тексту на зелений, якщо залишилося 45 
   або більше секунд, або червоний, якщо залишилося 15 або менше секунд. В інших випадках текст залишається чорним.
   Налаштовуємо шрифт і також зупиняємо таймер при досягненні часу "00:00:00".'''
    def timer3Event(self):
        global time
        time = time.addSecs(-1)
        self.text_timer.setText(time.toString("hh:mm:ss"))
        if int(time.toString("hh:mm:ss")[6:8]) >= 45:
            self.text_timer.setStyleSheet("color: rgb(0,255,0)")
        elif int(time.toString("hh:mm:ss")[6:8]) <= 15:
            self.text_timer.setStyleSheet("color: rgb(0,255,0)")
        else:
            self.text_timer.setStyleSheet("color: rgb(0,0,0)")
        self.text_timer.setFont(QFont("Times", 36, QFont.Bold))
        if time.toString("hh:mm:ss") == "00:00:00":
            self.timer.stop()

    # Встановлюємо зв'язки між графічними елементами
    def connects(self):
        self.btn_next.clicked.connect(self.next_click)
        self.btn_test1.clicked.connect(self.timer_test)
        self.btn_test2.clicked.connect(self.timer_sits)
        self.btn_test3.clicked.connect(self.timer_final)
