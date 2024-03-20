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

'''
Params:
    A: a point in 3-dimensional space
    B: a point in 3-dimensional space
    C: a point in 3-dimensional space
Description: Calculate the angle between 2 vectors
'''
def calcAngleBetweenTwoVectors(A, B, C) -> float:
    BA = [A[0] - B[0], A[1] - B[1], A[2] - B[2]]
    BC = [C[0] - B[0], C[1] - B[1], C[2] - B[2]]
    radianAngle = vtkmath.AngleBetweenVectors(BA, BC) # radian unit
    degreeAngle = vtkmath.DegreesFromRadians(radianAngle) # degree unit
    # BA x BC (Cross product)
    crossProduct = [
        BA[1] * BC[2] - BA[2] * BC[1],
        BA[2] * BC[0] - BA[0] * BC[2],
        BA[0] * BC[1] - BA[1] * BC[0]
    ]
    return degreeAngle if crossProduct[2] < 0 else -degreeAngle

def main(path_to_dir):
    # Markup by sphere
    colors = vtk.vtkNamedColors()
    # sphere = vtk.vtkSphereSource()
    # mapper = vtk.vtkPolyDataMapper()
    # property = vtk.vtkProperty()
    # sphereActor = vtk.vtkActor()

    # sphere.SetRadius(10)
    # mapper.SetInputConnection(sphere.GetOutputPort())
    # property.SetColor(colors.GetColor3d("Blue"))
    # sphereActor.SetMapper(mapper)
    # sphereActor.SetProperty(property)

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
    rotationMatrix = vtk.vtkMatrix4x4()
    resultMatrix = vtk.vtkMatrix4x4()
    resliceAxial = vtk.vtkImageReslice()
    resliceCoronal = vtk.vtkImageReslice()
    resliceSagittal = vtk.vtkImageReslice()
    actorAxial = vtk.vtkImageActor()
    actorCoronal = vtk.vtkImageActor()
    actorSagittal = vtk.vtkImageActor()
    cameraAxialView = vtk.vtkCamera()
    cameraCoronalView = vtk.vtkCamera()
    cameraSagittalView = vtk.vtkCamera()
    rendererAxial = vtk.vtkRenderer()
    rendererCoronal = vtk.vtkRenderer()
    rendererSagittal = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    # interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
    interactorStyle = vtk.vtkInteractorStyleImage()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()

    # Setup interactor style
    interactorStyle.SetInteractionModeToImageSlicing()
    # Setup render window interactor
    renderWindowInteractor.SetInteractorStyle(interactorStyle)

    # Setup render window
    renderWindow.SetSize(800, 400)
    renderWindow.SetWindowName("3D MPR")
    renderWindow.SetInteractor(renderWindowInteractor)
    # renderWindowInteractor.SetRenderWindow(renderWindow)

    # Reader
    reader.SetDirectoryName(path_to_dir)
    reader.Update()
    imageData = reader.GetOutput()
    center = imageData.GetCenter()
    (xMin, xMax, yMin, yMax, zMin, zMax) = imageData.GetBounds()

    # Setup widgets in axial view
    sphereWidgetAxial.SetCenter(center)
    sphereWidgetAxial.SetRadius(8)
    sphereWidgetAxial.SetInteractor(renderWindowInteractor)
    sphereWidgetAxial.SetRepresentationToSurface()
    sphereWidgetAxial.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))
    sphereWidgetAxial.GetSelectedSphereProperty().SetOpacity(0)
    # Markup a position to rotate a green line in axial view
    sphereWidgetInteractionRotateGreenLineAxial = vtk.vtkSphereWidget()
    sphereWidgetInteractionRotateGreenLineAxial.SetRadius(8)
    sphereWidgetInteractionRotateGreenLineAxial.SetInteractor(renderWindowInteractor)
    sphereWidgetInteractionRotateGreenLineAxial.SetRepresentationToSurface()
    sphereWidgetInteractionRotateGreenLineAxial.GetSphereProperty().SetColor(colors.GetColor3d("Green"))
    sphereWidgetInteractionRotateGreenLineAxial.GetSelectedSphereProperty().SetOpacity(0)

    # Setup widgets in coronal view
    sphereWidgetCoronal.SetCenter(center)
    sphereWidgetCoronal.SetRadius(8)
    # sphereWidgetCoronal.SetInteractor(renderWindowInteractor)
    sphereWidgetCoronal.SetInteractor(renderWindowInteractor)
    sphereWidgetCoronal.SetRepresentationToSurface()
    sphereWidgetCoronal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))
    sphereWidgetCoronal.GetSelectedSphereProperty().SetOpacity(0)

    # Setup widgets in sagittal view
    sphereWidgetSagittal.SetCenter(center)
    sphereWidgetSagittal.SetRadius(8)
    # sphereWidgetSagittal.SetInteractor(renderWindowInteractor)
    sphereWidgetSagittal.SetInteractor(renderWindowInteractor)
    sphereWidgetSagittal.SetRepresentationToSurface()
    sphereWidgetSagittal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))
    sphereWidgetSagittal.GetSelectedSphereProperty().SetOpacity(0)

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

    # Display dicom
    actorAxial.GetMapper().SetInputConnection(resliceAxial.GetOutputPort())
    actorCoronal.GetMapper().SetInputConnection(resliceCoronal.GetOutputPort())
    actorSagittal.GetMapper().SetInputConnection(resliceSagittal.GetOutputPort())

    # Set position and rotate dicom
    actorAxial.SetUserMatrix(axial)
    actorCoronal.SetUserMatrix(coronal)
    actorSagittal.SetUserMatrix(sagittal)
    # sphereActor.SetPosition(0, 0, 0)

    # Renderers
    rendererAxial.AddActor(actorAxial)
    # rendererAxial.AddActor(sphereActor)
    rendererAxial.AddActor(greenLineAxialActor)
    rendererAxial.AddActor(blueLineAxialActor)
    rendererAxial.SetViewport(0, 0, 0.5, 1)
    rendererAxial.SetBackground(0.3, 0.1, 0.1)
    cameraAxialView.SetPosition(center[0], center[1], 3*zMax)
    cameraAxialView.SetFocalPoint(center)
    cameraAxialView.SetViewUp(0, 1, 0)
    cameraAxialView.SetThickness(3*zMax)
    rendererAxial.SetActiveCamera(cameraAxialView)
    sphereWidgetAxial.SetCurrentRenderer(rendererAxial)
    sphereWidgetInteractionRotateGreenLineAxial.SetCurrentRenderer(rendererAxial)

    rendererCoronal.AddActor(actorCoronal)
    # rendererCoronal.AddActor(sphereActor)
    rendererCoronal.AddActor(greenLineCoronalActor)
    rendererCoronal.AddActor(redLineCoronalActor)
    rendererCoronal.SetViewport(0.5, 0, 1, 0.5)
    rendererCoronal.SetBackground(0.1, 0.3, 0.1)
    cameraCoronalView.SetPosition(center[0], 3*yMax, center[2])
    cameraCoronalView.SetFocalPoint(center)
    cameraCoronalView.SetViewUp(0, 0, -1)
    cameraCoronalView.SetThickness(3*yMax)
    rendererCoronal.SetActiveCamera(cameraCoronalView)
    sphereWidgetCoronal.SetCurrentRenderer(rendererCoronal)

    rendererSagittal.AddActor(actorSagittal)
    # rendererSagittal.AddActor(sphereActor)
    rendererSagittal.AddActor(blueLineSagittalActor)
    rendererSagittal.AddActor(redLineSagittalActor)
    rendererSagittal.SetViewport(0.5, 0.5, 1, 1)
    rendererSagittal.SetBackground(0.1, 0.1, 0.3)
    cameraSagittalView.SetPosition(3*xMax, center[1], center[2])
    cameraSagittalView.SetFocalPoint(center)
    cameraSagittalView.SetViewUp(0, 0, -1)
    cameraSagittalView.SetThickness(3.5*xMax)
    rendererSagittal.SetActiveCamera(cameraSagittalView)
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

    # Set lines in coronal view
    greenLineCoronal.SetPoint1(0, 0, -zMax)
    greenLineCoronal.SetPoint2(0, 0, zMax)
    greenLineCoronalActor.SetOrigin(0, 0, 0)
    greenLineCoronalActor.SetPosition(center)
    redLineCoronal.SetPoint1(-xMax, 0, 0)
    redLineCoronal.SetPoint2(xMax, 0, 0)
    redLineCoronalActor.SetOrigin(0, 0, 0)
    redLineCoronalActor.SetPosition(center)

    # Set lines in sagittal view
    blueLineSagittal.SetPoint1(0, 0, -zMax)
    blueLineSagittal.SetPoint2(0, 0, zMax)
    blueLineSagittalActor.SetOrigin(0, 0, 0)
    blueLineSagittalActor.SetPosition(center)
    redLineSagittal.SetPoint1(0, -yMax, 0)
    redLineSagittal.SetPoint2(0, yMax, 0)
    redLineSagittalActor.SetOrigin(0, 0, 0)
    redLineSagittalActor.SetPosition(center)

    # Init rotation matrix (y-axes)
    rotationMatrix.DeepCopy(
        (math.cos(math.radians(0)), 0, math.sin(math.radians(0)), 0, 
        0, 1, 0, 0, 
        -math.sin(math.radians(0)), 0, math.cos(math.radians(0)), 0, 
        0, 0, 0, 1)
    )

    # Create callback function for sphere widget interaction
    currentSphereWidgetCenter = {
        "axial": sphereWidgetAxial.GetCenter(),
        "coronal": sphereWidgetCoronal.GetCenter(),
        "sagittal": sphereWidgetSagittal.GetCenter()
    }
    currentSphereWidgetCenterRotateLinesAxial = {
        "green": sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
    }
    def interactionEventHandleTranslateLines_AxialView(obj, event) -> None:
        newPosition = obj.GetCenter()
        translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]

        # Translate lines in axial view
        greenLineAxialActor.SetPosition(newPosition)
        blueLineAxialActor.SetPosition(newPosition)
        # Translate a rotation point on green line in axial view
        sphereWidgetInteractionRotateGreenLineAxial.SetCenter([sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
        currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

        resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in sagittal view
        sphereWidgetSagittal.SetCenter(newPosition)
        # Translate lines in sagital view
        blueLineSagittalActor.SetPosition(newPosition)
        redLineSagittalActor.SetPosition(newPosition)
        # Set position of camera in sagittal view
        # cameraPosition = rendererSagittal.GetActiveCamera().GetPosition()
        # focalPoint = rendererSagittal.GetActiveCamera().GetFocalPoint()
        # rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1], cameraPosition[2])
        # rendererSagittal.GetActiveCamera().SetFocalPoint(focalPoint[0] + translationInterval[0], focalPoint[1], focalPoint[2])
        # rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1] + translationInterval[1], cameraPosition[2] + translationInterval[2])
        # rendererSagittal.GetActiveCamera().SetFocalPoint(focalPoint[0] + translationInterval[0], focalPoint[1] + translationInterval[1], focalPoint[2] + translationInterval[2])
        
        resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in coronal view
        sphereWidgetCoronal.SetCenter(newPosition)
        # Translate lines in coronal view
        greenLineCoronalActor.SetPosition(newPosition)
        redLineCoronalActor.SetPosition(newPosition)
        # Set position of camera in coronal view
        # cameraPosition = rendererCoronal.GetActiveCamera().GetPosition()
        # focalPoint = rendererCoronal.GetActiveCamera().GetFocalPoint()
        # rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1] + translationInterval[1], cameraPosition[2])
        # rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1] + translationInterval[1], cameraPosition[2] + translationInterval[2])
        # rendererCoronal.GetActiveCamera().SetFocalPoint(focalPoint[0] + translationInterval[0], focalPoint[1] + translationInterval[1], focalPoint[2] + translationInterval[2])

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
        sphereWidgetInteractionRotateGreenLineAxial.SetCenter([sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
        currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
        # Set position of camera in axial view
        # cameraPosition = rendererAxial.GetActiveCamera().GetPosition()
        # rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1], cameraPosition[2] + translationInterval[2])
        # rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1] + translationInterval[1], cameraPosition[2] + translationInterval[2])

        resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in sagittal view
        sphereWidgetSagittal.SetCenter(newPosition)
        # Translate lines in sagittal view
        blueLineSagittalActor.SetPosition(newPosition)
        redLineSagittalActor.SetPosition(newPosition)
        # Set position of camera in sagittal view
        # cameraPosition = rendererSagittal.GetActiveCamera().GetPosition()
        # rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1], cameraPosition[2])
        # rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1] + translationInterval[1], cameraPosition[2] + translationInterval[2])

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
        sphereWidgetInteractionRotateGreenLineAxial.SetCenter([sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
        currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
        # Set position of camera in axial view
        # cameraPosition = rendererAxial.GetActiveCamera().GetPosition()
        # rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1], cameraPosition[2] + translationInterval[2])
        # rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1] + translationInterval[1], cameraPosition[2] + translationInterval[2])

        resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
        resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
        resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
        # Translate sphere widget in coronal view
        sphereWidgetCoronal.SetCenter(newPosition)
        # Translate lines in coronal view
        greenLineCoronalActor.SetPosition(newPosition)
        redLineCoronalActor.SetPosition(newPosition)
        # Set position of camera in coronal view
        # cameraPosition = rendererCoronal.GetActiveCamera().GetPosition()
        # rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1] + translationInterval[1], cameraPosition[2])
        # rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0] + translationInterval[0], cameraPosition[1] + translationInterval[1], cameraPosition[2] + translationInterval[2])

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

        # Set elements of rotation matrix (y-axes)
        rotationMatrix.SetElement(0, 0, math.cos(math.radians(angle)))
        rotationMatrix.SetElement(0, 2, math.sin(math.radians(angle)))
        rotationMatrix.SetElement(2, 0, -math.sin(math.radians(angle)))
        rotationMatrix.SetElement(2, 2, math.cos(math.radians(angle)))
        
        # Set transform matrix (sagittal view)
        vtk.vtkMatrix4x4.Multiply4x4(resliceSagittal.GetResliceAxes(), rotationMatrix, resultMatrix)
        for i in range(4):
            for j in range(4):
                resliceSagittal.GetResliceAxes().SetElement(i, j, resultMatrix.GetElement(i, j))
        redLineSagittalActor.RotateZ(-angle)
        rendererSagittal.GetActiveCamera().Azimuth(angle)

        # Set transform matrix (coronal view)
        vtk.vtkMatrix4x4.Multiply4x4(resliceCoronal.GetResliceAxes(), rotationMatrix, resultMatrix)
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
            sliceSpacing = resliceAxial.GetOutput().GetSpacing()[2]
            cameraPosition = rendererAxial.GetActiveCamera().GetPosition()
            focalPoint = rendererAxial.GetActiveCamera().GetFocalPoint()
            if event == "MouseWheelForwardEvent":
                # Move the center point that we are slicing through
                # newPosition = resliceAxial.GetResliceAxes().MultiplyPoint((0, 0, -sliceSpacing, 1))
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                temp = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["axial"][i] + temp[i] for i in range(3)]
                resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
                # sliceSpacing = -sliceSpacing
            elif event == "MouseWheelBackwardEvent":
                # Move the center point that we are slicing through
                # newPosition = resliceAxial.GetResliceAxes().MultiplyPoint((0, 0, sliceSpacing, 1))
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                temp = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["axial"][i] + temp[i] for i in range(3)]
                resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set position of camera in axial view
            # rendererAxial.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1], cameraPosition[2] + sliceSpacing)
            # Translate sphere widget in axial view
            # sphereWidgetAxial.SetCenter(currentSphereWidgetCenter["axial"][0], currentSphereWidgetCenter["axial"][1], currentSphereWidgetCenter["axial"][2] + sliceSpacing)
            sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            greenLineAxialActor.SetPosition(newPosition)
            blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            # sphereWidgetInteractionRotateGreenLineAxial.SetCenter(sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[0], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[1], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[2] + sliceSpacing)
            sphereWidgetInteractionRotateGreenLineAxial.SetCenter([sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in coronal view
            # sphereWidgetCoronal.SetCenter(currentSphereWidgetCenter["coronal"][0], currentSphereWidgetCenter["coronal"][1], currentSphereWidgetCenter["coronal"][2] + sliceSpacing)
            sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            greenLineCoronalActor.SetPosition(newPosition)
            redLineCoronalActor.SetPosition(newPosition)
            
            # Translate sphere widget in sagittal view
            # sphereWidgetSagittal.SetCenter(currentSphereWidgetCenter["sagittal"][0], currentSphereWidgetCenter["sagittal"][1], currentSphereWidgetCenter["sagittal"][2] + sliceSpacing)
            sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            blueLineSagittalActor.SetPosition(newPosition)
            redLineSagittalActor.SetPosition(newPosition)
        # Coronal view
        elif viewId == 2:
            sliceSpacing = resliceCoronal.GetOutput().GetSpacing()[2]
            cameraPosition = rendererCoronal.GetActiveCamera().GetPosition()
            focalPoint = rendererCoronal.GetActiveCamera().GetFocalPoint()
            if event == "MouseWheelForwardEvent":
                # move the center point that we are slicing through
                # newPosition = [
                #     resliceCoronal.GetResliceAxes().GetElement(0, 3), 
                #     resliceCoronal.GetResliceAxes().GetElement(1, 3) - sliceSpacing, 
                #     resliceCoronal.GetResliceAxes().GetElement(2, 3)
                # ]
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                temp = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["coronal"][i] + temp[i] for i in range(3)]
                resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
                # sliceSpacing = -sliceSpacing
            elif event == "MouseWheelBackwardEvent":
                # move the center point that we are slicing through
                # newPosition = [
                #     resliceCoronal.GetResliceAxes().GetElement(0, 3), 
                #     resliceCoronal.GetResliceAxes().GetElement(1, 3) + sliceSpacing, 
                #     resliceCoronal.GetResliceAxes().GetElement(2, 3)
                # ]
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                temp = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["coronal"][i] + temp[i] for i in range(3)]
                resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set position of camera in coronal view
            # rendererCoronal.GetActiveCamera().SetPosition(cameraPosition[0], cameraPosition[1] + sliceSpacing, cameraPosition[2])

            # Translate sphere widget in coronal view
            # sphereWidgetCoronal.SetCenter(currentSphereWidgetCenter["coronal"][0], currentSphereWidgetCenter["coronal"][1] + sliceSpacing, currentSphereWidgetCenter["coronal"][2])
            sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            greenLineCoronalActor.SetPosition(newPosition)
            redLineCoronalActor.SetPosition(newPosition)
            
            # Translate sphere widget in axial view
            # sphereWidgetAxial.SetCenter(currentSphereWidgetCenter["axial"][0], currentSphereWidgetCenter["axial"][1] + sliceSpacing, currentSphereWidgetCenter["axial"][2])
            sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            greenLineAxialActor.SetPosition(newPosition)
            blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            # sphereWidgetInteractionRotateGreenLineAxial.SetCenter(sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[0], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[1] + sliceSpacing, sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[2])
            sphereWidgetInteractionRotateGreenLineAxial.SetCenter([sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in sagittal view
            # sphereWidgetSagittal.SetCenter(currentSphereWidgetCenter["sagittal"][0], currentSphereWidgetCenter["sagittal"][1] + sliceSpacing, currentSphereWidgetCenter["sagittal"][2])
            sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            blueLineSagittalActor.SetPosition(newPosition)
            redLineSagittalActor.SetPosition(newPosition)
        # Sagittal view
        elif viewId == 3:
            sliceSpacing = resliceSagittal.GetOutput().GetSpacing()[2]
            cameraPosition = rendererSagittal.GetActiveCamera().GetPosition()
            focalPoint = rendererSagittal.GetActiveCamera().GetFocalPoint()
            if event == "MouseWheelForwardEvent":
                # move the center point that we are slicing through
                # newPosition = [
                #     resliceSagittal.GetResliceAxes().GetElement(0, 3) - sliceSpacing, 
                #     resliceSagittal.GetResliceAxes().GetElement(1, 3), 
                #     resliceSagittal.GetResliceAxes().GetElement(2, 3)
                # ]
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                temp = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["sagittal"][i] + temp[i] for i in range(3)]
                resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
                # sliceSpacing = -sliceSpacing
            elif event == "MouseWheelBackwardEvent":
                # move the center point that we are slicing through
                # newPosition = [
                #     resliceSagittal.GetResliceAxes().GetElement(0, 3) + sliceSpacing, 
                #     resliceSagittal.GetResliceAxes().GetElement(1, 3), 
                #     resliceSagittal.GetResliceAxes().GetElement(2, 3)
                # ]
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                temp = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["sagittal"][i] + temp[i] for i in range(3)]
                resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set position of camera in sagittal view
            # rendererSagittal.GetActiveCamera().SetPosition(cameraPosition[0] + sliceSpacing, cameraPosition[1], cameraPosition[2])

            # Translate sphere widget in sagittal view
            # sphereWidgetSagittal.SetCenter(currentSphereWidgetCenter["sagittal"][0] + sliceSpacing, currentSphereWidgetCenter["sagittal"][1], currentSphereWidgetCenter["sagittal"][2])
            sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            blueLineSagittalActor.SetPosition(newPosition)
            redLineSagittalActor.SetPosition(newPosition)

            # Translate sphere widget in axial view
            # sphereWidgetAxial.SetCenter(currentSphereWidgetCenter["axial"][0] + sliceSpacing, currentSphereWidgetCenter["axial"][1], currentSphereWidgetCenter["axial"][2])
            sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            greenLineAxialActor.SetPosition(newPosition)
            blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            # sphereWidgetInteractionRotateGreenLineAxial.SetCenter(sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[0] + sliceSpacing, sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[1], sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[2])
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            sphereWidgetInteractionRotateGreenLineAxial.SetCenter([sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in coronal view
            # sphereWidgetCoronal.SetCenter(currentSphereWidgetCenter["coronal"][0] + sliceSpacing, currentSphereWidgetCenter["coronal"][1], currentSphereWidgetCenter["coronal"][2])
            sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            greenLineCoronalActor.SetPosition(newPosition)
            redLineCoronalActor.SetPosition(newPosition)
        
        currentSphereWidgetCenter["axial"] = sphereWidgetAxial.GetCenter()
        currentSphereWidgetCenter["coronal"] = sphereWidgetCoronal.GetCenter()
        currentSphereWidgetCenter["sagittal"] = sphereWidgetSagittal.GetCenter()
        renderWindow.Render()
        
    interactorStyle.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandle)
    interactorStyle.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandle)

    # Turn on widgets
    sphereWidgetAxial.On()
    sphereWidgetInteractionRotateGreenLineAxial.On()
    sphereWidgetCoronal.On()
    sphereWidgetSagittal.On()

    renderWindowInteractor.Start()

if __name__ == "__main__":
    path1 = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    path2 = "D:/workingspace/Python/dicom-data/64733 NGUYEN TAN THANH"
    path3 = "D:/workingspace/Python/dicom-data/23006355 NGUYEN VAN PHUONG/VR128904 Thorax 1_Nguc Adult/CT ThorRoutine 5.0 B70s"
    path4 = "D:/workingspace/Python/dicom-data/1.2.840.113619.2.428.3.678656.285.1684973027.401"
    path5 = "D:/workingspace/Python/dicom-data/17025648 HOANG VAN KHIEN/24.0203.003678 Chup CLVT he dong mach canh co tiem thuoc can quang tu 64128 d/CT 0.625mm KHONG THUOC"
    main(path1)
