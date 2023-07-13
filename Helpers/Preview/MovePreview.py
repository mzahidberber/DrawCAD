from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
class MovePreview(BasePreview):
    def paintPreview(self, painter: QPainter) -> None:pass
        # if self._editManyElements is not None:
        #     for i in self._editManyElements:
        #         print(i)

    def boundaryBuild(self) -> QRectF:
        return QRectF()