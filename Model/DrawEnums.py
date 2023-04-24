from enum import Enum


class StateTypes(Enum):
    "ModelStateTypes"
    added="added"
    update="update"
    delete="delete"
    unchanged="unchange"
    detached="detached"



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
    id = "id"
    dname = "name"
    userId = "userId"
    layers = "layers"


class LInfo(Enum):
    "LayerInformation"
    id = "id"
    lname = "name"
    lock = "lock"
    visibility = "visibility"
    thickness = "thickness"
    drawBoxId = "drawBoxId"
    penId = "penId"
    pen = "pen"
    elements = "elements"


class EInfo(Enum):
    "ElementInformation"
    id = "id"
    penId = "penId"
    typeId = "typeId"
    layerId = "layerId"
    layer = "layer"
    ssAngles = "ssangles"
    radiuses = "radiuses"
    points = "points"


class PInfo(Enum):
    "PointInformation"
    id = "id"
    x = "x"
    y = "y"
    elementId = "elementId"
    pointTypeId = "pointTypeId"


class RInfo(Enum):
    "RadiusInformation"
    id = "id"
    rvalue = "value"
    elementId = "elementId"


class HInfo(Enum):
    "HandleInformation"
    id = "id"
    elementId = "elementId"
    handleTypeId = "typeId"


class SSAInfo(Enum):
    "SSAngleInformation"
    id = "id"
    type = "type"
    ssvalue = "value"
    elementId = "elementId"




class PenInfo(Enum):
    "Pen Information"
    id = "id"
    pname = "name"
    # penColorId = "penColorId"
    # penColor = "penColor"
    red="red"
    blue="blue"
    green="green"
    penStyleId = "penStyleId"
    penStyle = "penStyle"


class CInfo(Enum):
    "ColorInformation"
    id = "id"
    cname = "name"
    red = "red"
    blue = "blue"
    green = "green"


class PSInfo(Enum):
    "PenStyleInformation"
    id = "id"
    psname = "name"


class UInfo(Enum):
    "UserInformation"
    userId = "userId"
    userName = "userName"
    userPassword = "userPassword"
