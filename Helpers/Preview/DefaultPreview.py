from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF


class DefaultPreview(BasePreview):
    def boundaryBuild(self):return QRectF()
    def paintPreview(self, painter):pass