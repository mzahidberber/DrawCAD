from Helpers.Preview.BasePreview import BasePreview
from Helpers.Preview.LinePreview import LinePreview
from Helpers.Preview.RectanglePreview import RectanglePreview
from Helpers.Preview.ArcThreePointPreview import ArcThreePointPreview
from Helpers.Preview.EllipsPreview import EllipsPreview
from Helpers.Preview.SplinePreview import SplinePreview
from Helpers.Preview.CircleTwoPointPreview import CircleTwoPointPreview
from Helpers.Preview.CircleCenterPointPreview import CircleCenterPointPreview
from Helpers.Preview.CircleCenterRadiusPreview import CircleCenterRadiusPreview
from Helpers.Preview.CircleTreePointPreivew import CircleTreePointPreivew
from Helpers.Preview.DefaultPreview import DefaultPreview
from Helpers.Preview.ArcCenterTwoPointPreview import ArcCenterTwoPointPreview
from Helpers.Preview.MovePreview import MovePreview
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle


class PreviewContext:
    __preview: BasePreview
    __preivewTypes: dict = {
        0: LinePreview,
        1: CircleTwoPointPreview,
        2: CircleCenterPointPreview,
        3: CircleCenterRadiusPreview,
        4: CircleTreePointPreivew,
        5: RectanglePreview,
        6: ArcThreePointPreview,
        7: SplinePreview,
        8: MovePreview,
        10: EllipsPreview,
        11: ArcCenterTwoPointPreview
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PreviewContext, cls).__new__(cls)
        return cls.instance

    def setPreviewBuilder(self, previewType: int) -> BasePreview:
        self.__preview = self.__preivewTypes[previewType]
        return self.__preview()
    
    
    def setDefaultPreview(self):return DefaultPreview()
