from Helpers.Pen import CreatePen

class Setting:

    #Move
    movePen = CreatePen.createPen(150, 150, 150, 1, 1)

    #crooss
    croosPen = CreatePen.createPen(255, 255, 255, 1, 1)

    # pixelSize info
    pixelSize: float=1
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

    lineWidth:bool=False

    # Snap Setting
    snapSize = 5
    snapSizeSetting = 8

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

    elementInfo=False
    commandLine=False

    radius:float=50


    # Snap Degree Setting
    snapDegreePen = CreatePen.createPen(74, 128, 77, 1, 1)

    # Select Setting
    selectLeftPen = CreatePen.createPen(174, 216, 225, 1, 1)
    selectLeftHatch = CreatePen.createHatch(174, 216, 225, 1,alpha=0.3)

    selectRightPen = CreatePen.createPen(74, 128, 77, 1, 1)
    selectRightHatch = CreatePen.createHatch(74,128,77, 1,alpha=0.3)

    # Preview Line Setting
    previewLinePen = CreatePen.createPen(211, 0, 0, 1, 1)
    previewSquareHatch = CreatePen.createHatch(74, 128, 77, 1)

    # Grid Setting
    gridPenThickness=0.3
    XYPenThickness=0.4
    gridPen = CreatePen.createPen(153, 153, 153, gridPenThickness, 1)
    gridHatch = CreatePen.createHatch(0, 0, 0, 1)
    XYAxlePen = CreatePen.createPen(255, 127, 0, XYPenThickness, 1)


    #Zoom

    zoom:float=1.15


    @staticmethod
    def refreshValues():
        Setting.gridPenThickness = Setting.pixelSize * 0.3
        Setting.XYPenThickness = Setting.pixelSize * 0.7
        Setting.lineBoundDistance = Setting.pixelSize * Setting.lineBoundDistanceSetting
        Setting.handleSize = Setting.pixelSize * Setting.handleSizeSetting
        Setting.handlePen = CreatePen.createPen(99, 184, 255, Setting.pixelSize, 1)
        Setting.handleSelectedPen = CreatePen.createPen(153, 153, 153, Setting.pixelSize, 1)
        Setting.snapSize = Setting.pixelSize * Setting.snapSizeSetting
        Setting.lineSelectedPen = CreatePen.createPen(99, 184, 255, Setting.pixelSize, 1)
        Setting.previewLinePen = CreatePen.createPen(211, 0, 0, Setting.pixelSize, 1)

        Setting.movePen = CreatePen.createPen(150, 150, 150, Setting.pixelSize, 1)
        Setting.gridPen=CreatePen.createPen(153, 153, 153,Setting.gridPenThickness, 1)
        Setting.XYAxlePen = CreatePen.createPen(255, 127, 0, Setting.XYPenThickness, 1)
        Setting.croosPen = CreatePen.createPen(255, 255, 255, Setting.pixelSize, 1)
        Setting.selectLeftPen = CreatePen.createPen(174, 216, 225, Setting.pixelSize, 1)
        Setting.selectRightPen = CreatePen.createPen(74, 128, 77, Setting.pixelSize, 1)
        Setting.snapPen = CreatePen.createPen(211, 0, 0, Setting.pixelSize, 1)