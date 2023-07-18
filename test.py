import pytest
from PySide2.QtCore import Qt

from main import CustomInput, MainWindow


def test_function_input(qtbot):
    """Test the CustomInput class."""
    function_input = CustomInput("Function", default_value="")
    qtbot.addWidget(function_input)

    # Check that the input is empty.
    assert function_input.get_input() == ""

    # Enter a valid function.
    function_input.input.setText("cos(x)")
    assert function_input.get_input() == "cos(x)"

    # Enter an invalid function.
    function_input.input.setText("invalid_function")
    assert function_input.get_input() == ""

def test_min_value_input(qtbot):
    """Test the CustomInput class."""
    min_value_input = CustomInput("Min value", isnum=True, default_value="0")
    qtbot.addWidget(min_value_input)

    # Check that the input is correct.
    assert min_value_input.get_input() == "0"

    # Enter an invalid number.
    min_value_input.input.setText("invalid_number")
    assert min_value_input.get_input() == ""

def test_main_window(qtbot):
    """Test the MainWindow class."""
    window = MainWindow()
    qtbot.addWidget(window)

    # Check that the window title is correct.
    assert window.windowTitle() == "Function Plotter"

    # Check that the min value input is correct.
    assert window.min_value_input.get_input() == "-10"

    # Check that the max value input is correct.
    assert window.max_value_input.get_input() == "10"

    # Click the Plot button.
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)