import vtk

class MyInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, resliceCursor: vtk.vtkResliceCursor) -> None:
        # self.AddObserver("MouseWheelForwardEvent", self.__mouseWheelForwardEventHandle)
        self.resliceCursor = resliceCursor

    def __mouseWheelForwardEventHandle(self, obj, event: str) -> None:
        print(self.resliceCursor.GetCenter())

def callback(obj, event) -> None:
    print("callback")
    return

def main(path_to_dir: str) -> None:
    # Init
    reader = vtk.vtkDICOMImageReader()
    # Reslice cursor generating the 3 slice planes
    resliceCursor = vtk.vtkResliceCursor()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1000, 500)
    renderWindow.SetWindowName("MPR")
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    style = vtk.vtkInteractorStyleImage()
    # style = MyInteractorStyle()
    renderWindowInteractor.SetInteractorStyle(style)
    picker = vtk.vtkCellPicker()
    picker.SetTolerance(0.005)
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.SetPicker(picker)
    renderWindowInteractor.GetPickingManager().SetEnabled(1)
    renderWindowInteractor.GetPickingManager().AddPicker(picker)
    renderWindowInteractor.Initialize()

    reader.SetDirectoryName(path_to_dir)
    reader.Update()
    imageData = reader.GetOutput()
    scalarRange = imageData.GetScalarRange()
    center = imageData.GetCenter()

    resliceCursor.SetCenter(center)
    resliceCursor.SetThickMode(1)
    resliceCursor.SetThickness(0, 0, 0)
    resliceCursor.SetImage(imageData)
    # Build the polydata
    resliceCursor.Update()

    resliceCursorWidgets = []
    resliceCursorThickLineRepresentations = []
    xmins = [0.0, 0.5, 0.5]
    ymins = [0.0, 0.0, 0.5]
    xmaxs = [0.5, 1.0, 1.0]
    ymaxs = [1.0, 0.5, 1.0]

    for i in range(3):
        # One renderer for each slice orientation
        renderer = vtk.vtkRenderer()
        renderWindow.AddRenderer(renderer)
        renderer.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])

        resliceCursorWidget = vtk.vtkResliceCursorWidget()
        resliceCursorWidgets.append(resliceCursorWidget)
        resliceCursorWidget.SetInteractor(renderWindowInteractor)

        resliceCursorThickLineRepresentation = vtk.vtkResliceCursorThickLineRepresentation()
        resliceCursorThickLineRepresentations.append(resliceCursorThickLineRepresentation)

        # vtkResliceCursorActor(): A reslice cursor consists of a pair of lines (cross hairs), 
        # thin or thick, that may be interactively manipulated for thin/thick reformats through 
        # the data
        resliceCursorActor = resliceCursorThickLineRepresentation.GetResliceCursorActor()
        centerlineProperty = resliceCursorActor.GetCenterlineProperty(0) # // x
        centerlineProperty.SetLineWidth(1)
        centerlineProperty.SetColor([0, 1, 0]) # green
        centerlineProperty.SetRepresentationToWireframe()
        thickSlabProperty = resliceCursorActor.GetThickSlabProperty(0)
        thickSlabProperty.SetColor([0, 1, 0]) # green
        thickSlabProperty.SetRepresentationToWireframe()

        centerlineProperty = resliceCursorActor.GetCenterlineProperty(1) # // y
        centerlineProperty.SetLineWidth(1)
        centerlineProperty.SetColor([0, 0, 1]) # blue
        centerlineProperty.SetRepresentationToWireframe()
        thickSlabProperty = resliceCursorActor.GetThickSlabProperty(1)
        thickSlabProperty.SetColor([0, 0, 1]) # blue
        thickSlabProperty.SetRepresentationToWireframe()

        centerlineProperty = resliceCursorActor.GetCenterlineProperty(2) # // z
        centerlineProperty.SetLineWidth(1)
        centerlineProperty.SetColor([1, 0, 0]) # red
        centerlineProperty.SetRepresentationToWireframe()
        thickSlabProperty = resliceCursorActor.GetThickSlabProperty(2)
        thickSlabProperty.SetColor([1, 0, 0]) # red
        thickSlabProperty.SetRepresentationToWireframe()

        # vtkResliceCursorPolyDataAlgorithm: generates a 2D reslice cursor vtkPolyData
        resliceCursorPolyDataAlgorithm = resliceCursorActor.GetCursorAlgorithm()
        resliceCursorPolyDataAlgorithm.SetResliceCursor(resliceCursor)
        cameraPosition = [0, 0, 0]
        if i == 0: # Axial plane
            resliceCursorPolyDataAlgorithm.SetReslicePlaneNormalToZAxis()
            cameraPosition[2] = 1
            viewUp = [0, 1, 0]
        elif i == 1: # Coronal plane
            resliceCursorPolyDataAlgorithm.SetReslicePlaneNormalToYAxis()
            cameraPosition[1] = 1
            viewUp = [0, 0, -1]
        else: # Sagittal plane
            resliceCursorPolyDataAlgorithm.SetReslicePlaneNormalToXAxis()
            cameraPosition[0] = 1
            viewUp = [0, 0, -1]

        # Specify an instance of vtkWidgetRepresentation used to represent this widget in the scene
        resliceCursorWidget.SetRepresentation(resliceCursorThickLineRepresentation)
        resliceCursorWidget.SetDefaultRenderer(renderer)
        resliceCursorWidget.SetEnabled(1)
        # resliceCursorWidget.AddObserver("InteractionEvent", callback)

        # Setting right camera orientation
        renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
        renderer.GetActiveCamera().SetPosition(cameraPosition)
        renderer.GetActiveCamera().ParallelProjectionOn()
        renderer.GetActiveCamera().SetViewUp(viewUp)
        renderer.ResetCamera()

        resliceCursorThickLineRepresentation.SetWindowLevel(scalarRange[1] - scalarRange[0], (scalarRange[0] + scalarRange[1]) / 2.0)
        resliceCursorThickLineRepresentation.SetLookupTable(resliceCursorThickLineRepresentations[0].GetLookupTable())

        resliceCursorWidget.On()

    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    path_to_dir = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    main(path_to_dir)
