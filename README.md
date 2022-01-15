# pyqt-custom-frameless-mainwindow
PyQt Custom Frameless Main Window (Enable to move and resize)

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
<a href="https://github.com/yjg30737/pyqt-system-specific-custom-frameless-widget.git">pyqt-system-specific-custom-frameless-widget</a>
