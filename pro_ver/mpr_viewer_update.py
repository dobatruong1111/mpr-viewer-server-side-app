# Render multi-view (multi render window)

import vtk
from vtkmodules.vtkCommonCore import vtkCommand
import math
from typing import Union, List, Tuple

vtkmath = vtk.vtkMath()

class MPRViewer(object):
    def __init__(self) -> None:
        self.colors = vtk.vtkNamedColors()
        self.initialize()

        self.initCenterlineAxialView()
        self.initCenterlineCoronalView()
        self.initCenterlineSagittalView()

        self.initWidgetsAxialView()
        self.initWidgetsCoronalView()
        self.initWidgetsSagittalView()

    def initialize(self) -> None:
        self.reader = vtk.vtkDICOMImageReader()
        self.axial = vtk.vtkMatrix4x4()
        self.coronal = vtk.vtkMatrix4x4()
        self.sagittal = vtk.vtkMatrix4x4()
        self.rotationMatrix = vtk.vtkMatrix4x4()
        self.resultMatrix = vtk.vtkMatrix4x4()
        self.resliceAxial = vtk.vtkImageReslice()
        self.resliceCoronal = vtk.vtkImageReslice()
        self.resliceSagittal = vtk.vtkImageReslice()
        self.actorAxial = vtk.vtkImageActor()
        self.actorCoronal = vtk.vtkImageActor()
        self.actorSagittal = vtk.vtkImageActor()
        self.cameraAxialView = vtk.vtkCamera()
        self.cameraCoronalView = vtk.vtkCamera()
        self.cameraSagittalView = vtk.vtkCamera()
        self.rendererAxial = vtk.vtkRenderer()
        self.rendererCoronal = vtk.vtkRenderer()
        self.rendererSagittal = vtk.vtkRenderer()
        self.renderWindowAxial = vtk.vtkRenderWindow()
        self.renderWindowCoronal = vtk.vtkRenderWindow()
        self.renderWindowSagittal = vtk.vtkRenderWindow()
        self.interactorStyleAxial = vtk.vtkInteractorStyleImage()
        # self.interactorStyleAxial = vtk.vtkInteractorStyleTrackballCamera()
        # self.interactorStyleAxial = vtk.vtkInteractorStyle()
        self.interactorStyleCoronal = vtk.vtkInteractorStyleImage()
        # self.interactorStyleCoronal = vtk.vtkInteractorStyleTrackballCamera()
        self.interactorStyleSagittal = vtk.vtkInteractorStyleImage()
        # self.interactorStyleSagittal = vtk.vtkInteractorStyleTrackballCamera()
        self.renderWindowInteractorAxial = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractorCoronal = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractorSagittal = vtk.vtkRenderWindowInteractor()

        self.rendererAxial.SetBackground(0.3, 0.1, 0.1)
        self.rendererCoronal.SetBackground(0.1, 0.3, 0.1)
        self.rendererSagittal.SetBackground(0.1, 0.1, 0.3)

        self.interactorStyleAxial.SetInteractionModeToImageSlicing()
        self.interactorStyleCoronal.SetInteractionModeToImageSlicing()
        self.interactorStyleSagittal.SetInteractionModeToImageSlicing()

        self.renderWindowInteractorAxial.SetInteractorStyle(self.interactorStyleAxial)
        self.renderWindowInteractorCoronal.SetInteractorStyle(self.interactorStyleCoronal)
        self.renderWindowInteractorSagittal.SetInteractorStyle(self.interactorStyleSagittal)

        self.renderWindowAxial.SetSize(400, 400)
        self.renderWindowAxial.SetWindowName("Axial view")
        self.renderWindowAxial.SetInteractor(self.renderWindowInteractorAxial)
        self.renderWindowAxial.SetPosition(0, 0)
        self.renderWindowAxial.AddRenderer(self.rendererAxial)

        self.renderWindowCoronal.SetSize(400, 400)
        self.renderWindowCoronal.SetWindowName("Coronal view")
        self.renderWindowCoronal.SetInteractor(self.renderWindowInteractorCoronal)
        self.renderWindowCoronal.SetPosition(400, 0)
        self.renderWindowCoronal.AddRenderer(self.rendererCoronal)

        self.renderWindowSagittal.SetSize(400, 400)
        self.renderWindowSagittal.SetWindowName("Sagittal view")
        self.renderWindowSagittal.SetInteractor(self.renderWindowInteractorSagittal)
        self.renderWindowSagittal.SetPosition(800, 0)
        self.renderWindowSagittal.AddRenderer(self.rendererSagittal)

        # Initialize rotation matrix (y-axes)
        self.rotationMatrix.DeepCopy(
            (math.cos(math.radians(0)), 0, math.sin(math.radians(0)), 0, 
            0, 1, 0, 0, 
            -math.sin(math.radians(0)), 0, math.cos(math.radians(0)), 0, 
            0, 0, 0, 1)
        )
    
    def initCenterlineAxialView(self) -> None:
        greenLineAxial = vtk.vtkLineSource()
        greenLineAxial.SetPoint1(0, 500, 0)
        greenLineAxial.SetPoint2(0, -500, 0)
        greenLineAxial.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(greenLineAxial.GetOutput().GetNumberOfCells())
        for c in range(greenLineAxial.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 255, 0])
        greenLineAxial.GetOutput().GetCellData().SetScalars(colorArray)

        blueLineAxial = vtk.vtkLineSource()
        blueLineAxial.SetPoint1(-500, 0, 0)
        blueLineAxial.SetPoint2(500, 0, 0)
        blueLineAxial.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(blueLineAxial.GetOutput().GetNumberOfCells())
        for c in range(blueLineAxial.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 0, 255])
        blueLineAxial.GetOutput().GetCellData().SetScalars(colorArray)

        linesAxial = vtk.vtkAppendPolyData()
        linesAxial.AddInputData(greenLineAxial.GetOutput())
        linesAxial.AddInputData(blueLineAxial.GetOutput())
        linesAxial.Update()

        linesAxialMapper = vtk.vtkPolyDataMapper()
        linesAxialMapper.SetInputConnection(linesAxial.GetOutputPort())

        self.linesAxialActor = vtk.vtkActor()
        self.linesAxialActor.SetMapper(linesAxialMapper)
        self.linesAxialActor.GetProperty().SetLineWidth(1)
        self.linesAxialActor.SetOrigin(0, 0, 0)
    
    def initCenterlineCoronalView(self) -> None:
        greenLineCoronal = vtk.vtkLineSource()
        greenLineCoronal.SetPoint1(0, 0, -500)
        greenLineCoronal.SetPoint2(0, 0, 500)
        greenLineCoronal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(greenLineCoronal.GetOutput().GetNumberOfCells())
        for c in range(greenLineCoronal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 255, 0])
        greenLineCoronal.GetOutput().GetCellData().SetScalars(colorArray)

        redLineCoronal = vtk.vtkLineSource()
        redLineCoronal.SetPoint1(-500, 0, 0)
        redLineCoronal.SetPoint2(500, 0, 0)
        redLineCoronal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(redLineCoronal.GetOutput().GetNumberOfCells())
        for c in range(redLineCoronal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [255, 0, 0])
        redLineCoronal.GetOutput().GetCellData().SetScalars(colorArray)

        linesCoronal = vtk.vtkAppendPolyData()
        linesCoronal.AddInputData(greenLineCoronal.GetOutput())
        linesCoronal.AddInputData(redLineCoronal.GetOutput())
        linesCoronal.Update()

        linesCoronalMapper = vtk.vtkPolyDataMapper()
        linesCoronalMapper.SetInputConnection(linesCoronal.GetOutputPort())

        self.linesCoronalActor = vtk.vtkActor()
        self.linesCoronalActor.SetMapper(linesCoronalMapper)
        self.linesCoronalActor.GetProperty().SetLineWidth(1)
        self.linesCoronalActor.SetOrigin(0, 0, 0)

    def initCenterlineSagittalView(self) -> None:
        blueLineSagittal = vtk.vtkLineSource()
        blueLineSagittal.SetPoint1(0, 0, -500)
        blueLineSagittal.SetPoint2(0, 0, 500)
        blueLineSagittal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(blueLineSagittal.GetOutput().GetNumberOfCells())
        for c in range(blueLineSagittal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [0, 0, 255])
        blueLineSagittal.GetOutput().GetCellData().SetScalars(colorArray)

        redLineSagittal = vtk.vtkLineSource()
        redLineSagittal.SetPoint1(0, -500, 0)
        redLineSagittal.SetPoint2(0, 500, 0)
        redLineSagittal.Update()

        colorArray = vtk.vtkUnsignedCharArray()
        colorArray.SetNumberOfComponents(3)
        colorArray.SetNumberOfTuples(redLineSagittal.GetOutput().GetNumberOfCells())
        for c in range(redLineSagittal.GetOutput().GetNumberOfCells()):
            colorArray.SetTuple(c, [255, 0, 0])
        redLineSagittal.GetOutput().GetCellData().SetScalars(colorArray)

        linesSagittal = vtk.vtkAppendPolyData()
        linesSagittal.AddInputData(blueLineSagittal.GetOutput())
        linesSagittal.AddInputData(redLineSagittal.GetOutput())
        linesSagittal.Update()

        linesSagittalMapper = vtk.vtkPolyDataMapper()
        linesSagittalMapper.SetInputConnection(linesSagittal.GetOutputPort())

        self.linesSagittalActor = vtk.vtkActor()
        self.linesSagittalActor.SetMapper(linesSagittalMapper)
        self.linesSagittalActor.GetProperty().SetLineWidth(1)
        self.linesSagittalActor.SetOrigin(0, 0, 0)

    def initWidgetsAxialView(self) -> None:
        self.sphereWidgetAxial = vtk.vtkSphereWidget()
        self.sphereWidgetAxial.SetRadius(5)
        self.sphereWidgetAxial.SetInteractor(self.renderWindowInteractorAxial)
        self.sphereWidgetAxial.SetRepresentationToSurface()
        self.sphereWidgetAxial.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        self.sphereWidgetAxial.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetAxial.SetCurrentRenderer(self.rendererAxial)

        self.sphereWidgetInteractionRotateGreenLineAxial = vtk.vtkSphereWidget()
        self.sphereWidgetInteractionRotateGreenLineAxial.SetRadius(5)
        self.sphereWidgetInteractionRotateGreenLineAxial.SetInteractor(self.renderWindowInteractorAxial)
        self.sphereWidgetInteractionRotateGreenLineAxial.SetRepresentationToSurface()
        self.sphereWidgetInteractionRotateGreenLineAxial.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        self.sphereWidgetInteractionRotateGreenLineAxial.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetInteractionRotateGreenLineAxial.SetCurrentRenderer(self.rendererAxial)
    
    def initWidgetsCoronalView(self) -> None:
        self.sphereWidgetCoronal = vtk.vtkSphereWidget()
        self.sphereWidgetCoronal.SetRadius(5)
        self.sphereWidgetCoronal.SetInteractor(self.renderWindowInteractorCoronal)
        self.sphereWidgetCoronal.SetRepresentationToSurface()
        self.sphereWidgetCoronal.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        self.sphereWidgetCoronal.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetCoronal.SetCurrentRenderer(self.rendererCoronal)

    def initWidgetsSagittalView(self) -> None:
        self.sphereWidgetSagittal = vtk.vtkSphereWidget()
        self.sphereWidgetSagittal.SetRadius(5)
        self.sphereWidgetSagittal.SetInteractor(self.renderWindowInteractorSagittal)
        self.sphereWidgetSagittal.SetRepresentationToSurface()
        self.sphereWidgetSagittal.GetSphereProperty().SetColor(self.colors.GetColor3d("Blue"))
        self.sphereWidgetSagittal.GetSelectedSphereProperty().SetOpacity(0)
        self.sphereWidgetSagittal.SetCurrentRenderer(self.rendererSagittal)

    def turnOnWidgets(self) -> None:
        self.sphereWidgetAxial.On()
        self.sphereWidgetInteractionRotateGreenLineAxial.On()
        self.sphereWidgetCoronal.On()
        self.sphereWidgetSagittal.On()

    def turnOffWidgets(self) -> None:
        self.sphereWidgetAxial.Off()
        self.sphereWidgetInteractionRotateGreenLineAxial.Off()
        self.sphereWidgetCoronal.Off()
        self.sphereWidgetSagittal.Off()

    def renderWindows(self) -> None:
        self.renderWindowAxial.Render()
        self.renderWindowCoronal.Render()
        self.renderWindowSagittal.Render()
    
    def setCrosshairPositionAxialView(self, position: Union[List, Tuple]) -> None:
        self.sphereWidgetAxial.SetCenter(position)
        self.linesAxialActor.SetPosition(position)

    def setCrosshairPositionCoronalView(self, position: Union[List, Tuple]) -> None:
        self.sphereWidgetCoronal.SetCenter(position)
        self.linesCoronalActor.SetPosition(position)
    
    def setCrosshairPositionSagittalView(self, position: Union[List, Tuple]) -> None:
        self.sphereWidgetSagittal.SetCenter(position)
        self.linesSagittalActor.SetPosition(position)

    def show3DMPR(self, path_to_dir: str) -> None:
        # Reader
        self.reader.SetDirectoryName(path_to_dir)
        self.reader.Update()
        imageData = self.reader.GetOutput()
        center = imageData.GetCenter()
        (xMin, xMax, yMin, yMax, zMin, zMax) = imageData.GetBounds()

        # Set crosshair position in views
        self.setCrosshairPositionAxialView(center)
        self.setCrosshairPositionCoronalView(center)
        self.setCrosshairPositionSagittalView(center)

        self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter(center[0], (yMax + center[1])/2, center[2])

        # Matrices for axial, coronal, and sagittal view orientations
        # Model matrix = Translation matrix
        self.axial.DeepCopy(
            (1, 0, 0, center[0],
            0, 1, 0, center[1],
            0, 0, 1, center[2],
            0, 0, 0, 1)
        )
        # Model matrix = Translation matrix . Rotation matrix x-axes(90)
        self.coronal.DeepCopy(
            (1, 0, 0, center[0],
            0, 0, 1, center[1],
            0, -1, 0, center[2],
            0, 0, 0, 1)
        )
        # Model matrix = Translation matrix . Rotation matrix x-axes(90) . Rotation matrix y-axes(90)
        self.sagittal.DeepCopy(
            (0, 0, -1, center[0],
            1, 0, 0, center[1],
            0, -1, 0, center[2],
            0, 0, 0, 1)
        )
        
        # Extract a slice in the desired orientation
        self.resliceAxial.SetInputData(imageData)
        self.resliceAxial.SetOutputDimensionality(2)
        self.resliceAxial.SetResliceAxes(self.axial)
        self.resliceAxial.SetInterpolationModeToLinear()

        self.resliceCoronal.SetInputData(imageData)
        self.resliceCoronal.SetOutputDimensionality(2)
        self.resliceCoronal.SetResliceAxes(self.coronal)
        self.resliceCoronal.SetInterpolationModeToLinear()
        
        self.resliceSagittal.SetInputData(imageData)
        self.resliceSagittal.SetOutputDimensionality(2)
        self.resliceSagittal.SetResliceAxes(self.sagittal)
        self.resliceSagittal.SetInterpolationModeToLinear()

        # Display
        self.actorAxial.GetMapper().SetInputConnection(self.resliceAxial.GetOutputPort())
        self.actorCoronal.GetMapper().SetInputConnection(self.resliceCoronal.GetOutputPort())
        self.actorSagittal.GetMapper().SetInputConnection(self.resliceSagittal.GetOutputPort())

        # Set position and rotate in world coordinates
        self.actorAxial.SetUserMatrix(self.axial)
        self.actorCoronal.SetUserMatrix(self.coronal)
        self.actorSagittal.SetUserMatrix(self.sagittal)

        # Set renderers
        self.rendererAxial.AddActor(self.actorAxial)
        self.rendererAxial.AddActor(self.linesAxialActor)
        # The reset camera call is figuring out the frustum bounds based on all the actors present
        # in the viewport.
        self.rendererAxial.ResetCamera()
        self.cameraAxialView.SetPosition(center[0], center[1], 2*zMax)
        self.cameraAxialView.SetFocalPoint(center)
        self.cameraAxialView.SetViewUp(0, 1, 0)
        self.cameraAxialView.SetThickness(2*zMax)
        self.rendererAxial.SetActiveCamera(self.cameraAxialView)

        self.rendererCoronal.AddActor(self.actorCoronal)
        self.rendererCoronal.AddActor(self.linesCoronalActor)
        # The reset camera call is figuring out the frustum bounds based on all the actors present
        # in the viewport.
        self.rendererCoronal.ResetCamera()
        self.cameraCoronalView.SetPosition(center[0], 2*yMax, center[2])
        self.cameraCoronalView.SetFocalPoint(center)
        self.cameraCoronalView.SetViewUp(0, 0, -1)
        self.cameraCoronalView.SetThickness(2*yMax)
        self.rendererCoronal.SetActiveCamera(self.cameraCoronalView)

        self.rendererSagittal.AddActor(self.actorSagittal)
        self.rendererSagittal.AddActor(self.linesSagittalActor)
        # The reset camera call is figuring out the frustum bounds based on all the actors present
        # in the viewport.
        self.rendererSagittal.ResetCamera()
        self.cameraSagittalView.SetPosition(2*xMax, center[1], center[2])
        self.cameraSagittalView.SetFocalPoint(center)
        self.cameraSagittalView.SetViewUp(0, 0, -1)
        self.cameraSagittalView.SetThickness(2*xMax)
        self.rendererSagittal.SetActiveCamera(self.cameraSagittalView)
        self.renderWindows()

        # Create callback function for sphere widget interaction
        currentSphereWidgetCenter = {
            "axial": self.sphereWidgetAxial.GetCenter(),
            "coronal": self.sphereWidgetCoronal.GetCenter(),
            "sagittal": self.sphereWidgetSagittal.GetCenter()
        }
        currentSphereWidgetCenterRotateLinesAxial = {
            "green": self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
        }

        def setupCameraAxialView(newPosition: Union[List, Tuple]) -> None:
            cameraPosition = self.rendererAxial.GetActiveCamera().GetPosition()
            focalPoint = self.rendererAxial.GetActiveCamera().GetFocalPoint()
            reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
            normReverseProjectionVector = vtkmath.Norm(reverseProjectionVector)
            vector = [newPosition[i] - focalPoint[i] for i in range(3)]
            translationInterval = [(vtkmath.Dot(reverseProjectionVector, vector)/math.pow(normReverseProjectionVector, 2))*reverseProjectionVector[i] for i in range(3)]
            self.rendererAxial.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            self.rendererAxial.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

        def setupCameraCoronalView(newPosition: Union[List, Tuple]) -> None:
            cameraPosition = self.rendererCoronal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererCoronal.GetActiveCamera().GetFocalPoint()
            reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
            normReverseProjectionVector = vtkmath.Norm(reverseProjectionVector)
            vector = [newPosition[i] - focalPoint[i] for i in range(3)]
            translationInterval = [(vtkmath.Dot(reverseProjectionVector, vector)/math.pow(normReverseProjectionVector, 2))*reverseProjectionVector[i] for i in range(3)]
            self.rendererCoronal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            self.rendererCoronal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])

        def setupCameraSagittalView(newPosition: Union[List, Tuple]) -> None:
            cameraPosition = self.rendererSagittal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererSagittal.GetActiveCamera().GetFocalPoint()
            reverseProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
            normReverseProjectionVector = vtkmath.Norm(reverseProjectionVector)
            vector = [newPosition[i] - focalPoint[i] for i in range(3)]
            translationInterval = [(vtkmath.Dot(reverseProjectionVector, vector)/math.pow(normReverseProjectionVector, 2))*reverseProjectionVector[i] for i in range(3)]
            self.rendererSagittal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            self.rendererSagittal.GetActiveCamera().SetFocalPoint([focalPoint[i] + translationInterval[i] for i in range(3)])
        
        def interactionEventHandleTranslateLinesAxialView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Set centerline position in axial view
            self.linesAxialActor.SetPosition(newPosition)
            # Set rotation position on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Extract image with new position
            self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)
            # Setup camera in coronal view
            setupCameraCoronalView(newPosition)

            # Extract image with new position
            self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)
            # Setup camera in sagittal view
            setupCameraSagittalView(newPosition)

            currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
            currentSphereWidgetCenter["sagittal"] = self.sphereWidgetCoronal.GetCenter()
            currentSphereWidgetCenter["coronal"] = self.sphereWidgetSagittal.GetCenter()

            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def interactionEventHandleTranslateLinesCoronalView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Set centerline position in coronal view
            self.linesCoronalActor.SetPosition(newPosition)

            # Extract image with new position
            self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            # Setup camera in axial view
            setupCameraAxialView(newPosition)

            # Extract image with new position
            self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)
            # Setup camera in sagittal view
            setupCameraSagittalView(newPosition)

            currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
            currentSphereWidgetCenter["sagittal"] = self.sphereWidgetCoronal.GetCenter()
            currentSphereWidgetCenter["coronal"] = self.sphereWidgetSagittal.GetCenter()

            self.renderWindowAxial.Render()
            self.renderWindowSagittal.Render()

        def interactionEventHandleTranslateLinesSagittalView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Set centerline position in sagittal view
            self.linesSagittalActor.SetPosition(newPosition)

            # Extract image with new position
            self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["sagittal"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            # Setup camera in axial view
            setupCameraAxialView(newPosition)

            # Extract image with new position
            self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)
            # Setup camera in coronal view
            setupCameraCoronalView(newPosition)

            currentSphereWidgetCenter["axial"] = self.sphereWidgetAxial.GetCenter()
            currentSphereWidgetCenter["sagittal"] = self.sphereWidgetCoronal.GetCenter()
            currentSphereWidgetCenter["coronal"] = self.sphereWidgetSagittal.GetCenter()

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()

        def interactionEventHandleRotateGreenLineAxialView(obj, event) -> None:
            newPosition = obj.GetCenter()

            # Calculate rotation angle (degree unit)
            v1 = [currentSphereWidgetCenterRotateLinesAxial["green"][i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            v2 = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            angle = vtkmath.DegreesFromRadians(vtkmath.SignedAngleBetweenVectors(v1, v2, [0, 0, -1]))
            # Rotate lines in axial view
            self.linesAxialActor.RotateZ(-angle)

            # Set elements of rotation matrix (y-axes)
            self.rotationMatrix.SetElement(0, 0, math.cos(math.radians(angle)))
            self.rotationMatrix.SetElement(0, 2, math.sin(math.radians(angle)))
            self.rotationMatrix.SetElement(2, 0, -math.sin(math.radians(angle)))
            self.rotationMatrix.SetElement(2, 2, math.cos(math.radians(angle)))
            
            # Calculate new transform matrix (sagittal view)
            vtk.vtkMatrix4x4.Multiply4x4(self.resliceSagittal.GetResliceAxes(), self.rotationMatrix, self.resultMatrix)
            # Extract image after rotation
            for i in range(4):
                for j in range(4):
                    self.resliceSagittal.GetResliceAxes().SetElement(i, j, self.resultMatrix.GetElement(i, j))
            self.linesSagittalActor.RotateZ(-angle)
            self.rendererSagittal.GetActiveCamera().Azimuth(angle)

            # Calculate new transform matrix (coronal view)
            vtk.vtkMatrix4x4.Multiply4x4(self.resliceCoronal.GetResliceAxes(), self.rotationMatrix, self.resultMatrix)
            # Extract image after rotation
            for i in range(4):
                for j in range(4):
                    self.resliceCoronal.GetResliceAxes().SetElement(i, j, self.resultMatrix.GetElement(i, j))
            self.linesCoronalActor.RotateZ(-angle)
            self.rendererCoronal.GetActiveCamera().Azimuth(angle)

            currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition

            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        self.sphereWidgetAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLinesAxialView)
        self.sphereWidgetInteractionRotateGreenLineAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleRotateGreenLineAxialView)
        
        self.sphereWidgetCoronal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLinesCoronalView)
        
        self.sphereWidgetSagittal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLinesSagittalView)

        def mouseWheelEventHandleAxialView(obj, event) -> None:
            sliceSpacing = self.resliceAxial.GetOutput().GetSpacing()[2]
            cameraPosition = self.rendererAxial.GetActiveCamera().GetPosition()
            focalPoint = self.rendererAxial.GetActiveCamera().GetFocalPoint()
            if event == "MouseWheelForwardEvent":
                # Move the center point that we are slicing through
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                temp = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["axial"][i] + temp[i] for i in range(3)]
                self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            elif event == "MouseWheelBackwardEvent":
                # Move the center point that we are slicing through
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                temp = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["axial"][i] + temp[i] for i in range(3)]
                self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])

            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            # Set camera position in axial view
            cameraPosition = self.rendererAxial.GetActiveCamera().GetPosition()
            self.rendererAxial.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])

            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)

            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def mouseWheelEventHandleCoronalView(obj, event) -> None:
            sliceSpacing = self.resliceCoronal.GetOutput().GetSpacing()[2]
            cameraPosition = self.rendererCoronal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererCoronal.GetActiveCamera().GetFocalPoint()
            if event == "MouseWheelForwardEvent":
                # move the center point that we are slicing through
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                temp = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["coronal"][i] + temp[i] for i in range(3)]
                self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            elif event == "MouseWheelBackwardEvent":
                # move the center point that we are slicing through
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                temp = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["coronal"][i] + temp[i] for i in range(3)]
                self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)
            # Set camera position in coronal view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["coronal"][i] for i in range(3)]
            cameraPosition = self.rendererCoronal.GetActiveCamera().GetPosition()
            self.rendererCoronal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])
            
            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            
            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def mouseWheelEventHandleSagittalView(obj, event) -> None:
            sliceSpacing = self.resliceSagittal.GetOutput().GetSpacing()[2]
            cameraPosition = self.rendererSagittal.GetActiveCamera().GetPosition()
            focalPoint = self.rendererSagittal.GetActiveCamera().GetFocalPoint()
            if event == "MouseWheelForwardEvent":
                # move the center point that we are slicing through
                projectionVector = [focalPoint[i] - cameraPosition[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(projectionVector)
                temp = [(sliceSpacing/norm) * projectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["sagittal"][i] + temp[i] for i in range(3)]
                self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            elif event == "MouseWheelBackwardEvent":
                # move the center point that we are slicing through
                invertProjectionVector = [cameraPosition[i] - focalPoint[i] for i in range(3)]
                norm = vtk.vtkMath.Norm(invertProjectionVector)
                temp = [(sliceSpacing/norm) * invertProjectionVector[i] for i in range(3)]
                newPosition = [currentSphereWidgetCenter["sagittal"][i] + temp[i] for i in range(3)]
                self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
                self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
                self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Set crosshair position in sagittal view
            self.setCrosshairPositionSagittalView(newPosition)
            # Set camera position in sagittal view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["sagittal"][i] for i in range(3)]
            cameraPosition = self.rendererSagittal.GetActiveCamera().GetPosition()
            self.rendererSagittal.GetActiveCamera().SetPosition([cameraPosition[i] + translationInterval[i] for i in range(3)])

            # Set crosshair position in axial view
            self.setCrosshairPositionAxialView(newPosition)
            # Set rotation position on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Set crosshair position in coronal view
            self.setCrosshairPositionCoronalView(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()
        
        self.interactorStyleAxial.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandleAxialView)
        self.interactorStyleAxial.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandleAxialView)
        
        self.interactorStyleCoronal.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandleCoronalView)
        self.interactorStyleCoronal.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandleCoronalView)
        
        self.interactorStyleSagittal.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandleSagittalView)
        self.interactorStyleSagittal.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandleSagittalView)

        # Turn on widgets
        self.turnOnWidgets()

        self.renderWindowInteractorAxial.Start()

if __name__ == "__main__":
    mpr = MPRViewer()
    # 1601 dicoms
    path1 = "D:/workingspace/Python/dicom-data/1.2.840.113619.2.25.4.20352545.1711599249.29"
    # 281 dicoms
    path2 = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    mpr.show3DMPR(path_to_dir=path1)
