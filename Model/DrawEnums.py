from enum import Enum


class ETypes(Enum):
    "ElementTypes"
    line = 0
    circle = 1
    rectangle = 3
    arc = 4
    ellips = 5
    spline = 6


class DBInfo(Enum):
    "DrawBoxInformation"
    drawBoxId = "drawBoxId"
    drawName = "drawName"
    userId = "userId"
    layers = "layers"


class LInfo(Enum):
    "LayerInformation"
    layerId = "layerId"
    layerName = "layerName"
    layerLock = "layerLock"
    LayerVisibility = "layerVisibility"
    LayerThickness = "layerThickness"
    DrawBoxId = "drawBoxId"
    PenId = "penId"
    Pen = "pen"
    elements = "elements"


class EInfo(Enum):
    "ElementInformation"
    elementId = "elementId"
    penId = "penId"
    elementTypeId = "elementTypeId"
    layerId = "layerId"
    layer = "layer"
    ssAngles = "ssangles"
    radiuses = "radiuses"
    points = "points"


class PInfo(Enum):
    "PointInformation"
    pointId = "pointId"
    pointX = "pointX"
    pointY = "pointY"
    elementId = "elementId"
    pointTypeId = "pointTypeId"


class RInfo(Enum):
    "RadiusInformation"
    radiusId = "radiusId"
    radiusValue = "radiusValue"
    radiusElementId = "radiusElementId"


class HInfo(Enum):
    "HandleInformation"
    handleId = "handleId"
    handleElementId = "handleElementId"
    handleTypeId = "handleTypeId"


class SSAInfo(Enum):
    "SSAngleInformation"
    ssangleId = "ssAngleId"
    ssangleType = "ssAngleType"
    ssangleValue = "ssAngleValue"
    ssangleElementId = "ssAngleElementId"


class PenInfo(Enum):
    "Pen Information"
    penId = "penId"
    penName = "penName"
    # penColorId = "penColorId"
    # penColor = "penColor"
    penRed="penRed"
    penBlue="penBlue"
    penGreen="penGreen"
    penStyleId = "penStyleId"
    penStyle = "penStyle"


class CInfo(Enum):
    "ColorInformation"
    colorId = "colorId"
    colorName = "colorName"
    colorRed = "colorRed"
    colorBlue = "colorBlue"
    colorGreen = "colorGreen"


class PSInfo(Enum):
    "PenStyleInformation"
    penStyleId = "penStyleId"
    penStyleName = "penStyleName"


class UInfo(Enum):
    "UserInformation"
    userId = "userId"
    userName = "userName"
    userPassword = "userPassword"
