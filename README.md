# pyqt-custom-frameless-mainwindow
PyQt Custom Frameless Main Window (Enable to move and resize). I made this because i want to make system-independent frameless window. That is quite a chore to accomplish only by me.

## Requirements
PyQt5 >= 5.8

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-frameless-mainwindow.git --upgrade```

## Example
Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_custom_frameless_mainwindow import CustomFramelessMainWindow


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    example = CustomFramelessMainWindow()
    example.show()
    app.exec_()
```

## See also
If you want to see more system-friendly(or system-dependent) and well-functioning one, check below.
<a href="https://github.com/yjg30737/pyqt-custom-titlebar-window.git">pyqt-custom-titlebar-window</a>



