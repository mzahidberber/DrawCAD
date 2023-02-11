from Model import Element,EInfo,PInfo,RInfo
from Commands.ElementDraw import ElementDraw
def drawTest(scene):
        line=Element({
            EInfo.elementId.value:1,
            EInfo.penId.value:1,
            EInfo.elementTypeId.value:1,
            EInfo.layerId.value:1,
            EInfo.ssAngles.value:None,
            EInfo.radiuses.value:None,
            EInfo.points.value:[{
                PInfo.pointId.value:1,
                PInfo.pointX.value:20,
                PInfo.pointY.value:20,
                PInfo.elementId.value:1,
                PInfo.pointTypeId.value:1},{
                PInfo.pointId.value:2,
                PInfo.pointX.value:30,
                PInfo.pointY.value:30,
                PInfo.elementId.value:1,
                PInfo.pointTypeId.value:1}],
            EInfo.handles.value:None
        })
        circle=Element({
            EInfo.elementId.value:2,
            EInfo.penId.value:1,
            EInfo.elementTypeId.value:2,
            EInfo.layerId.value:1,
            EInfo.ssAngles.value:None,
            EInfo.radiuses.value:[{
                RInfo.radiusId.value:1,
                RInfo.radiusValue.value:10,
                RInfo.radiusElementId.value:1}],
            EInfo.points.value:[{
                PInfo.pointId.value:1,
                PInfo.pointX.value:20,
                PInfo.pointY.value:20,
                PInfo.elementId.value:1,
                PInfo.pointTypeId.value:1},{
                PInfo.pointId.value:2,
                PInfo.pointX.value:30,
                PInfo.pointY.value:30,
                PInfo.elementId.value:1,
                PInfo.pointTypeId.value:1}],
            EInfo.handles.value:None
        })
        # ElementDraw(scene).drawElement(line)
        # ElementDraw(scene).drawElement(circle)
