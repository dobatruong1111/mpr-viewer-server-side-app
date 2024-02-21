import vtk

class MyInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self, mapper) -> None:
        # self.AddObserver("LeftButtonPressEvent", self.__leftButtonPressEventHandle)
        # self.AddObserver("LeftButtonReleaseEvent", self.__leftButtonReleaseEventHandle)
        self.AddObserver("MouseWheelForwardEvent", self.__mouseWheelForwardEventHandle)
        self.AddObserver("MouseWheelBackwardEvent", self.__mouseWheelBackwardEventHandle)
        # self.AddObserver("MouseMoveEvent", self.__mouseMoveEventHandle)
        # self.AddObserver("RightButtonPressEvent", self.__rightButtonPressEventHandle)
        # self.AddObserver("RightButtonReleaseEvent", self.__rightButtonReleaseEventHandle)

        self.mapper = mapper
        
        self.sliceNumberMinValue = mapper.GetSliceNumberMinValue()
        self.currentSlice = self.sliceNumberMinValue
        self.sliceNumberMaxValue = mapper.GetSliceNumberMaxValue()

        self.windowLevel = False

    def __leftButtonPressEventHandle(self, obj, event: str) -> None:
        self.OnLeftButtonDown()

    def __leftButtonReleaseEventHandle(self, obj, event: str) -> None:
        self.OnLeftButtonDown()

    def __mouseWheelForwardEventHandle(self, obj, event) -> None:
        if self.currentSlice > self.sliceNumberMinValue:
            self.mapper.SetSliceNumber(self.currentSlice)
            self.currentSlice = self.currentSlice - 1
        else:
            self.currentSlice = self.sliceNumberMaxValue
            self.mapper.SetSliceNumber(self.currentSlice)
            self.currentSlice = self.currentSlice - 1
        self.GetInteractor().Render()

    def __mouseWheelBackwardEventHandle(self, obj, event) -> None:
        if self.currentSlice <= self.sliceNumberMaxValue:
            self.mapper.SetSliceNumber(self.currentSlice)
            self.currentSlice = self.currentSlice + 1
        else:
            self.currentSlice = self.sliceNumberMinValue
            self.mapper.SetSliceNumber(self.currentSlice)
            self.currentSlice = self.currentSlice + 1
        self.GetInteractor().Render()

    def __mouseMoveEventHandle(self, obj, event) -> None:
        if self.windowLevel:
            self.WindowLevel()
        else:
            self.OnMouseMove()

    def __rightButtonPressEventHandle(self, obj, event) -> None:
        # self.OnRightButtonDown()
        self.StartWindowLevel()
        if not self.windowLevel:
            self.windowLevel = True
        self.GetInteractor().Render()

    def __rightButtonReleaseEventHandle(self, obj, event) -> None:
        # self.OnRightButtonUp()
        if self.windowLevel:
            self.windowLevel = False
        self.EndWindowLevel()
        self.GetInteractor().Render()

def main(path_to_dir: str) -> None:
    # Init
    reader = vtk.vtkDICOMImageReader()
    mapper = vtk.vtkImageSliceMapper()
    originalSlice = vtk.vtkImageSlice()
    rendererAxialPlane = vtk.vtkRenderer()
    # rendererCoronalPlane = vtk.vtkRenderer()
    # rendererSagittalPlane = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    reader.SetDirectoryName(path_to_dir)
    reader.Update()

    imageData = reader.GetOutput()
    print(imageData)

    mapper.SetInputData(imageData)

    originalSlice.SetMapper(mapper)

    rendererAxialPlane.AddViewProp(originalSlice)
    # rendererAxialPlane.SetViewport(0.0, 0.0, 0.5, 1.0)

    # rendererCoronalPlane.AddViewProp(originalSlice)
    # rendererCoronalPlane.SetViewport(0.5, 0.0, 1.0, 0.5)

    # rendererSagittalPlane.AddViewProp(originalSlice)
    # rendererSagittalPlane.SetViewport(0.5, 0.5, 1.0, 1.0)
    
    renderWindow.AddRenderer(rendererAxialPlane)
    # renderWindow.AddRenderer(rendererCoronalPlane)
    # renderWindow.AddRenderer(rendererSagittalPlane)
    renderWindow.SetSize(500, 500)
    renderWindow.SetWindowName("MPR")

    interactorStyle = MyInteractorStyle(mapper)
    renderWindowInteractor.SetInteractorStyle(interactorStyle)

    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    path_to_dir = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    main(path_to_dir)
