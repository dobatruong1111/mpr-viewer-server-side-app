import vtk

def main() -> None:
    # Test
    colors = vtk.vtkNamedColors()
    cone = vtk.vtkConeSource()
    mapper = vtk.vtkPolyDataMapper()
    property = vtk.vtkProperty()
    actor = vtk.vtkActor()

    cone.SetHeight(2.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)
    cone.SetDirection(1, 0, 0)

    mapper.SetInputConnection(cone.GetOutputPort())

    property.SetColor(colors.GetColor3d("Tomato"))

    actor.SetMapper(mapper)
    actor.SetProperty(property)

    def resliceCursorCallback(obj, event):
        print("Hello")

    path = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"

    # Init
    reader = vtk.vtkDICOMImageReader()
    resliceCursor = vtk.vtkResliceCursor()
    resliceCursorWidget = vtk.vtkResliceCursorWidget()
    resliceCursorRep = vtk.vtkResliceCursorLineRepresentation()
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()

    # Setup render window
    renderer.SetBackground(0.3, 0.1, 0.1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetMultiSamples(0)
    renderWindow.SetSize(600, 600)
    renderWindow.SetWindowName("MPR Viewer")
    renderWindow.SetInteractor(renderWindowInteractor)

    # Reader
    reader.SetDirectoryName(path)
    reader.Update()
    imageData = reader.GetOutput()
    scalarRange = imageData.GetScalarRange()
    center = imageData.GetCenter()

    actor.SetPosition(center)
    renderer.AddActor(actor)

    # Reslice cursor
    resliceCursor.SetCenter(center[0], center[1], center[2])
    resliceCursor.SetThickMode(0)
    resliceCursor.SetThickness(10, 10, 10)
    resliceCursor.SetHole(1)
    resliceCursor.SetImage(imageData)

    # 2D Reslice cursor widgets
    resliceCursorWidget.SetInteractor(renderWindowInteractor)
    resliceCursorWidget.SetRepresentation(resliceCursorRep)

    resliceCursorActor = resliceCursorRep.GetResliceCursorActor()
    resliceCursorActor.GetCursorAlgorithm().SetResliceCursor(resliceCursor)
    resliceCursorActor.GetCursorAlgorithm().SetReslicePlaneNormal(0)

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

    resliceCursorRep.SetWindowLevel(scalarRange[1] - scalarRange[0], (scalarRange[0] + scalarRange[1]) / 2.0, 0)

    resliceCursorWidget.SetDefaultRenderer(renderer)
    resliceCursorWidget.SetEnabled(True)

    # Setup camera
    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(0, 0, 0)
    camPos = [1, 0, 0]
    camera.SetPosition(camPos[0], camPos[1], camPos[2])
    camera.ParallelProjectionOn()
    viewUp = [0, 0, -1]
    camera.SetViewUp(viewUp[0], viewUp[1], viewUp[2])
    renderer.ResetCamera()
    
    resliceCursorWidget.AddObserver('InteractionEvent', resliceCursorCallback)
    resliceCursorWidget.On()
    
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
