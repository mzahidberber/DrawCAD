from enum import Enum


class CommandEnums(Enum):
    Line = 0
    CircleTwoPoint = 1
    CircleCenterPoint = 2
    CircleCenterRadius = 3
    CircleTreePoint = 4
    Rectangle = 5
    ArcThreePoint = 6
    Polyline = 7
    Move = 8
    Copy = 9
    Ellipse=10
    ArcCenterTwoPoint = 11



class CommandTypes(Enum):
    line=0
    circle=1
    rectangle=2
    arc=3
    ellips=4
    spline=5

getType={
    CommandEnums.Line:CommandTypes.line,
    CommandEnums.CircleTwoPoint:CommandTypes.circle,
    CommandEnums.CircleCenterPoint:CommandTypes.circle,
    CommandEnums.CircleCenterRadius:CommandTypes.circle,
    CommandEnums.CircleTreePoint:CommandTypes.circle,
    CommandEnums.Rectangle:CommandTypes.rectangle,
    CommandEnums.ArcThreePoint:CommandTypes.arc,
    CommandEnums.Polyline:CommandTypes.spline
    }