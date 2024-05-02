
from PySide6.QtUiTools import QUiLoader
from src.component.settings.SaveSocketPopup import SaveSocketPopup
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Settings():
    instance = None

    saveSkWindow = None
    def __init__(self):

        print(resource_path('views/settings.ui'))

        self.instance = QUiLoader().load(resource_path('views/settings.ui'), None)
        self.instance.setWindowTitle('설정')

        self.saveSkWindow = SaveSocketPopup(resource_path('views/settings-saveSocket.ui'))
        self.saveSkWindow.instance.setWindowTitle('추가')
        self.saveSkWindow.instance.show()
