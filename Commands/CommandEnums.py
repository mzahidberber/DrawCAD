from enum import Enum


class CommandEnums(Enum):
    line = 0
    circleTwoPoint = 1
    circleCenterPoint = 2
    circleCenterRadius = 3
    circleTreePoint = 4
    rectangle = 5
    arcThreePoint = 6
    spline = 7
    move = 8
    copy = 9
    ellipse=10
    arcCenterTwoPoint = 11



class CommandTypes(Enum):
    line=0
    circle=1
    rectangle=2
    arc=3
    ellips=4
    spline=5

getType={
    CommandEnums.line:CommandTypes.line,
    CommandEnums.circleTwoPoint:CommandTypes.circle,
    CommandEnums.circleCenterPoint:CommandTypes.circle,
    CommandEnums.circleCenterRadius:CommandTypes.circle,
    CommandEnums.circleTreePoint:CommandTypes.circle,
    CommandEnums.rectangle:CommandTypes.rectangle,
    CommandEnums.arcThreePoint:CommandTypes.arc,
    CommandEnums.spline:CommandTypes.spline
    }