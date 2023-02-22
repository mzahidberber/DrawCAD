from enum import Enum


class ETypesClass(Enum):
    "ElementTypes"
    line = "Line"
    circle = "Circle"


# print(ETypesClass.)
from Model.Point import Point
from Model.DrawEnums import PInfo

point = Point(
    {
        PInfo.pointId.value: 1,
        PInfo.pointX.value: 20,
        PInfo.pointY.value: 20,
        PInfo.elementId.value: 1,
        PInfo.pointTypeId.value: 1,
    }
)
# a.pointX=30
# print(point.pointX)
# print(point.mapDict())

from Model.Element import Element
from Model.DrawEnums import EInfo

element = Element(
    {
        EInfo.elementId.value: 1,
        EInfo.penId.value: 1,
        EInfo.elementTypeId.value: 1,
        EInfo.layerId.value: 1,
        EInfo.ssAngles.value: None,
        EInfo.radiuses.value: None,
        EInfo.points.value: [
            {
                PInfo.pointId.value: 1,
                PInfo.pointX.value: 20,
                PInfo.pointY.value: 20,
                PInfo.elementId.value: 1,
                PInfo.pointTypeId.value: 1,
            },
            {
                PInfo.pointId.value: 2,
                PInfo.pointX.value: 30,
                PInfo.pointY.value: 30,
                PInfo.elementId.value: 1,
                PInfo.pointTypeId.value: 1,
            },
        ],
        EInfo.handles.value: None,
    }
)
print(element.to_dict())
for i in element.points:
    print(i.to_dict())
print(element.points[1].pointX)
