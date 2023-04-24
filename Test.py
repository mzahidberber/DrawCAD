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
        PInfo.id.value: 1,
        PInfo.x.value: 20,
        PInfo.y.value: 20,
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
        EInfo.id.value: 1,
        EInfo.penId.value: 1,
        EInfo.typeId.value: 1,
        EInfo.layerId.value: 1,
        EInfo.ssAngles.value: None,
        EInfo.radiuses.value: None,
        EInfo.points.value: [
            {
                PInfo.id.value: 1,
                PInfo.x.value: 20,
                PInfo.y.value: 20,
                PInfo.elementId.value: 1,
                PInfo.pointTypeId.value: 1,
            },
            {
                PInfo.id.value: 2,
                PInfo.x.value: 30,
                PInfo.y.value: 30,
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
print(element.points[1].x)
