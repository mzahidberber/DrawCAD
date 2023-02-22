from Helpers.Preview.BasePreview import BasePreview
from Helpers.Preview.LinePreview import LinePreview
from Helpers.Preview.RectanglePreview import RectanglePreview
from Helpers.Preview.ArcPreview import ArcPreview
from Helpers.Preview.EllipsPreview import EllipsPreview
from Helpers.Preview.SplinePreview import SplinePreview
from Helpers.Preview.CircleTwoPointPreview import CircleTwoPointPreview
from Helpers.Preview.CircleCenterPointPreview import CircleCenterPointPreview
from Helpers.Preview.CircleCenterRadiusPreview import CircleCenterRadiusPreview
from Helpers.Preview.CircleTreePointPreivew import CircleTreePointPreivew
from Helpers.Preview.DefaultPreview import DefaultPreview



class PreviewContext:
    __preview: BasePreview
    __preivewTypes: dict = {
        0: LinePreview,
        1: CircleTwoPointPreview,
        2: CircleCenterPointPreview,
        3: CircleCenterRadiusPreview,
        4: CircleTreePointPreivew,
        5: RectanglePreview,
        6: ArcPreview,
        7: SplinePreview,
        8: EllipsPreview
    }

    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(PreviewContext, self).__new__(self)
        return self.instance

    def setPreviewBuilder(self, previewType: int) -> BasePreview:
        self.__preview = self.__preivewTypes[previewType]
        return self.__preview()
    
    
    def setDefaultPreview(self):return DefaultPreview()
