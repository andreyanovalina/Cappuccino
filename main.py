import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow
from PyQt5.QtWidgets import QInputDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.open_second_form)
        self.con = sqlite3.connect("_coffee.db")

    def run(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM cappuccino").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'title_ofvariety', 'degree_of_roasting',
                                                    'type', 'description_of_taste', 'price', 'volume_of_packaging'])
        i = 0  # Используется для обозначения координаты ячейки при занесении значений
        for elem in result:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j in range(7):  # Кол-во столбцов: 4
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem[j])))
            i += 1
        self.tableWidget.resizeColumnsToContents()
        self.con.commit()

    def open_second_form(self):
        self.second_form = SecondForm()
        self.second_form.show()


class SecondForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.con = sqlite3.connect("_coffee.db")

    def add(self):
        cur = self.con.cursor()
        title_of_variety, ok_tv_Pressed = QInputDialog.getText(self, "Название сорта",
                                                               "Введите название сорта:")
        if ok_tv_Pressed:
            degree_of_roasting, ok_dr_Pressed = QInputDialog.getText(self, "Степень обжарки",
                                                                     "Введите степень обжарки:")
            if ok_dr_Pressed:
                type, ok_t_Pressed = QInputDialog.getItem(self, "Молотый/в зернах", "молотый - 1; в зернах - 2",
                                                          ("1", "2"), 0, False)
                if ok_t_Pressed:
                    description_of_taste, ok_dt_Pressed = QInputDialog.getText(self, "Описание вкуса",
                                                                               "Введите описание вкуса:")
                    if ok_dt_Pressed:
                        price, ok_p_Pressed = QInputDialog.getText(self, "Цена",
                                                                   "Введите цену:")
                        if ok_p_Pressed:
                            volume_of_packaging, ok_vp_Pressed = QInputDialog.getText(self, "Объем упаковки",
                                                                                      "Введите объем упаковки:")
                            if ok_vp_Pressed:
                                cur.execute(
                                    "INSERT INTO cappuccino(title_of_variety, degree_of_roasting, type,"
                                    "description_of_taste, price, volume_of_packaging) VALUES(?, ?, ?, ?, ?, ?)",
                                    (title_of_variety, degree_of_roasting, int(type), description_of_taste, price,
                                     volume_of_packaging))
                                self.con.commit()

    def edit(self):
        cur = self.con.cursor()
        id_for_coffee, okBtn_idPressed = QInputDialog.getText(self, "id записи",
                                                              "Введите id записи:")
        if okBtn_idPressed:
            title_of_variety, ok_tv_Pressed = QInputDialog.getText(self, "Название сорта",
                                                                   "Введите название сорта:")
            if ok_tv_Pressed:
                degree_of_roasting, ok_dr_Pressed = QInputDialog.getText(self, "Степень обжарки",
                                                                         "Введите степень обжарки:")
                if ok_dr_Pressed:
                    type, ok_t_Pressed = QInputDialog.getItem(self, "Молотый/в зернах", "молотый - 1; в зернах - 2",
                                                              ("1", "2"), 0, False)
                    if ok_t_Pressed:
                        description_of_taste, ok_dt_Pressed = QInputDialog.getText(self, "Описание вкуса",
                                                                                   "Введите описание вкуса:")
                        if ok_dt_Pressed:
                            price, ok_p_Pressed = QInputDialog.getText(self, "Цена",
                                                                       "Введите цену:")
                            if ok_p_Pressed:
                                volume_of_packaging, ok_vp_Pressed = QInputDialog.getText(self, "Объем упаковки",
                                                                                          "Введите объем упаковки:")
                                if ok_vp_Pressed:
                                    cur.execute(
                                        "UPDATE cappuccino SET title_of_variety = ?, degree_of_roasting = ?, type = ?,"
                                        "description_of_taste = ?, price = ?, volume_of_packaging = ? WHERE ID = ?",
                                        (title_of_variety, degree_of_roasting, type, description_of_taste, price,
                                         volume_of_packaging, id_for_coffee))
                                    self.con.commit()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
