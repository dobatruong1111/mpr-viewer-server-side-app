#!/usr/bin/env python

# This example shows how to load a 3D image into VTK and then reformat
# that image into a different orientation for viewing.  It uses
# vtkImageReslice for reformatting the image, and uses vtkImageActor
# and vtkInteractorStyleImage to display the image.  This InteractorStyle
# forces the camera to stay perpendicular to the XY plane.

import vtk
from vtkmodules.vtkCommonCore import vtkCommand
import math

vtkmath = vtk.vtkMath()

def calcAngleBetweenTwoVectors(A, B, C) -> float:
    BA = [A[0] - B[0], A[1] - B[1], A[2] - B[2]]
    BC = [C[0] - B[0], C[1] - B[1], C[2] - B[2]]
    radianAngle = vtkmath.AngleBetweenVectors(BA, BC) # radian unit
    degreeAngle = vtkmath.DegreesFromRadians(radianAngle) # degree unit
    # BA x BC (cross product)
    crossProduct = [
        BA[1] * BC[2] - BA[2] * BC[1],
        BA[2] * BC[0] - BA[0] * BC[2],
        BA[0] * BC[1] - BA[1] * BC[0]
    ]
    return degreeAngle if crossProduct[2] < 0 else -degreeAngle

def calcTwoPointsOfLine(firstPoint, secondPoint) -> tuple:
    # Calc point1
    point1 = [firstPoint[0] * 2 - secondPoint[0], firstPoint[1] * 2 - secondPoint[1], firstPoint[2] * 2 - secondPoint[2]]
    # i = 0
    # while i < 1:
    #     point1 = [point1[0] * 2 - secondPoint[0], point1[1] * 2 - secondPoint[1], point1[2] * 2 - secondPoint[2]]
    #     i += 1

    # Calc point2
    point2 = [secondPoint[0] * 2 - point1[0], secondPoint[1] * 2 - point1[1], secondPoint[2] * 2 - point1[2]]
    return (point1, point2)

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
    greenLineAxialActor.GetProperty().SetLineWidth(1.5)

    blueLineAxial = vtk.vtkLineSource()
    blueLineAxialMapper = vtk.vtkPolyDataMapper()
    blueLineAxialActor = vtk.vtkActor()
    blueLineAxialMapper.SetInputConnection(blueLineAxial.GetOutputPort())
    blueLineAxialActor.SetMapper(blueLineAxialMapper)
    blueLineAxialActor.GetProperty().SetColor(colors.GetColor3d("Blue"))
    blueLineAxialActor.GetProperty().SetLineWidth(1.5)

    # Markup by two lines - coronal plane
    greenLineCoronal = vtk.vtkLineSource()
    greenLineCoronalMapper = vtk.vtkPolyDataMapper()
    greenLineCoronalActor = vtk.vtkActor()
    greenLineCoronalMapper.SetInputConnection(greenLineCoronal.GetOutputPort())
    greenLineCoronalActor.SetMapper(greenLineCoronalMapper)
    greenLineCoronalActor.GetProperty().SetColor(colors.GetColor3d("Green"))
    greenLineCoronalActor.GetProperty().SetLineWidth(1.5)

    redLineCoronal = vtk.vtkLineSource()
    redLineCoronalMapper = vtk.vtkPolyDataMapper()
    redLineCoronalActor = vtk.vtkActor()
    redLineCoronalMapper.SetInputConnection(redLineCoronal.GetOutputPort())
    redLineCoronalActor.SetMapper(redLineCoronalMapper)
    redLineCoronalActor.GetProperty().SetColor(colors.GetColor3d("Red"))
    redLineCoronalActor.GetProperty().SetLineWidth(1.5)

    # Markup by two lines - sagittal plane
    blueLineSagittal = vtk.vtkLineSource()
    blueLineSagittalMapper = vtk.vtkPolyDataMapper()
    blueLineSagittalActor = vtk.vtkActor()
    blueLineSagittalMapper.SetInputConnection(blueLineSagittal.GetOutputPort())
    blueLineSagittalActor.SetMapper(blueLineSagittalMapper)
    blueLineSagittalActor.GetProperty().SetColor(colors.GetColor3d("Blue"))
    blueLineSagittalActor.GetProperty().SetLineWidth(1.5)

    redLineSagittal = vtk.vtkLineSource()
    redLineSagittalMapper = vtk.vtkPolyDataMapper()
    redLineSagittalActor = vtk.vtkActor()
    redLineSagittalMapper.SetInputConnection(redLineSagittal.GetOutputPort())
    redLineSagittalActor.SetMapper(redLineSagittalMapper)
    redLineSagittalActor.GetProperty().SetColor(colors.GetColor3d("Red"))
    redLineSagittalActor.GetProperty().SetLineWidth(1.5)

    # Markup a position by sphere widget
    sphereWidgetAxial = vtk.vtkSphereWidget()
    sphereWidgetCoronal = vtk.vtkSphereWidget()
    sphereWidgetSagittal = vtk.vtkSphereWidget()

    # Main init
    reader = vtk.vtkDICOMImageReader()
    axial = vtk.vtkMatrix4x4()
    coronal = vtk.vtkMatrix4x4()
    sagittal = vtk.vtkMatrix4x4()
    transformMatrix = vtk.vtkMatrix4x4()
    resultMatrix = vtk.vtkMatrix4x4()
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
    # interactorStyle = vtk.vtkInteractorStyleImage()
    interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()

    # Setup render window
    renderWindow.SetSize(800, 400)
    renderWindow.SetWindowName("3D MPR")
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

    # Setup widgets in axial view
    sphereWidgetAxial.SetCenter(center)
    sphereWidgetAxial.SetRadius(6)
    sphereWidgetAxial.SetInteractor(renderWindowInteractor)
    sphereWidgetAxial.SetRepresentationToSurface()
    sphereWidgetAxial.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))
    sphereWidgetAxial.GetSelectedSphereProperty().SetOpacity(0)
    # Markup a position to rotate a green line in axial view
    sphereWidgetInteractionRotateGreenLineAxial = vtk.vtkSphereWidget()
    sphereWidgetInteractionRotateGreenLineAxial.SetRadius(4)
    sphereWidgetInteractionRotateGreenLineAxial.SetInteractor(renderWindowInteractor)
    sphereWidgetInteractionRotateGreenLineAxial.SetRepresentationToSurface()
    sphereWidgetInteractionRotateGreenLineAxial.GetSphereProperty().SetColor(colors.GetColor3d("green"))
    sphereWidgetInteractionRotateGreenLineAxial.GetSelectedSphereProperty().SetOpacity(0)

    # Setup widgets in coronal view
    sphereWidgetCoronal.SetCenter(center)
    sphereWidgetCoronal.SetRadius(6)
    sphereWidgetCoronal.SetInteractor(renderWindowInteractor)
    sphereWidgetCoronal.SetRepresentationToSurface()
    sphereWidgetCoronal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    # Setup widgets in sagittal view
    sphereWidgetSagittal.SetCenter(center)
    sphereWidgetSagittal.SetRadius(6)
    sphereWidgetSagittal.SetInteractor(renderWindowInteractor)
    sphereWidgetSagittal.SetRepresentationToSurface()
    sphereWidgetSagittal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    # Matrices for axial, coronal, and sagittal view orientations
    # Model matrix = Translation matrix
    axial.DeepCopy((1, 0, 0, center[0],
                    0, 1, 0, center[1],
                    0, 0, 1, center[2],
                    0, 0, 0, 1))
    
    # Model matrix = Translation matrix . Rotation matrix x-axes(90)
    coronal.DeepCopy((1, 0, 0, center[0],
                    0, 0, 1, center[1],
                    0, -1, 0, center[2],
                    0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix x-axes(90) . Rotation matrix y-axes(90)
    # coronal.DeepCopy((0, 0, -1, center[0],
    #                 1, 0, 0, center[1],
    #                 0, -1, 0, center[2],
    #                 0, 0, 0, 1))

    # Model matrix = Translation matrix . Rotation matrix x-axes(90) . Rotation matrix y-axes(90)
    sagittal.DeepCopy((0, 0, -1, center[0],
                    1, 0, 0, center[1],
                    0, -1, 0, center[2],
                    0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix x-axes(90) . Rotation matrix y-axes(90) . Rotate matrix y-axes(45)
    # sagittal.DeepCopy((-math.sqrt(2)/2, 0, -math.sqrt(2)/2, center[0],
    #                 math.sqrt(2)/2, 0, -math.sqrt(2)/2, center[1],
    #                 0, -1, 0, center[2],
    #                 0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix x-axes(90) . Rotation matrix y-axes(90) . Rotation matrix y-axes(90)
    # sagittal.DeepCopy((-1, 0, 0, center[0],
    #                 0, 0, -1, center[1],
    #                 0, -1, 0, center[2],
    #                 0, 0, 0, 1))

    # Extract a slice in the desired orientation
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
    actorAxial.SetUserMatrix(axial)
    actorCoronal.SetUserMatrix(coronal)
    actorSagittal.SetUserMatrix(sagittal)
    sphereActor.SetPosition(0, 0, 0)

    # Renderers
    rendererAxial.AddActor(actorAxial)
    rendererAxial.AddActor(sphereActor)
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
    sphereWidgetInteractionRotateGreenLineAxial.SetCurrentRenderer(rendererAxial)

    rendererCoronal.AddActor(actorCoronal)
    rendererCoronal.AddActor(sphereActor)
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
    rendererSagittal.AddActor(sphereActor)
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

    # Set lines in axial view
    greenLineAxial.SetPoint1(0, yMax, 0)
    greenLineAxial.SetPoint2(0, -yMax, 0)
    greenLineAxialActor.SetOrigin(0, 0, 0)
    greenLineAxialActor.SetPosition(center)
    blueLineAxial.SetPoint1(-xMax, 0, 0)
    blueLineAxial.SetPoint2(xMax, 0, 0)
    blueLineAxialActor.SetOrigin(0, 0, 0)
    blueLineAxialActor.SetPosition(center)
    sphereWidgetInteractionRotateGreenLineAxial.SetCenter(center[0], (yMax + center[1])/2, center[2])
    # sphereWidgetInteractionRotateBlueLineAxial.SetCenter((xMin + center[0])/2, center[1], center[2])

    # Set lines in coronal view
    greenLineCoronal.SetPoint1(0, 0, -zMax)
    greenLineCoronal.SetPoint2(0, 0, zMax)
    greenLineCoronalActor.SetOrigin(0, 0, 0)
    greenLineCoronalActor.SetPosition(center)
    redLineCoronal.SetPoint1(-xMax, 0, 0)
    redLineCoronal.SetPoint2(xMax, 0, 0)
    redLineCoronalActor.SetOrigin(0, 0, 0)
    redLineCoronalActor.SetPosition(center)

    # Set lines in coronal view
    blueLineSagittal.SetPoint1(0, 0, -zMax)
    blueLineSagittal.SetPoint2(0, 0, zMax)
    blueLineSagittalActor.SetOrigin(0, 0, 0)
    blueLineSagittalActor.SetPosition(center)
    redLineSagittal.SetPoint1(0, -yMax, 0)
    redLineSagittal.SetPoint2(0, yMax, 0)
    redLineSagittalActor.SetOrigin(0, 0, 0)
    redLineSagittalActor.SetPosition(center)

    # Create callback function for sphere widget interaction
    currentSphereWidgetCenter = {
        "axial": sphereWidgetAxial.GetCenter(),
        "coronal": sphereWidgetCoronal.GetCenter(),
        "sagittal": sphereWidgetSagittal.GetCenter()
    }
    currentSphereWidgetCenterRotateLinesAxial = {
        "green": sphereWidgetInteractionRotateGreenLineAxial.GetCenter(),
        # "blue": sphereWidgetInteractionRotateBlueLineAxial.GetCenter()
    }

    def interactionEventHandleTranslateLines_AxialView(obj, event) -> None:
        newPosition = obj.GetCenter()
        translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]

        # Translate lines in axial view
        greenLineAxialActor.SetPosition(newPosition)
        blueLineAxialActor.SetPosition(newPosition)
        # Translate a rotation point on green line in axial view
        newCenter = [sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)]
        sphereWidgetInteractionRotateGreenLineAxial.SetCenter(newCenter)
        currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition

        resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in sagittal view
        sphereWidgetSagittal.SetCenter(newPosition)
        # Translate lines in sagital view
        blueLineSagittalActor.SetPosition(newPosition)
        redLineSagittalActor.SetPosition(newPosition)
        # Set position of camera in sagittal view
        cameraPosition = rendererSagittal.GetActiveCamera().GetPosition()
        rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1], cameraPosition[2])

        resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in coronal view
        sphereWidgetCoronal.SetCenter(newPosition)
        # Translate lines in coronal view
        greenLineCoronalActor.SetPosition(newPosition)
        redLineCoronalActor.SetPosition(newPosition)
        # Set position of camera in coronal view
        cameraPosition = rendererCoronal.GetActiveCamera().GetPosition()
        rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1] + translationInterval[1], cameraPosition[2])

        currentSphereWidgetCenter["axial"] = newPosition
        currentSphereWidgetCenter["sagittal"] = newPosition
        currentSphereWidgetCenter["coronal"] = newPosition
        renderWindow.Render()

    def interactionEventHandleTranslateLines_CoronalView(obj, event) -> None:
        newPosition = obj.GetCenter()
        translationInterval = [newPosition[i] - currentSphereWidgetCenter["coronal"][i] for i in range(3)]

        # Translate lines in coronal view
        greenLineCoronalActor.SetPosition(newPosition)
        redLineCoronalActor.SetPosition(newPosition)

        resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in axial view
        sphereWidgetAxial.SetCenter(newPosition)
        # Translate lines in axial view
        greenLineAxialActor.SetPosition(newPosition)
        blueLineAxialActor.SetPosition(newPosition)
        # Translate a rotation point on green line in axial view
        newCenter = [sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)]
        sphereWidgetInteractionRotateGreenLineAxial.SetCenter(newCenter)
        currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition
        # Set position of camera in axial view
        cameraPosition = rendererAxial.GetActiveCamera().GetPosition()
        rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1], cameraPosition[2] + translationInterval[2])

        resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in sagittal view
        sphereWidgetSagittal.SetCenter(newPosition)
        # Translate lines in sagittal view
        blueLineSagittalActor.SetPosition(newPosition)
        redLineSagittalActor.SetPosition(newPosition)
        # Set position of camera in sagittal view
        cameraPosition = rendererSagittal.GetActiveCamera().GetPosition()
        rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1], cameraPosition[2])

        currentSphereWidgetCenter["axial"] = newPosition
        currentSphereWidgetCenter["sagittal"] = newPosition
        currentSphereWidgetCenter["coronal"] = newPosition
        renderWindow.Render()

    def interactionEventHandleTranslateLines_SagittalView(obj, event) -> None:
        newPosition = obj.GetCenter()
        translationInterval = [newPosition[i] - currentSphereWidgetCenter["sagittal"][i] for i in range(3)]

        # Translate lines in sagittal view
        blueLineSagittalActor.SetPosition(newPosition)
        redLineSagittalActor.SetPosition(newPosition)

        resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in axial view
        sphereWidgetAxial.SetCenter(newPosition)
       # Translate lines in axial view
        greenLineAxialActor.SetPosition(newPosition)
        blueLineAxialActor.SetPosition(newPosition)
        # Translate a rotation point on green line in axial view
        newCenter = [sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)]
        sphereWidgetInteractionRotateGreenLineAxial.SetCenter(newCenter)
        currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition
        # Set position of camera in axial view
        cameraPosition = rendererAxial.GetActiveCamera().GetPosition()
        rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1], cameraPosition[2] + translationInterval[2])

        resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in coronal view
        sphereWidgetCoronal.SetCenter(newPosition)
        # Translate lines in coronal view
        greenLineCoronalActor.SetPosition(newPosition)
        redLineCoronalActor.SetPosition(newPosition)
        # Set position of camera in coronal view
        cameraPosition = rendererCoronal.GetActiveCamera().GetPosition()
        rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1] + translationInterval[1], cameraPosition[2])

        currentSphereWidgetCenter["axial"] = newPosition
        currentSphereWidgetCenter["sagittal"] = newPosition
        currentSphereWidgetCenter["coronal"] = newPosition
        renderWindow.Render()

    def interactionEventHandleRotateGreenLine_AxialView(obj, event) -> None:
        newPosition = obj.GetCenter()

        # Calculate rotation angle (degree unit)
        angle = calcAngleBetweenTwoVectors(currentSphereWidgetCenterRotateLinesAxial["green"], currentSphereWidgetCenter["axial"], newPosition)

        # Rotate lines in axial view
        greenLineAxialActor.RotateZ(-angle)
        blueLineAxialActor.RotateZ(-angle)

        # Create rotate matrix (y-axes)
        transformMatrix.DeepCopy(
            (math.cos(math.radians(angle)), 0, math.sin(math.radians(angle)), 0, 
            0, 1, 0, 0, 
            -math.sin(math.radians(angle)), 0, math.cos(math.radians(angle)), 0, 
            0, 0, 0, 1)
        )
        
        # Set transform matrix (sagittal view)
        vtk.vtkMatrix4x4.Multiply4x4(resliceSagittal.GetResliceAxes(), transformMatrix, resultMatrix)
        for i in range(4):
            for j in range(4):
                resliceSagittal.GetResliceAxes().SetElement(i, j, resultMatrix.GetElement(i, j))
        redLineSagittalActor.RotateZ(-angle)
        rendererSagittal.GetActiveCamera().Azimuth(angle)

        # Set transform matrix (coronal view)
        vtk.vtkMatrix4x4.Multiply4x4(resliceCoronal.GetResliceAxes(), transformMatrix, resultMatrix)
        for i in range(4):
            for j in range(4):
                resliceCoronal.GetResliceAxes().SetElement(i, j, resultMatrix.GetElement(i, j))
        redLineCoronalActor.RotateZ(-angle)
        rendererCoronal.GetActiveCamera().Azimuth(angle)

        currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition
        renderWindow.Render()

    sphereWidgetAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLines_AxialView)
    sphereWidgetInteractionRotateGreenLineAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleRotateGreenLine_AxialView)
    sphereWidgetCoronal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLines_CoronalView)
    sphereWidgetSagittal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLines_SagittalView)

    def mouseWheelEventHandle(obj, event) -> None:
        mousePosition = renderWindowInteractor.GetEventPosition()
        pokedRenderer = renderWindowInteractor.FindPokedRenderer(mousePosition[0], mousePosition[1])
        viewId = math.floor(sum(pokedRenderer.GetViewport()))

        # Axial view
        if (viewId == 1):
            cameraPosition = rendererAxial.GetActiveCamera().GetPosition()
            sliceSpacing = resliceAxial.GetOutput().GetSpacing()[2]
            if event == "MouseWheelForwardEvent":
                # Move the center point that we are slicing through
                newPosition = resliceAxial.GetResliceAxes().MultiplyPoint((0, 0, -sliceSpacing, 1))
                resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
                sliceSpacing = -sliceSpacing
            elif event == "MouseWheelBackwardEvent":
                # Move the center point that we are slicing through
                newPosition = resliceAxial.GetResliceAxes().MultiplyPoint((0, 0, sliceSpacing, 1))
                resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set position of camera in axial view
            rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1], cameraPosition[2] + sliceSpacing)

            # Translate sphere widget in axial view
            sphereWidgetAxial.SetCenter(currentSphereWidgetCenter["axial"][0], currentSphereWidgetCenter["axial"][1], currentSphereWidgetCenter["axial"][2] + sliceSpacing)
            # Translate lines in axial view
            greenLineAxialActor.SetPosition(sphereWidgetAxial.GetCenter())
            blueLineAxialActor.SetPosition(sphereWidgetAxial.GetCenter())
            # Translate a rotation point on green line in axial view
            sphereWidgetInteractionRotateGreenLineAxial.SetCenter(sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[0], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[1], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[2] + sliceSpacing)
            currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in coronal view
            sphereWidgetCoronal.SetCenter(currentSphereWidgetCenter["coronal"][0], currentSphereWidgetCenter["coronal"][1], currentSphereWidgetCenter["coronal"][2] + sliceSpacing)
            # Translate lines in coronal view
            greenLineCoronalActor.SetPosition(sphereWidgetCoronal.GetCenter())
            redLineCoronalActor.SetPosition(sphereWidgetCoronal.GetCenter())
            
            # Translate sphere widget in sagittal view
            sphereWidgetSagittal.SetCenter(currentSphereWidgetCenter["sagittal"][0], currentSphereWidgetCenter["sagittal"][1], currentSphereWidgetCenter["sagittal"][2] + sliceSpacing)
            # Translate lines in sagittal view
            blueLineSagittalActor.SetPosition(sphereWidgetSagittal.GetCenter())
            redLineSagittalActor.SetPosition(sphereWidgetSagittal.GetCenter())
        # Coronal view
        elif viewId == 2:
            cameraPosition = rendererCoronal.GetActiveCamera().GetPosition()
            sliceSpacing = resliceCoronal.GetOutput().GetSpacing()[2]
            if event == "MouseWheelForwardEvent":
                # move the center point that we are slicing through
                newPosition = [
                    resliceCoronal.GetResliceAxes().GetElement(0, 3), 
                    resliceCoronal.GetResliceAxes().GetElement(1, 3) - sliceSpacing, 
                    resliceCoronal.GetResliceAxes().GetElement(2, 3)
                ]
                resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
                sliceSpacing = -sliceSpacing
            elif event == "MouseWheelBackwardEvent":
                # move the center point that we are slicing through
                newPosition = [
                    resliceCoronal.GetResliceAxes().GetElement(0, 3), 
                    resliceCoronal.GetResliceAxes().GetElement(1, 3) + sliceSpacing, 
                    resliceCoronal.GetResliceAxes().GetElement(2, 3)
                ]
                resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set position of camera in coronal view
            rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1] + sliceSpacing, cameraPosition[2])

            # Translate sphere widget in coronal view
            sphereWidgetCoronal.SetCenter(currentSphereWidgetCenter["coronal"][0], currentSphereWidgetCenter["coronal"][1] + sliceSpacing, currentSphereWidgetCenter["coronal"][2])
            # Translate lines in coronal view
            greenLineCoronalActor.SetPosition(sphereWidgetCoronal.GetCenter())
            redLineCoronalActor.SetPosition(sphereWidgetCoronal.GetCenter())
            
            # Translate sphere widget in axial view
            sphereWidgetAxial.SetCenter(currentSphereWidgetCenter["axial"][0], currentSphereWidgetCenter["axial"][1] + sliceSpacing, currentSphereWidgetCenter["axial"][2])
            # Translate lines in axial view
            greenLineAxialActor.SetPosition(sphereWidgetAxial.GetCenter())
            blueLineAxialActor.SetPosition(sphereWidgetAxial.GetCenter())
            # Translate a rotation point on green line in axial view
            sphereWidgetInteractionRotateGreenLineAxial.SetCenter(sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[0], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[1] + sliceSpacing, sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[2])
            currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in sagittal view
            sphereWidgetSagittal.SetCenter(currentSphereWidgetCenter["sagittal"][0], currentSphereWidgetCenter["sagittal"][1] + sliceSpacing, currentSphereWidgetCenter["sagittal"][2])
            # Translate lines in sagittal view
            blueLineSagittalActor.SetPosition(sphereWidgetSagittal.GetCenter())
            redLineSagittalActor.SetPosition(sphereWidgetSagittal.GetCenter())
        # Sagittal view
        elif viewId == 3:
            cameraPosition = rendererSagittal.GetActiveCamera().GetPosition()
            sliceSpacing = resliceSagittal.GetOutput().GetSpacing()[2]
            if event == "MouseWheelForwardEvent":
                # move the center point that we are slicing through
                newPosition = [
                    resliceSagittal.GetResliceAxes().GetElement(0, 3) - sliceSpacing, 
                    resliceSagittal.GetResliceAxes().GetElement(1, 3), 
                    resliceSagittal.GetResliceAxes().GetElement(2, 3)
                ]
                resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
                sliceSpacing = -sliceSpacing
            elif event == "MouseWheelBackwardEvent":
                # move the center point that we are slicing through
                newPosition = [
                    resliceSagittal.GetResliceAxes().GetElement(0, 3) + sliceSpacing, 
                    resliceSagittal.GetResliceAxes().GetElement(1, 3), 
                    resliceSagittal.GetResliceAxes().GetElement(2, 3)
                ]
                resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set position of camera in sagittal view
            rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + sliceSpacing, cameraPosition[1], cameraPosition[2])

            # Translate sphere widget in sagittal view
            sphereWidgetSagittal.SetCenter(currentSphereWidgetCenter["sagittal"][0] + sliceSpacing, currentSphereWidgetCenter["sagittal"][1], currentSphereWidgetCenter["sagittal"][2])
            # Translate lines in sagittal view
            blueLineSagittalActor.SetPosition(sphereWidgetSagittal.GetCenter())
            redLineSagittalActor.SetPosition(sphereWidgetSagittal.GetCenter())

            # Translate sphere widget in axial view
            sphereWidgetAxial.SetCenter(currentSphereWidgetCenter["axial"][0] + sliceSpacing, currentSphereWidgetCenter["axial"][1], currentSphereWidgetCenter["axial"][2])
            # Translate lines in axial view
            greenLineAxialActor.SetPosition(sphereWidgetAxial.GetCenter())
            blueLineAxialActor.SetPosition(sphereWidgetAxial.GetCenter())
            # Translate a rotation point on green line in axial view
            sphereWidgetInteractionRotateGreenLineAxial.SetCenter(sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[0] + sliceSpacing, sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[1], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[2])
            currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in coronal view
            sphereWidgetCoronal.SetCenter(currentSphereWidgetCenter["coronal"][0] + sliceSpacing, currentSphereWidgetCenter["coronal"][1], currentSphereWidgetCenter["coronal"][2])
            # Translate lines in coronal view
            greenLineCoronalActor.SetPosition(sphereWidgetCoronal.GetCenter())
            redLineCoronalActor.SetPosition(sphereWidgetCoronal.GetCenter())
        
        currentSphereWidgetCenter["axial"] = sphereWidgetAxial.GetCenter()
        currentSphereWidgetCenter["coronal"] = sphereWidgetCoronal.GetCenter()
        currentSphereWidgetCenter["sagittal"] = sphereWidgetSagittal.GetCenter()
        renderWindow.Render()
        
    interactorStyle.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandle)
    interactorStyle.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandle)

    # Turn on sphere widget
    sphereWidgetAxial.On()
    sphereWidgetInteractionRotateGreenLineAxial.On()
    # sphereWidgetInteractionRotateBlueLineAxial.On()
    sphereWidgetCoronal.On()
    sphereWidgetSagittal.On()

    renderWindowInteractor.Start()

if __name__ == "__main__":
    path1 = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    path2 = "D:/workingspace/Python/dicom-data/64733 NGUYEN TAN THANH"
    path3 = "D:/workingspace/Python/dicom-data/23006355 NGUYEN VAN PHUONG/VR128904 Thorax 1_Nguc Adult/CT ThorRoutine 5.0 B70s"
    path4 = "D:/workingspace/Python/dicom-data/1.2.840.113619.2.428.3.678656.285.1684973027.401"
    main(path1)
