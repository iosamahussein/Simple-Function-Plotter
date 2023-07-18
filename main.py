# imort the necessary packages
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget,  QHBoxLayout,  QVBoxLayout, QLineEdit, QPushButton, QLabel
import matplotlib.pyplot as plt
import numpy as np

# function to evaluate the function for the most common functions


def evaluate_function(function, x):
    function = function.replace("sin", "np.sin")
    function = function.replace("cos", "np.cos")
    function = function.replace("tan", "np.tan")
    function = function.replace("exp", "np.exp")
    function = function.replace("ln", "np.log")
    function = function.replace("log", "np.log10")
    function = function.replace("sqrt", "np.sqrt")
    function = function.replace("^", "**")
    return eval(function)


# function to check if the input is a valid function
def is_function_valid(function):
    try:
        function = function.replace("^", "**")
        x = np.linspace(-10, 10, 100)
        y = evaluate_function(function, x)
        if (x.shape != y.shape):
            return False
        return True
    except:
        return False


class CustomInput(QWidget):

    def __init__(self, label_text, isnum=False, default_value="", parent=None):
        super(CustomInput, self).__init__(parent)
        self.isnum = isnum
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.label.font()
        font.setPointSize(15)
        self.label.setFont(font)
        self.input = QLineEdit()
        # set default value as a default value until the user changes it
        self.input.setText(default_value)
        font = self.input.font()
        font.setPointSize(12)
        self.input.setFont(font)
        self.error_message = QLabel("")
        self.error_message.setStyleSheet("color: red")
        font = self.error_message.font()
        font.setPointSize(10)
        self.error_message.setFont(font)
        self.error_message.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.error_message)
        self.setLayout(self.layout)
        self.input.textChanged.connect(self.check_input)

    def check_input(self, text):
        if self.input.text() == "":
            self.error_message.setText("Input is empty")
        elif (self.isnum and not self.input.text().isnumeric() and
              not (self.input.text()[0] == "-" and self.input.text()[1:].isnumeric())):
            self.error_message.setText("Input is not a number")
        elif (not self.isnum and not is_function_valid(self.input.text())):
            self.error_message.setText("Invalid function")
        else:
            self.error_message.setText("")

    def get_input(self):
        if (self.error_message.text() != ""):
            return ""
        return self.input.text()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Function Plotter")
        layout = QVBoxLayout()
        sub_layout = QHBoxLayout()
        self.function_input = CustomInput("Function", default_value="sin(x)")
        self.min_value_input = CustomInput(
            "Min value", True, default_value="-10")
        self.max_value_input = CustomInput(
            "Max value", True, default_value="10")
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFixedSize(70, 70)
        self.plot_button.setStyleSheet("background-color: #0077FF")
        self.plot_button.clicked.connect(self.on_plot_button_clicked)
        sub_layout.addWidget(self.function_input)
        sub_layout.addWidget(self.min_value_input)
        sub_layout.addWidget(self.max_value_input)
        sub_layout.addWidget(self.plot_button)
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumSize(500, 500)
        layout.addLayout(sub_layout)
        layout.addWidget(self.canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # to display the default plot when the window is opened
        self.on_plot_button_clicked()

    def on_plot_button_clicked(self):
        if (not self.function_input.get_input() or not self.min_value_input.get_input() or not self.max_value_input.get_input()):
            return
        min_value = float(self.min_value_input.get_input())
        max_value = float(self.max_value_input.get_input())
        if (min_value >= max_value):
            self.min_value_input.error_message.setText(
                "Min value must be less than max value")
            return
        self.min_value_input.error_message.setText("")
        function = self.function_input.get_input()
        x = np.linspace(min_value, max_value, 1000)
        y = evaluate_function(function, x)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
