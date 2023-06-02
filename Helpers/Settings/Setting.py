from Helpers.Pen import CreatePen

class Setting:
    # pixelSize info
    pixelSize: float
    # Handle Setting
    handlePen = CreatePen.createPen(99, 184, 255, 1, 1)
    handleHatch = CreatePen.createHatch(153, 153, 153, 1)

    handleSelectedPen = CreatePen.createPen(153, 153, 153, 1, 1)
    handleSelectedHatch = CreatePen.createHatch(255, 127, 0, 1)

    handleSize = 1
    handleSizeSetting = 10

    # Line Setting
    lineSelectedPen = CreatePen.createPen(99, 184, 255, 1, 1)

    lineBoundDistance = 5
    lineBoundDistanceSetting = 10

    # Snap Setting
    snapSize = 4
    snapSizeSetting = 7

    snapLineBoundDistance=0.1

    snapPen = CreatePen.createPen(211, 0, 0, 2, 1)

    snapEnd=False
    snapMiddle=False
    snapCenter=False
    snapGrid=False
    snapNearest=False
    snapIntersection=False

    orthoMode=False
    polarMode=False

    snapAngle:float=30

    gridDistance:float=10


    # Snap Degree Setting
    snapDegreePen = CreatePen.createPen(74, 128, 77, 1, 1)

    # Preview Line Setting
    previewLinePen = CreatePen.createPen(211, 0, 0, 1, 1)
    previewSquareHatch = CreatePen.createHatch(74, 128, 77, 1)

    # Grid Setting
    gridPen = CreatePen.createPen(153, 153, 153, 0.5, 1)
    gridHatch = CreatePen.createHatch(0, 0, 0, 1)
    XYAxlePen = CreatePen.createPen(255, 127, 0, 0.5, 1)
