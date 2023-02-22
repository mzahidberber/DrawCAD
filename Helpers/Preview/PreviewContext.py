from Helpers.Preview.BasePreview import BasePreview
from Helpers.Preview.LinePreview import LinePreview
from Helpers.Preview.CirclePreview import CirclePreview
from Helpers.Preview.RectanglePreview import RectanglePreview
from Helpers.Preview.ArcPreview import ArcPreview
from Helpers.Preview.EllipsPreview import EllipsPreview
from Helpers.Preview.SplinePreview import SplinePreview


class PreviewContext:
    __preview: BasePreview
    __preivewTypes: dict = {
        0: LinePreview,
        1: CirclePreview,
        2: RectanglePreview,
        3: ArcPreview,
        4: EllipsPreview,
        5: SplinePreview,
    }

    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(PreviewContext, self).__new__(self)
        return self.instance

    def setPreviewBuilder(self, previewType: int) -> BasePreview:
        self.__preview = self.__preivewTypes[previewType]
        return self.__preview()
