from enum import Enum

class CommandTypes(Enum):
    Draw=0
    Edit=1

class CommandEnums(Enum):
    Line = 0,CommandTypes.Draw
    CircleCenterPoint = 2,CommandTypes.Draw
    CircleTwoPoint = 1,CommandTypes.Draw
    CircleCenterRadius = 3,CommandTypes.Draw
    CircleTreePoint = 4,CommandTypes.Draw
    Rectangle = 5,CommandTypes.Draw
    ArcThreePoint = 6,CommandTypes.Draw
    Polyline = 7,CommandTypes.Draw
    Move = 8,CommandTypes.Edit
    Copy = 9,CommandTypes.Edit
    Ellipse=10,CommandTypes.Draw
    ArcCenterTwoPoint = 11,CommandTypes.Draw
    Rotate=12,CommandTypes.Edit
    Scale=13,CommandTypes.Edit
    Mirror=14,CommandTypes.Edit



