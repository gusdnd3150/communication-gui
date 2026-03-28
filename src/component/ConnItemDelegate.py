from PySide6.QtCore import Signal, QRect, QModelIndex, Qt, QEvent
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class ConnItemDelegate(QStyledItemDelegate):
    button_clicked = Signal(QModelIndex)

    BTN_WIDTH = 24
    BTN_MARGIN = 4

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        # 자식 항목은 버튼 없이 기본 렌더링
        if index.parent().isValid():
            super().paint(painter, option, index)
            return

        # 텍스트 영역을 버튼 폭만큼 줄여서 그림
        text_option = QStyleOptionViewItem(option)
        text_option.rect = option.rect.adjusted(0, 0, -(self.BTN_WIDTH + self.BTN_MARGIN * 2), 0)
        super().paint(painter, text_option, index)

        # 버튼 그리기
        btn_rect = self._btn_rect(option.rect)
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("#888"), 1))
        painter.setBrush(QBrush(QColor("#ddd")))
        painter.drawRoundedRect(btn_rect, 3, 3)
        painter.setPen(QPen(QColor("#333")))
        painter.drawText(btn_rect, Qt.AlignCenter, "✕")
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if index.parent().isValid():
            return False
        if event.type() == QEvent.MouseButtonRelease:
            if self._btn_rect(option.rect).contains(event.position().toPoint()):
                self.button_clicked.emit(index)
                return True
        return super().editorEvent(event, model, option, index)

    def _btn_rect(self, item_rect: QRect) -> QRect:
        return QRect(
            item_rect.right() - self.BTN_WIDTH - self.BTN_MARGIN,
            item_rect.top() + 2,
            self.BTN_WIDTH,
            item_rect.height() - 4,
        )