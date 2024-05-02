
from PySide6.QtUiTools import QUiLoader


class SaveSocketPopup():

    instance = None  # 위젯

    def __init__(self,filePath, parent=None):
        self.instance = QUiLoader().load(filePath, None)
        self.instance.setWindowTitle('소켓 추가')
        # self.instance.show()


