import sys
import random
import time
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QButtonGroup, QDialog, QTabWidget,\
    QVBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setGeometry(700, 100, 640, 880)
        # создание кнопок и добавление их в button_table
        self.button_table = []
        for i in range(9):
            self.bg = QButtonGroup()
            self.bg.setExclusive(True)
            self.button_table.append(self.bg)
            for j in range(9):
                self.btn = Sudoku_button(self)
                self.btn.setText("")
                self.btn.set_standart_font()
                self.btn.set_standart_colour()
                self.button_table[-1].addButton(self.btn)
                self.btn.clicked.connect(self.define_button)
                self.btn.setGeometry(10 + 70 * j, 250 + 70 * i, 60, 60)
        # другие визуальные элементы
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(205, 250, 20, 621))
        self.line.setMidLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(415, 250, 20, 621))
        self.line_2.setLineWidth(1)
        self.line_2.setMidLineWidth(5)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setGeometry(QtCore.QRect(10, 445, 621, 20))
        self.line_3.setMidLineWidth(5)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setGeometry(QtCore.QRect(10, 655, 621, 20))
        self.line_4.setMidLineWidth(5)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.new_game_button = QtWidgets.QPushButton(Form)
        self.new_game_button.setGeometry(QtCore.QRect(440, 10, 190, 50))
        self.new_game_button.setFont(QtGui.QFont('Arial', 12))
        self.new_game_button.setObjectName("new_game_button")
        self.difficult_box = QtWidgets.QComboBox(Form)
        self.difficult_box.setGeometry(QtCore.QRect(290, 10, 150, 50))
        self.difficult_box.setFont(QtGui.QFont('Arial', 12))
        self.difficult_box.setObjectName("difficult_box")
        self.difficult_box.addItem("")
        self.difficult_box.addItem("")
        self.difficult_box.addItem("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 310, 50))
        self.label.setObjectName("label")
        self.label.setFont(QtGui.QFont('Arial', 12))
        self.time_label = QtWidgets.QLabel(Form)
        self.time_label.setGeometry(QtCore.QRect(280, 180, 200, 75))
        self.time_label.setFont(QtGui.QFont('Arial', 30))
        self.time_label.setObjectName("time_label")
        self.table_button = QtWidgets.QPushButton(Form)
        self.table_button.setGeometry(QtCore.QRect(380, 60, 250, 50))
        self.table_button.setFont(QtGui.QFont('Arial', 15))
        self.table_button.setObjectName("table_button")
        self.hint_button = QtWidgets.QPushButton(Form)
        self.hint_button.setGeometry(QtCore.QRect(10, 60, 150, 50))
        self.hint_button.setFont(QtGui.QFont('Arial', 15))
        self.hint_button.setObjectName("hint_button")
        self.solution_button = QtWidgets.QPushButton(Form)
        self.solution_button.setGeometry(QtCore.QRect(170, 60, 200, 50))
        self.solution_button.setFont(QtGui.QFont('Arial', 15))
        self.solution_button.setObjectName("solution_button")
        self.help_button = QtWidgets.QPushButton(Form)
        self.help_button.setGeometry(QtCore.QRect(10, 120, 200, 50))
        self.help_button.setFont(QtGui.QFont('Arial', 15))
        self.help_button.setObjectName("help_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sudoku"))
        self.new_game_button.setText(_translate("Form", "Начать новую игру"))
        self.difficult_box.setItemText(0, _translate("Form", "легкий"))
        self.difficult_box.setItemText(1, _translate("Form", "нормальный"))
        self.difficult_box.setItemText(2, _translate("Form", "сложный"))
        self.label.setText(_translate("Form", "Выберите уровень сложности:"))
        self.time_label.setText(_translate("Form", "0:00"))
        self.table_button.setText(_translate("Form", "Таблица рекордов"))
        self.hint_button.setText(_translate("Form", "Подсказка"))
        self.solution_button.setText(_translate("Form", "Показать ответ"))
        self.help_button.setText(_translate("Form", "Помощь"))


class Sudoku(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("icon.png"))
        # вспомогательные переменные
        self.selected_btn = None
        self.selected_btn_coords = []
        self.key_nums = []
        self.game_is_on = False
        self.time_is_on = False
        self.hints = 0
        # бинд кнопок
        self.new_game_button.clicked.connect(self.start_new_game)
        self.solution_button.clicked.connect(self.show_answer)
        self.hint_button.clicked.connect(self.give_hint)
        self.help_button.clicked.connect(self.show_help_w)
        self.table_button.clicked.connect(self.show_table_window)

    # функция для выбора кнопки
    def define_button(self):
        self.paint_button(self.sender())
        for n, i in enumerate(self.button_table):
            if self.sender() in i.buttons():
                self.selected_btn_coords = [n, i.buttons().index(self.sender())]

    # функция для покраски выбранной кнопки
    def paint_button(self, btn):
        if self.selected_btn != None:
            self.selected_btn.unmark_chosen_btn()
            self.selected_btn = btn
            self.selected_btn.mark_as_chosen()
        else:
            self.selected_btn = btn
            self.selected_btn.mark_as_chosen()

    # функция переводящая кнопку в альтернативный режим
    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            if self.selected_btn != None:
                if self.game_is_on:
                    self.selected_btn.change_mode()

    # функция для начала новой игры
    def start_new_game(self):
        # интерпретация выбранного уровня сложности
        self.difficult = self.difficult_box.currentText()
        if self.difficult == 'легкий':
            dif_lvl = 1
        elif self.difficult == 'нормальный':
            dif_lvl = 2
        else:
            dif_lvl = 3
        # получение полей: игрока и ответов
        f = Field(dif_lvl)
        self.solution, self.puzzle = f.get_fields()
        self.show_puzzle(self.puzzle)
        self.game_is_on = True
        self.hints = 4 - dif_lvl
        # запуск таймера
        self.start_timer()

    # функция отображающая поле
    def show_puzzle(self, puzzle):
        self.key_nums = []
        # итерация по таблице с полем игрока
        for rowind, i in enumerate(self.button_table):
            for colind, j in enumerate(i.buttons()):
                # если значение известно изначально
                if puzzle[rowind][colind] != ' ':
                    self.key_nums.append([rowind, colind])
                    j.setText(str(puzzle[rowind][colind]))
                    j.mark_as_unchangeble()
                # иначе
                else:
                    j.setText(str(puzzle[rowind][colind]))
                    j.set_standart_colour()

    # функция запускающая таймер
    def start_timer(self):
        self.time_label.setText('0:00')
        if not self.time_is_on:
            self.startTimer(1000)
        self.time_is_on = True

    # функция считающая время
    def timerEvent(self, *args, **kwargs):
        if self.game_is_on:
            time = [int(i) for i in self.time_label.text().split(':')]
            mins = time[0] * 60 + time[1]
            mins += 1
            self.time_label.setText(':'.join([str(mins // 60), str(mins % 60).rjust(2, '0')]))

    # функция обрабатывающая нажатия с клавиатуры
    def keyPressEvent(self, event):
        if self.game_is_on and self.selected_btn != None and self.selected_btn_coords not in self.key_nums:
            if event.key() == 49:
                self.selected_btn.change_value(1)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 1
                self.end()
            if event.key() == 50:
                self.selected_btn.change_value(2)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 2
                self.end()
            if event.key() == 51:
                self.selected_btn.change_value(3)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 3
                self.end()
            if event.key() == 52:
                self.selected_btn.change_value(4)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 4
                self.end()
            if event.key() == 53:
                self.selected_btn.change_value(5)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 5
                self.end()
            if event.key() == 54:
                self.selected_btn.change_value(6)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 6
                self.end()
            if event.key() == 55:
                self.selected_btn.change_value(7)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 7
                self.end()
            if event.key() == 56:
                self.selected_btn.change_value(8)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 8
                self.end()
            if event.key() == 57:
                self.selected_btn.change_value(9)
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = 9
                self.end()
            if event.key() == 16777219:
                self.selected_btn.change_value(' ')
                self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = ' '
                self.end()
        if self.selected_btn != None:
            if event.key() == 87:
                self.paint_button(self.button_table[(self.selected_btn_coords[0] - 1) % 9].buttons()[self.selected_btn_coords[1]])
                self.selected_btn_coords[0] = (self.selected_btn_coords[0] - 1) % 9
            elif event.key() == 68:
                self.paint_button(self.button_table[self.selected_btn_coords[0]].buttons()[(self.selected_btn_coords[1] + 1) % 9])
                self.selected_btn_coords[1] = (self.selected_btn_coords[1] + 1) % 9
            elif event.key() == 83:
                self.paint_button(self.button_table[(self.selected_btn_coords[0] + 1) % 9].buttons()[self.selected_btn_coords[1]])
                self.selected_btn_coords[0] = (self.selected_btn_coords[0] + 1) % 9
            elif event.key() == 65:
                self.paint_button(self.button_table[self.selected_btn_coords[0]].buttons()[(self.selected_btn_coords[1] - 1) % 9])
                self.selected_btn_coords[1] = (self.selected_btn_coords[1] - 1) % 9

    # функция заканчивающая игру
    def end(self):
        if self.puzzle == self.solution:
            self.game_is_on = False
            # обновление БД
            name, okBtnPressed = QInputDialog.getText(self, "Введите имя",
                                                   "Введите имя для занесения в рекордную таблицу")
            if okBtnPressed:
                t = int(self.time_label.text().split(':')[0]) * 60 + int(self.time_label.text().split(':')[1])
                self.update_db([name, t])

    # функция выводящая ответ
    def show_answer(self):
        if self.game_is_on:
            # итерация по списку с кнопками и отображение верного ответа
            for rowind, i in enumerate(self.button_table):
                for colind, j in enumerate(i.buttons()):
                    if self.puzzle[rowind][colind] != self.solution[rowind][colind]:
                        j.setText(str(self.solution[rowind][colind]))
                        j.mark_as_wa()
        self.game_is_on = False

    # функция показывающая подсказку
    def give_hint(self):
        if self.game_is_on and self.hints != 0 and self.selected_btn.colour_state == 'st':
            # тображение правильного значения
            self.selected_btn.set_standart_mode()
            self.puzzle[self.selected_btn_coords[0]][self.selected_btn_coords[1]] = \
                self.solution[self.selected_btn_coords[0]][self.selected_btn_coords[1]]
            self.selected_btn.setText(
                str(self.solution[self.selected_btn_coords[0]][self.selected_btn_coords[1]]))
            # перевод кнопки в неизменяемый режим
            self.key_nums += self.selected_btn_coords
            self.selected_btn.mark_as_unchangeble()
            self.hints -= 1
            self.end()
        # оповещение о том, что кончинись подсказки
        elif self.hints == 0 and self.game_is_on:
            self.hw = OutOfHintsWindow()
            self.hw.show()

    # функция показывающая окно с подсказками
    def show_help_w(self):
        self.hw = HelpWindow()
        self.hw.show()

    # функция показывающая таблицу рекордов
    def show_table_window(self):
        self.tw = TableWindow()
        self.tw.show()

    # функция для обновления БД
    def update_db(self, data):
        if self.difficult == 'легкий':
            self.update_es_sheet(data)
        elif self.difficult == 'нормальный':
            self.update_nm_sheet(data)
        else:
            self.update_hd_sheet(data)

    # функция обновляющая EasyMode таблицу
    def update_es_sheet(self, d):
        con = sqlite3.connect("record sheet.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM EasyMode").fetchall()
        #получение текущий таблицы
        place = [0, len(result)]
        time = d[1]
        # поиск места, занятого игроком
        while place[0] != place[1]:
            n = (place[1] - place[0]) // 2 + place[0]
            nt = int(result[n][2].split(':')[0]) * 60 + int(result[n][2].split(':')[1])
            if time > nt:
                place[0] = n + 1
            elif time < nt:
                place[1] = n
            else:
                place = [n, n]
        place = place[0]
        #корриктировка данных
        d = [place] + d
        result.insert(place, d)
        d[2] = ':'.join([str(d[2] // 60), str(d[2] % 60).rjust(2, '0')])
        # занесение новых данных в таблицу
        for s in result[place:-1]:
            con.execute("UPDATE EasyMode SET Name = ?, Time = ? WHERE Place = ?",
                        (s[1], s[2], s[0] + 1))
            con.commit()
        con.execute("INSERT INTO EasyMode(Place, Name, Time) VALUES(?, ?, ?)",
                    (result[-1][0] + 1, result[-1][1], result[-1][2]))
        con.commit()

    # функция обновляющая NormMode таблицу
    def update_nm_sheet(self, d):
        con = sqlite3.connect("record sheet.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM NormMode").fetchall()
        #получение текущий таблицы
        place = [0, len(result)]
        time = d[1]
        # поиск места, занятого игроком
        while place[0] != place[1]:
            n = (place[1] - place[0]) // 2 + place[0]
            nt = int(result[n][2].split(':')[0]) * 60 + int(result[n][2].split(':')[1])
            if time > nt:
                place[0] = n + 1
            elif time < nt:
                place[1] = n
            else:
                place = [n, n]
        place = place[0]
        #корриктировка данных
        d = [place] + d
        result.insert(place, d)
        d[2] = ':'.join([str(d[2] // 60), str(d[2] % 60).rjust(2, '0')])
        # занесение новых данных в таблицу
        for s in result[place:-1]:
            con.execute("UPDATE NormMode SET Name = ?, Time = ? WHERE Place = ?",
                        (s[1], s[2], s[0] + 1))
            con.commit()
        con.execute("INSERT INTO NormMode(Place, Name, Time) VALUES(?, ?, ?)",
                    (result[-1][0] + 1, result[-1][1], result[-1][2]))
        con.commit()

    # функция обновляющая HardMode таблицу
    def update_hd_sheet(self, d):
        con = sqlite3.connect("record sheet.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM HardMode").fetchall()
        # получение текущий таблицы
        place = [0, len(result)]
        time = d[1]
        # поиск места, занятого игроком
        while place[0] != place[1]:
            n = (place[1] - place[0]) // 2 + place[0]
            nt = int(result[n][2].split(':')[0]) * 60 + int(result[n][2].split(':')[1])
            if time > nt:
                place[0] = n + 1
            elif time < nt:
                place[1] = n
            else:
                place = [n, n]
        place = place[0]
        # корриктировка данных
        d = [place] + d
        result.insert(place, d)
        d[2] = ':'.join([str(d[2] // 60), str(d[2] % 60).rjust(2, '0')])
        # занесение новых данных в таблицу
        for s in result[place:-1]:
            con.execute("UPDATE HardMode SET Name = ?, Time = ? WHERE Place = ?",
                        (s[1], s[2], s[0] + 1))
            con.commit()
        con.execute("INSERT INTO HardMode(Place, Name, Time) VALUES(?, ?, ?)",
                    (result[-1][0] + 1, result[-1][1], result[-1][2]))
        con.commit()


# классы вспомогательных окон
class OutOfHintsWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.init_ui(args)

    def init_ui(self, args):
        self.setWindowTitle('Hint window')
        self.setGeometry(800, 500, 350, 50)
        self.label = QtWidgets.QLabel(self)
        self.label.setText('У вас закончились подсказки.')
        self.label.setGeometry(0, 0, 350, 50)
        self.label.setFont(QtGui.QFont('Arial', 15))


class HelpWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.init_ui(args)

    def init_ui(self, args):
        self.setWindowTitle('Help')
        self.setGeometry(800, 300, 415, 470)
        self.label = QtWidgets.QLabel(self)
        self.label.setFont(QtGui.QFont('Arial', 10))
        self.label.setText(" Правила игры:\n"
                           " Внутри игрового поля находятся\n"
                           " 9 'квадратов' (состоящих из 3 x 3 клеток). Каждая\n"
                           " горизонтальная строка, вертикальный столбец\n"
                           " и квадрат (9 клеток каждый) должны заполняться\n"
                           " цифрами 1-9, не повторяя никаких чисел в строке,\n"
                           " столбце или квадрате.\n"
                           "\n"
                           " Как играть:\n"
                           " Выберите уровень сложности и нажмите кнопку\n"
                           " 'Начать новую игру'.\n"
                           " Выбирайти клетки нажатием ЛКМ и вводите цифры.\n"
                           " Стирайте зачения нажатием на клавишу BackSpace.\n"
                           " Вы можете поменять режим клетки нажатием ПКМ.\n"
                           " В альтернативном режиме вы можете записывать\n"
                           " предполагаемые значения. Что бы убрать цифру\n"
                           " нажмите на её кнопку ещё раз.\n"
                           " Нажав на кнопку 'Подсказка' вы получите верное\n"
                           " значение для выбранной кнопки.\n"
                           " Нажав на кнопку 'Показать ответ' вы получите\n"
                           " верный ответ, но победа не засчитается.\n"
                           " Нажав на кнопку 'Таблица рекордов' вы\n"
                           " увидите таблицу, в которой показаны рекорды.")


class Field:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        def_row = [i for i in range(1, 10)]
        random.shuffle(def_row)
        self.table = [[def_row[(i * 3 + i // 3 + j) % 9] for j in range(3 * 3)] for i in range(3 * 3)]
        self.shuffle_table()

    def shuffle_table(self):
        # функции для перемешивания таблицы
        def transposing():
            # транспонирование таблицы
            self.table = list(map(list, zip(*self.table)))

        def swap_small_rows():
            # получение случайного района и случайной строки
            area = random.randrange(0, 3)
            line1 = random.randrange(0, 3)
            s1 = area * 3 + line1
            # номер 1 строки для обмена
            line2 = random.randrange(0, 3)
            s2 = area * 3 + line2
            # номер 2 строки для обмена
            if s1 == s2:
                return
            self.table[s1], self.table[s2] = self.table[s2], self.table[s1]

        def swap_small_columns():
            transposing()
            swap_small_rows()
            transposing()

        def swap_rows():
            # получение случайных районов
            area1 = random.randrange(0, 3)
            area2 = random.randrange(0, 3)
            if area1 == area2:
                return
            # перемешивание районов
            for i in range(0, 3):
                n1, n2 = area1 * 3 + i, area2 * 3 + i
                self.table[n1], self.table[n2] = self.table[n2], self.table[n1]

        def swap_colums():
            transposing()
            swap_rows()
            transposing()

        l = [i for i in range(5)]
        random.shuffle(l)
        for i in l:
            if i == 0:
                for j in range(random.randint(1, 4)):
                    transposing()
            elif i == 1:
                for j in range(random.randint(1, 4)):
                    swap_small_columns()
            elif i == 2:
                for j in range(random.randint(1, 4)):
                    swap_small_columns()
            elif i == 3:
                for j in range(random.randint(1, 4)):
                    swap_rows()
            elif i == 4:
                for j in range(random.randint(1, 4)):
                    swap_colums()

    def make_player_field(self, dif):
        def can_solve(puzzle):
            if how_many_solutions(puzzle) == 1:
                return True
            return False

        def how_many_solutions(field):
            for i in range(9):
                for j in range(9):
                    if field[i][j] == ' ':
                        possible_nums = find_possible_values(i, j, field)
                        num_of_solutions = len(possible_nums)
                        if num_of_solutions <= dif:
                            solutions = 0
                            for v in possible_nums:
                                field_copy = [row.copy() for row in field]
                                field_copy[i][j] = v
                                solutions += how_many_solutions(field_copy)
                                return solutions
            if field == self.table:
                return 1
            else:
                return 0

        def find_possible_values(row_index, column_index, puzzle):
            values = {v for v in range(1, 10)}
            values -= get_row_values(row_index, puzzle)
            values -= get_column_values(column_index, puzzle)
            values -= get_block_values(row_index, column_index, puzzle)
            return values

        def get_row_values(row_index, puzzle):
            return set(puzzle[row_index][:])

        def get_column_values(column_index, puzzle):
            return {puzzle[r][column_index] for r in range(9)}

        def get_block_values(row_index, column_index, puzzle):
            block_row_start = 3 * (row_index // 3)
            block_column_start = 3 * (column_index // 3)
            return {
                puzzle[block_row_start + r][block_column_start + c]
                for r in range(3)
                for c in range(3)
            }

        player_field = [i.copy() for i in self.table]
        coords_list = [(i, j) for j in range(9) for i in range(9)]
        random.shuffle(coords_list)
        if dif == 1:
            dc = 46
        elif dif == 2:
            dc = 51
        elif dif == 3:
            dc = 56
        for r, c in coords_list:
            t = player_field[r][c]
            player_field[r][c] = ' '
            solve_field = [i.copy() for i in player_field]
            if not can_solve(solve_field):
                player_field[r][c] = t
                dc += 1
            dc -= 1
            if dc == 0:
                break
        return player_field

    def get_fields(self):
        return self.table, self.make_player_field(self.difficulty)


class Sudoku_button(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colour_state = None
        self.mode = 's'

# функции связанные с изменением режима кнопки
    def change_mode(self):
        if self.colour_state == 'unch':
            return
        if self.mode == 'g':
            self.set_standart_mode()
            self.mode = 's'
        else:
            self.set_guess_mode()
            self.mode = 'g'

    def set_standart_mode(self):
        self.set_standart_font()
        self.setText(' ')

    def set_guess_mode(self):
        self.set_guess_font()
        text = ['?    ',
                '     ',
                '     ',
                '     ',]
        self.setText('\n'.join(text))

    def set_guess_font(self):
        self.setFont(QtGui.QFont('Arial', 8))

    def change_value(self, v):
        if self.mode == 's':
            self.change_standart_val(v)
        else:
            self.change_guess_val(v)

    def change_standart_val(self, v):
        self.setText(str(v))

    def change_guess_val(self, v):
        if v == ' ':
            return
        text = self.text().split('\n')
        if text[(v - 1) // 3 + 1][(v - 1) % 3 * 2] == str(v):
            print(1)
            text[(v - 1) // 3 + 1] = text[(v - 1) // 3 + 1][:(v - 1) % 3 * 2] + ' ' +\
                                     text[(v - 1) // 3 + 1][(v - 1) % 3 * 2 + 1:]
        else:
            text[(v - 1) // 3 + 1] = text[(v - 1) // 3 + 1][:(v - 1) % 3 * 2] + str(v) + \
                                     text[(v - 1) // 3 + 1][(v - 1) % 3 * 2 + 1:]
        self.setText('\n'.join(text))

    def set_standart_font(self):
        self.setFont(QtGui.QFont('Arial', 26))
# ------------------------------
# функции связанные с изменением цвета кнопки
    def set_standart_colour(self):
        self.setStyleSheet("background-color:#d0d0d0;")
        self.colour_state = 'st'

    def mark_as_unchangeble(self):
        self.setStyleSheet("background-color:#a0c0a0;")
        self.colour_state = 'unch'

    def mark_as_wa(self):
        self.setStyleSheet("background-color:#a00000;")
        self.colour_state = 'wa'

    def mark_as_chosen(self):
        self.setStyleSheet('QPushButton {background-color: #A3C1DA}')

    def unmark_chosen_btn(self):
        if self.colour_state == 'st':
            self.set_standart_colour()
        elif self.colour_state == 'unch':
            self.mark_as_unchangeble()
        elif self.colour_state == 'wa':
            self.mark_as_wa()
    # -------------------------------------


# класс окна с таблицей рекордов и его вспомогательные классы
class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(800, 300, 450, 500)
        self.tabwid = QTabWidget()
        self.tabwid.addTab(EasyTab(), 'Легкий уровень')
        self.tabwid.addTab(NormTab(), 'Нормальный уровень')
        self.tabwid.addTab(HardTab(), 'Сложный уровень')


        self.vb = QVBoxLayout()
        self.vb.addWidget(self.tabwid)

        self.setLayout(self.vb)


class EasyTab(QWidget):
    def __init__(self):
        super(EasyTab, self).__init__()
        t = QTableWidget(self)
        t.setGeometry(0, 0, 500, 500)
        t.setColumnCount(3)
        con = sqlite3.connect("record sheet.db")
        cur = con.cursor()
        #установка заголовков
        headers = con.execute("""PRAGMA table_info(EasyMode)""")
        headers = [i[1] for i in headers]
        t.setHorizontalHeaderLabels(headers)
        # вывод результата
        result = cur.execute("SELECT * FROM EasyMode").fetchall()
        for ri, r in enumerate(result):
            t.setRowCount(t.rowCount() + 1)
            for ci, c in enumerate(r):
                t.setItem(ri, ci, QTableWidgetItem(str(c)))


class NormTab(QWidget):
    def __init__(self):
        super(NormTab, self).__init__()
        t = QTableWidget(self)
        t.setGeometry(0, 0, 500, 500)
        t.setColumnCount(3)
        con = sqlite3.connect("record sheet.db")
        cur = con.cursor()
        #установка заголовков
        headers = con.execute("""PRAGMA table_info(NormMode)""")
        headers = [i[1] for i in headers]
        t.setHorizontalHeaderLabels(headers)
        # вывод результата
        result = cur.execute("SELECT * FROM NormMode").fetchall()
        for ri, r in enumerate(result):
            t.setRowCount(t.rowCount() + 1)
            for ci, c in enumerate(r):
                t.setItem(ri, ci, QTableWidgetItem(c))


class HardTab(QWidget):
    def __init__(self):
        super(HardTab, self).__init__()
        t = QTableWidget(self)
        t.setGeometry(0, 0, 500, 500)
        t.setColumnCount(3)
        con = sqlite3.connect("record sheet.db")
        cur = con.cursor()
        #установка заголовков
        headers = con.execute("""PRAGMA table_info(HardMode)""")
        headers = [i[1] for i in headers]
        t.setHorizontalHeaderLabels(headers)
        # вывод результата
        result = cur.execute("SELECT * FROM HardMode").fetchall()
        for ri, r in enumerate(result):
            t.setRowCount(t.rowCount() + 1)
            for ci, c in enumerate(r):
                t.setItem(ri, ci, QTableWidgetItem(c))


app = QApplication(sys.argv)
ex = Sudoku()
ex.show()
sys.exit(app.exec_())
