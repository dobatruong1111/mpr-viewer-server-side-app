#!/usr/bin/env python

# This example shows how to load a 3D image into VTK and then reformat
# that image into a different orientation for viewing.  It uses
# vtkImageReslice for reformatting the image, and uses vtkImageActor
# and vtkInteractorStyleImage to display the image.  This InteractorStyle
# forces the camera to stay perpendicular to the XY plane.

import vtk

def main(path_to_dir):
    # Markup by sphere
    colors = vtk.vtkNamedColors()
    sphere = vtk.vtkSphereSource()
    mapper = vtk.vtkPolyDataMapper()
    property = vtk.vtkProperty()
    sphereActor = vtk.vtkActor()

    sphere.SetRadius(10)
    mapper.SetInputConnection(sphere.GetOutputPort())
    property.SetColor(colors.GetColor3d("Blue"))
    sphereActor.SetMapper(mapper)
    sphereActor.SetProperty(property)

    # Markup by two lines - axial plane
    greenLineAxial = vtk.vtkLineSource()
    greenLineAxialMapper = vtk.vtkPolyDataMapper()
    greenLineAxialActor = vtk.vtkActor()
    greenLineAxialMapper.SetInputConnection(greenLineAxial.GetOutputPort())
    greenLineAxialActor.SetMapper(greenLineAxialMapper)
    greenLineAxialActor.GetProperty().SetColor(colors.GetColor3d("Green"))

    blueLineAxial = vtk.vtkLineSource()
    blueLineAxialMapper = vtk.vtkPolyDataMapper()
    blueLineAxialActor = vtk.vtkActor()
    blueLineAxialMapper.SetInputConnection(blueLineAxial.GetOutputPort())
    blueLineAxialActor.SetMapper(blueLineAxialMapper)
    blueLineAxialActor.GetProperty().SetColor(colors.GetColor3d("Blue"))

    # Markup by two lines - coronal plane
    greenLineCoronal = vtk.vtkLineSource()
    greenLineCoronalMapper = vtk.vtkPolyDataMapper()
    greenLineCoronalActor = vtk.vtkActor()
    greenLineCoronalMapper.SetInputConnection(greenLineCoronal.GetOutputPort())
    greenLineCoronalActor.SetMapper(greenLineCoronalMapper)
    greenLineCoronalActor.GetProperty().SetColor(colors.GetColor3d("Green"))

    redLineCoronal = vtk.vtkLineSource()
    redLineCoronalMapper = vtk.vtkPolyDataMapper()
    redLineCoronalActor = vtk.vtkActor()
    redLineCoronalMapper.SetInputConnection(redLineCoronal.GetOutputPort())
    redLineCoronalActor.SetMapper(redLineCoronalMapper)
    redLineCoronalActor.GetProperty().SetColor(colors.GetColor3d("Red"))

    # Markup by two lines - sagittal plane
    blueLineSagittal = vtk.vtkLineSource()
    blueLineSagittalMapper = vtk.vtkPolyDataMapper()
    blueLineSagittalActor = vtk.vtkActor()
    blueLineSagittalMapper.SetInputConnection(blueLineSagittal.GetOutputPort())
    blueLineSagittalActor.SetMapper(blueLineSagittalMapper)
    blueLineSagittalActor.GetProperty().SetColor(colors.GetColor3d("Blue"))

    redLineSagittal = vtk.vtkLineSource()
    redLineSagittalMapper = vtk.vtkPolyDataMapper()
    redLineSagittalActor = vtk.vtkActor()
    redLineSagittalMapper.SetInputConnection(redLineSagittal.GetOutputPort())
    redLineSagittalActor.SetMapper(redLineSagittalMapper)
    redLineSagittalActor.GetProperty().SetColor(colors.GetColor3d("Red"))

    # Markup by sphere widget
    sphereWidgetAxial = vtk.vtkSphereWidget()
    sphereWidgetCoronal = vtk.vtkSphereWidget()
    sphereWidgetSagittal = vtk.vtkSphereWidget()

    # Main init
    reader = vtk.vtkDICOMImageReader()
    axial = vtk.vtkMatrix4x4()
    coronal = vtk.vtkMatrix4x4()
    sagittal = vtk.vtkMatrix4x4()
    resliceAxial = vtk.vtkImageReslice()
    resliceCoronal = vtk.vtkImageReslice()
    resliceSagittal = vtk.vtkImageReslice()
    actorAxial = vtk.vtkImageActor()
    actorCoronal = vtk.vtkImageActor()
    actorSagittal = vtk.vtkImageActor()
    rendererAxial = vtk.vtkRenderer()
    rendererCoronal = vtk.vtkRenderer()
    rendererSagittal = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    # interactorStyle = vtk.vtkInteractorStyleImage()
    interactorStyle = vtk.vtkInteractorStyleTrackballCamera()

    # Setup render window
    renderWindow.SetSize(800, 400)
    renderWindow.SetWindowName("MPR Viewer")
    # interactorStyle.SetInteractionModeToImageSlicing()
    renderWindowInteractor.SetInteractorStyle(interactorStyle)
    # renderWindow.SetInteractor(renderWindowInteractor)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Reader
    reader.SetDirectoryName(path_to_dir)
    reader.Update()
    imageData = reader.GetOutput()
    center = imageData.GetCenter()
    (xMin, xMax, yMin, yMax, zMin, zMax) = imageData.GetBounds()
    spacing = imageData.GetSpacing()

    # Setup sphere widget
    sphereWidgetAxial.SetCenter(center)
    sphereWidgetAxial.SetRadius(10)
    sphereWidgetAxial.SetInteractor(renderWindowInteractor)
    sphereWidgetAxial.SetRepresentationToSurface()
    sphereWidgetAxial.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    sphereWidgetCoronal.SetCenter(center)
    sphereWidgetCoronal.SetRadius(10)
    sphereWidgetCoronal.SetInteractor(renderWindowInteractor)
    sphereWidgetCoronal.SetRepresentationToSurface()
    sphereWidgetCoronal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    sphereWidgetSagittal.SetCenter(center)
    sphereWidgetSagittal.SetRadius(10)
    sphereWidgetSagittal.SetInteractor(renderWindowInteractor)
    sphereWidgetSagittal.SetRepresentationToSurface()
    sphereWidgetSagittal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    # Set position of lines in planes
    def setLinesAxialPlane(newPosition) -> None:
        greenLineAxial.SetPoint1(newPosition[0], yMax, newPosition[2])
        greenLineAxial.SetPoint2(newPosition[0], yMin, newPosition[2])
        blueLineAxial.SetPoint1(xMin, newPosition[1], newPosition[2])
        blueLineAxial.SetPoint2(xMax, newPosition[1], newPosition[2])

    def setLinesCoronalPlane(newPosition) -> None:
        greenLineCoronal.SetPoint1(newPosition[0], newPosition[1], zMin)
        greenLineCoronal.SetPoint2(newPosition[0], newPosition[1], zMax)
        redLineCoronal.SetPoint1(xMax, newPosition[1], newPosition[2])
        redLineCoronal.SetPoint2(xMin, newPosition[1], newPosition[2])

    def setLinesSagittalPlane(newPosition) -> None:
        blueLineSagittal.SetPoint1(newPosition[0], newPosition[1], zMin)
        blueLineSagittal.SetPoint2(newPosition[0], newPosition[1], zMax)
        redLineSagittal.SetPoint1(newPosition[0], yMax, newPosition[2])
        redLineSagittal.SetPoint2(newPosition[0], yMin, newPosition[2])
    
    setLinesAxialPlane(center)
    setLinesCoronalPlane(center)
    setLinesSagittalPlane(center)

    # Matrices for axial, coronal, and sagittal view orientations
    # Model matrix = Translation matrix
    axial.DeepCopy((1, 0, 0, center[0],
                    0, 1, 0, center[1],
                    0, 0, 1, center[2],
                    0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix(X)
    coronal.DeepCopy((1, 0, 0, center[0],
                    0, 0, 1, center[1],
                    0, -1, 0, center[2],
                    0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix(X) . Rotation matrix(Y)
    sagittal.DeepCopy((0, 0, -1, center[0],
                    1, 0, 0, center[1],
                    0, -1, 0, center[2],
                    0, 0, 0, 1))

    # Extract a slice in the desired orientation
    '''
        vtkImageReslice(): It can permute, rotate, flip, scale, resample, deform, and pad
        image data in any combination with reasonably high efficiency
        1. Application of transformations (either linear or nonlinear) to an image
        2. Resampling of one data set to match the voxel sampling of a second data set
        3. Extraction of slices from an image volume
    '''
    resliceAxial.SetInputData(imageData)
    resliceAxial.SetOutputDimensionality(2)
    resliceAxial.SetResliceAxes(axial)
    resliceAxial.SetInterpolationModeToLinear()

    resliceCoronal.SetInputData(imageData)
    resliceCoronal.SetOutputDimensionality(2)
    resliceCoronal.SetResliceAxes(coronal)
    resliceCoronal.SetInterpolationModeToLinear()
    
    resliceSagittal.SetInputData(imageData)
    resliceSagittal.SetOutputDimensionality(2)
    resliceSagittal.SetResliceAxes(sagittal)
    resliceSagittal.SetInterpolationModeToLinear()

    # Display the image
    actorAxial.GetMapper().SetInputConnection(resliceAxial.GetOutputPort())
    actorCoronal.GetMapper().SetInputConnection(resliceCoronal.GetOutputPort())
    actorSagittal.GetMapper().SetInputConnection(resliceSagittal.GetOutputPort())

    # Set position and rotate image actor
    actorAxial.SetPosition(center)
    actorCoronal.SetPosition(center)
    actorCoronal.RotateX(-90)
    actorSagittal.SetPosition(center)
    actorSagittal.RotateX(-90)
    actorSagittal.RotateY(-90)
    sphereActor.SetPosition(0, 0, 0)
    # print(f"sphere position: {actor.GetPosition()}")
    # print(f"image position: {actorAxial.GetPosition()}")
    # print(f"image center position: {actorAxial.GetCenter()}")

    # Renderers
    rendererAxial.AddActor(actorAxial)
    # rendererAxial.AddActor(sphereActor)
    rendererAxial.AddActor(greenLineAxialActor)
    rendererAxial.AddActor(blueLineAxialActor)
    rendererAxial.SetViewport(0, 0, 0.5, 1)
    rendererAxial.SetBackground(0.3, 0.1, 0.1)
    rendererAxial.GetActiveCamera().SetFocalPoint(center)
    rendererAxial.GetActiveCamera().SetPosition(center[0], center[1], zMax + spacing[2])
    rendererAxial.GetActiveCamera().ParallelProjectionOn()
    rendererAxial.GetActiveCamera().SetViewUp(0, 1, 0)
    rendererAxial.ResetCamera()
    sphereWidgetAxial.SetCurrentRenderer(rendererAxial)

    rendererCoronal.AddActor(actorCoronal)
    # rendererCoronal.AddActor(sphereActor)
    rendererCoronal.AddActor(greenLineCoronalActor)
    rendererCoronal.AddActor(redLineCoronalActor)
    rendererCoronal.SetViewport(0.5, 0, 1, 0.5)
    rendererCoronal.SetBackground(0.1, 0.3, 0.1)
    rendererCoronal.GetActiveCamera().SetFocalPoint(center)
    rendererCoronal.GetActiveCamera().SetPosition(center[0], yMax + spacing[1], center[2])
    rendererCoronal.GetActiveCamera().ParallelProjectionOn()
    rendererCoronal.GetActiveCamera().SetViewUp(0, 0, -1)
    rendererCoronal.ResetCamera()
    sphereWidgetCoronal.SetCurrentRenderer(rendererCoronal)

    rendererSagittal.AddActor(actorSagittal)
    # rendererSagittal.AddActor(sphereActor)
    rendererSagittal.AddActor(blueLineSagittalActor)
    rendererSagittal.AddActor(redLineSagittalActor)
    rendererSagittal.SetViewport(0.5, 0.5, 1, 1)
    rendererSagittal.SetBackground(0.1, 0.1, 0.3)
    rendererSagittal.GetActiveCamera().SetFocalPoint(center)
    rendererSagittal.GetActiveCamera().SetPosition(xMax + spacing[0], center[1], center[2])
    rendererSagittal.GetActiveCamera().ParallelProjectionOn()
    rendererSagittal.GetActiveCamera().SetViewUp(0, 0, -1)
    rendererSagittal.ResetCamera()
    sphereWidgetSagittal.SetCurrentRenderer(rendererSagittal)

    # Render window
    renderWindow.AddRenderer(rendererAxial)
    renderWindow.AddRenderer(rendererCoronal)
    renderWindow.AddRenderer(rendererSagittal)
    renderWindow.Render()

    # Create callback function for sphere widget interactor
    def sphereWidgetInteractorCallbackFunction_AxialPlane(obj, event) -> None:
        newPosition = obj.GetCenter()

        resliceCoronal.Update()
        matrix = resliceCoronal.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, center[2])

        resliceSagittal.Update()
        matrix = resliceSagittal.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])

        setLinesAxialPlane(newPosition)

        # sphereWidgetCoronal.SetCenter(newPosition[0], center[1], center[2])
        # setLinesCoronalPlane([newPosition[0], center[1], center[2]])

        # sphereWidgetSagittal.SetCenter(center[0], newPosition[1], center[2])
        # setLinesSagittalPlane([center[0], newPosition[1], center[2]])

        actorCoronal.SetPosition(center[0], newPosition[1], center[2])
        sphereWidgetCoronal.SetCenter(newPosition)
        setLinesCoronalPlane(newPosition)

        actorSagittal.SetPosition(newPosition[0], center[1], center[2])
        sphereWidgetSagittal.SetCenter(newPosition)
        setLinesSagittalPlane(newPosition)

        rendererCoronal.ResetCamera()
        rendererSagittal.ResetCamera()

        renderWindow.Render()

    def sphereWidgetInteractorCallbackFunction_CoronalPlane(obj, event) -> None:
        newPosition = obj.GetCenter()

        matrix = resliceAxial.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, newPosition[2])

        matrix = resliceSagittal.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, center[2])

        # sphereWidgetAxial.SetCenter(newPosition[0], center[1], center[2])
        # setLinesAxialPlane([newPosition[0], center[1], center[2]])

        # setLinesCoronalPlane(newPosition)

        # sphereWidgetSagittal.SetCenter(center[0], center[1], newPosition[2])
        # setLinesSagittalPlane([center[0], center[1], newPosition[2]])

        setLinesCoronalPlane(newPosition)

        actorAxial.SetPosition(center[0], center[1], newPosition[2])
        sphereWidgetAxial.SetCenter(newPosition)
        setLinesAxialPlane(newPosition)
        
        actorSagittal.SetPosition(newPosition[0], center[1], center[2])
        sphereWidgetSagittal.SetCenter(newPosition)
        setLinesSagittalPlane(newPosition)

        rendererAxial.ResetCamera()
        rendererSagittal.ResetCamera()

        renderWindow.Render()

    def sphereWidgetInteractorCallbackFunction_SagittalPlane(obj, event) -> None:
        newPosition = obj.GetCenter()

        matrix = resliceAxial.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, center[1])
        matrix.SetElement(2, 3, newPosition[2])

        matrix = resliceCoronal.GetResliceAxes()
        matrix.SetElement(0, 3, center[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, center[2])

        # sphereWidgetAxial.SetCenter(center[0], newPosition[1], center[2])
        # setLinesAxialPlane([center[0], newPosition[1], center[2]])

        # sphereWidgetCoronal.SetCenter(center[0], center[1], newPosition[2])
        # setLinesCoronalPlane([center[0], center[1], newPosition[2]])

        setLinesSagittalPlane(newPosition)

        actorAxial.SetPosition(center[0], center[1], newPosition[2])
        sphereWidgetAxial.SetCenter(newPosition)
        setLinesAxialPlane(newPosition)

        actorCoronal.SetPosition(center[0], newPosition[1], center[2])
        sphereWidgetCoronal.SetCenter(newPosition)
        setLinesCoronalPlane(newPosition)

        rendererAxial.ResetCamera()
        rendererSagittal.ResetCamera()

        renderWindow.Render()

    sphereWidgetAxial.AddObserver("InteractionEvent", sphereWidgetInteractorCallbackFunction_AxialPlane)
    sphereWidgetCoronal.AddObserver("InteractionEvent", sphereWidgetInteractorCallbackFunction_CoronalPlane)
    sphereWidgetSagittal.AddObserver("InteractionEvent", sphereWidgetInteractorCallbackFunction_SagittalPlane)

    # Create callbacks for slicing the image
    actions = {}
    actions["Slicing"] = 0

    def ButtonCallback(obj, event) -> None:
        if event == "LeftButtonPressEvent":
            actions["Slicing"] = 1
        else:
            actions["Slicing"] = 0

    def MouseMoveCallback(obj, event) -> None:
        (lastX, lastY) = renderWindowInteractor.GetLastEventPosition()
        (mouseX, mouseY) = renderWindowInteractor.GetEventPosition()
        if actions["Slicing"] == 1:
            deltaY = mouseY - lastY

            resliceAxial.Update()
            sliceSpacing = resliceAxial.GetOutput().GetSpacing()[2]
            # move the center point that we are slicing through
            matrix = resliceAxial.GetResliceAxes()
            newPosition = matrix.MultiplyPoint((0, 0, sliceSpacing*deltaY, 1))
            matrix.SetElement(0, 3, newPosition[0])
            matrix.SetElement(1, 3, newPosition[1])
            matrix.SetElement(2, 3, newPosition[2])

            actorAxial.SetPosition(center[0], center[1], newPosition[2])
            sphereWidgetAxialCenter = sphereWidgetAxial.GetCenter()
            sphereWidgetAxial.SetCenter(sphereWidgetAxialCenter[0], sphereWidgetAxialCenter[1], newPosition[2])
            setLinesAxialPlane([sphereWidgetAxialCenter[0], sphereWidgetAxialCenter[1], newPosition[2]])

            # Set z-axes position of sphere widget
            sphereWidgetCoronalCenter = sphereWidgetCoronal.GetCenter()
            sphereWidgetCoronal.SetCenter(sphereWidgetCoronalCenter[0], sphereWidgetCoronalCenter[1], newPosition[2])
            setLinesCoronalPlane([sphereWidgetCoronalCenter[0], sphereWidgetCoronalCenter[1], newPosition[2]])
            
            sphereWidgetSagittalCenter = sphereWidgetSagittal.GetCenter()
            sphereWidgetSagittal.SetCenter(sphereWidgetSagittalCenter[0], sphereWidgetSagittalCenter[1], newPosition[2])
            setLinesSagittalPlane([sphereWidgetSagittalCenter[0], sphereWidgetSagittalCenter[1], newPosition[2]])

            rendererAxial.ResetCamera()

            renderWindow.Render()
        else:
            interactorStyle.OnMouseMove()
            
    interactorStyle.AddObserver("MouseMoveEvent", MouseMoveCallback)
    interactorStyle.AddObserver("LeftButtonPressEvent", ButtonCallback)
    interactorStyle.AddObserver("LeftButtonReleaseEvent", ButtonCallback)

    # Turn on sphere widget
    sphereWidgetAxial.On()
    sphereWidgetCoronal.On()
    sphereWidgetSagittal.On()

    renderWindowInteractor.Start()

if __name__ == "__main__":
    path1 = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    path2 = "D:/workingspace/Python/dicom-data/64733 NGUYEN TAN THANH"
    path3 = "D:/workingspace/Python/dicom-data/23006355 NGUYEN VAN PHUONG/VR128904 Thorax 1_Nguc Adult/CT ThorRoutine 5.0 B70s"
    main(path1)
