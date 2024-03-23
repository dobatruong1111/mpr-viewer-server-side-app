import vtk

def main() -> None:
    # Reslice cursor callback
    def resliceCursorCallback(obj, event) -> None:
        for i in range(0, 3):
            ps = planeWidgetArray[i].GetPolyDataAlgorithm()
            origin = resliceCursorWidgetArray[i].GetResliceCursorRepresentation().GetPlaneSource().GetOrigin()
            ps.SetOrigin(origin)
            point1 = resliceCursorWidgetArray[i].GetResliceCursorRepresentation().GetPlaneSource().GetPoint1()
            ps.SetPoint1(point1)
            point2 = resliceCursorWidgetArray[i].GetResliceCursorRepresentation().GetPlaneSource().GetPoint2()
            ps.SetPoint2(point2)
            planeWidgetArray[i].UpdatePlacement()

    path = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    reader = vtk.vtkDICOMImageReader()
    volumeMapper = vtk.vtkPolyDataMapper()
    volumeActor = vtk.vtkActor()
    renderWindow = vtk.vtkRenderWindow()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    picker = vtk.vtkCellPicker()

    renderWindow.SetSize(600, 600)
    renderWindow.SetWindowName("MPR Viewer")
    renderWindow.SetInteractor(renderWindowInteractor)
    picker.SetTolerance(0.005)
    # renderWindowInteractor.SetPicker(picker)
    # renderWindowInteractor.GetPickingManager().SetEnabled(1)
    # renderWindowInteractor.GetPickingManager().AddPicker(picker)
    # renderWindow.SetInteractor(renderWindowInteractor)
    # renderWindowInteractor.SetRenderWindow(renderWindow)

    # Reader
    reader.SetDirectoryName(path)
    reader.Update()
    imageData = reader.GetOutput()
    imageDims = imageData.GetDimensions()
    scalarRange = imageData.GetScalarRange()
    center = imageData.GetCenter()

    # Bounding box
    outline = vtk.vtkOutlineFilter()
    outlineMapper = vtk.vtkPolyDataMapper()
    outlineActor = vtk.vtkActor()

    outline.SetInputConnection(reader.GetOutputPort())
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(1, 1, 0)

    # Mapper and actors for volume
    volumeMapper.SetInputConnection(reader.GetOutputPort())
    volumeActor.SetMapper(volumeMapper)

    # Renderers
    rendererArray = [None]*4
    for i in range(4):
        rendererArray[i] = vtk.vtkRenderer()
        renderWindow.AddRenderer(rendererArray[i])
    renderWindow.SetMultiSamples(0)

    # Properties
    ipwProp = vtk.vtkProperty()

    # 3D plane widgets
    planeWidgetArray = [None]*3
    for i in range(3):
        planeWidgetArray[i] = vtk.vtkImagePlaneWidget()
        planeWidgetArray[i].SetInteractor(renderWindowInteractor)
        planeWidgetArray[i].SetPicker(picker)
        planeWidgetArray[i].RestrictPlaneToVolumeOn()
        color = [0, 0, 0]
        color[i] = 1
        planeWidgetArray[i].GetPlaneProperty().SetColor(color)
        planeWidgetArray[i].SetTexturePlaneProperty(ipwProp)
        planeWidgetArray[i].TextureInterpolateOff()
        planeWidgetArray[i].SetResliceInterpolateToLinear()
        planeWidgetArray[i].SetInputConnection(reader.GetOutputPort())
        planeWidgetArray[i].SetPlaneOrientation(i)
        planeWidgetArray[i].SetSliceIndex(int(imageDims[i] / 2))
        planeWidgetArray[i].DisplayTextOn()
        planeWidgetArray[i].SetDefaultRenderer(rendererArray[3])
        # planeWidgetArray[i].SetWindowLevel(scalarRange[1] - scalarRange[0], (scalarRange[0] + scalarRange[1]) / 2.0, 0)
        planeWidgetArray[i].On()
        planeWidgetArray[i].InteractionOff()

    planeWidgetArray[1].SetLookupTable(planeWidgetArray[0].GetLookupTable()) 
    planeWidgetArray[2].SetLookupTable(planeWidgetArray[0].GetLookupTable())

    # Reslice Cursor
    resliceCursor = vtk.vtkResliceCursor()
    resliceCursor.SetCenter(center[0], center[1], center[2])
    resliceCursor.SetThickMode(0)
    resliceCursor.SetThickness(10, 10, 10)
    resliceCursor.SetHole(1)
    resliceCursor.SetImage(imageData)

    # 2D Reslice cursor widgets
    resliceCursorWidgetArray = [None]*3
    resliceCursorRepArray = [None]*3
    viewUp = [[0, 0, -1], [0, 0, -1], [0, 1, 0]]
    for i in range(3):
        resliceCursorWidgetArray[i] = vtk.vtkResliceCursorWidget()
        resliceCursorRepArray[i] = vtk.vtkResliceCursorLineRepresentation()
        resliceCursorWidgetArray[i].SetInteractor(renderWindowInteractor)
        resliceCursorWidgetArray[i].SetRepresentation(resliceCursorRepArray[i])

        resliceCursorActor = resliceCursorRepArray[i].GetResliceCursorActor()
        resliceCursorActor.GetCursorAlgorithm().SetResliceCursor(resliceCursor)
        resliceCursorActor.GetCursorAlgorithm().SetReslicePlaneNormal(i)

        # reslice = resliceCursorRepArray[i].GetReslice()
        # reslice.SetInputConnection(reader.GetOutputPort())
        # reslice.SetBackgroundColor(scalarRange[0], scalarRange[0], scalarRange[0], scalarRange[0])
        # reslice.AutoCropOutputOn()
        # reslice.Update()

        centerlineProperty = resliceCursorActor.GetCenterlineProperty(0) # // x
        centerlineProperty.SetLineWidth(1)
        centerlineProperty.SetColor([1, 0, 0]) # red
        centerlineProperty.SetRepresentationToWireframe()
        thickSlabProperty = resliceCursorActor.GetThickSlabProperty(0)
        thickSlabProperty.SetColor([1, 0, 0]) # red
        thickSlabProperty.SetRepresentationToWireframe()
        centerlineProperty = resliceCursorActor.GetCenterlineProperty(1) # // y
        centerlineProperty.SetLineWidth(1)
        centerlineProperty.SetColor([0, 1, 0]) # green
        centerlineProperty.SetRepresentationToWireframe()
        thickSlabProperty = resliceCursorActor.GetThickSlabProperty(1)
        thickSlabProperty.SetColor([0, 1, 0]) # green
        thickSlabProperty.SetRepresentationToWireframe()
        centerlineProperty = resliceCursorActor.GetCenterlineProperty(2) # // z
        centerlineProperty.SetLineWidth(1)
        centerlineProperty.SetColor([0, 0, 1]) # blue
        centerlineProperty.SetRepresentationToWireframe()
        thickSlabProperty = resliceCursorActor.GetThickSlabProperty(2)
        thickSlabProperty.SetColor([0, 0, 1]) # blue
        thickSlabProperty.SetRepresentationToWireframe()

        resliceCursorWidgetArray[i].SetDefaultRenderer(rendererArray[i])
        resliceCursorWidgetArray[i].SetEnabled(True)

        # Setup camera
        camera = rendererArray[i].GetActiveCamera()
        camera.SetFocalPoint(0, 0, 0)
        camPos = [0, 0, 0]
        camPos[i] = 1
        camera.SetPosition(camPos[0], camPos[1], camPos[2])
        camera.ParallelProjectionOn()
        camera.SetViewUp(viewUp[i][0], viewUp[i][1], viewUp[i][2])
        rendererArray[i].ResetCamera()

        resliceCursorRepArray[i].SetWindowLevel(scalarRange[1] - scalarRange[0], (scalarRange[0] + scalarRange[1]) / 2.0, 0)
        resliceCursorRepArray[i].SetLookupTable(resliceCursorRepArray[0].GetLookupTable())
        
        planeWidgetArray[i].SetWindowLevel(scalarRange[1] - scalarRange[0], (scalarRange[0] + scalarRange[1]) / 2.0, 0)
        planeWidgetArray[i].GetColorMap().SetLookupTable(resliceCursorRepArray[0].GetLookupTable())

        resliceCursorWidgetArray[i].AddObserver('InteractionEvent', resliceCursorCallback)
        resliceCursorWidgetArray[i].On()

    rendererArray[0].SetBackground(0.3, 0.1, 0.1)
    rendererArray[0].SetViewport(0, 0, 0.5, 0.5)

    rendererArray[1].SetBackground(0.1, 0.3, 0.1)
    rendererArray[1].SetViewport(0.5, 0, 1, 0.5)

    rendererArray[2].SetBackground(0.1, 0.1, 0.3)
    rendererArray[2].SetViewport(0, 0.5, 0.5, 1)

    rendererArray[3].AddActor(volumeActor)
    rendererArray[3].AddActor(outlineActor)
    rendererArray[3].SetBackground(0.1, 0.1, 0.1)
    rendererArray[3].SetViewport(0.5, 0.5, 1, 1)
    rendererArray[3].GetActiveCamera().Elevation(110)
    rendererArray[3].GetActiveCamera().SetViewUp(0, 0, -1)
    rendererArray[3].GetActiveCamera().Azimuth(45)
    rendererArray[3].GetActiveCamera().Dolly(1.15)
    rendererArray[3].ResetCamera()

    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
