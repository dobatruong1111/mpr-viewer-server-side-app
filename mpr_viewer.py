import vtk
from vtkmodules.vtkCommonCore import vtkCommand
import math
vtkmath = vtk.vtkMath()

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

class MPRViewer(object):
    def __init__(self) -> None:
        self.colors = vtk.vtkNamedColors()
        self.initialize()
        self.initCenterlineAxialView()
        self.initCenterlineCoronalView()
        self.initCenterlineSagittalView()
        self.initWidgets()

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
        self.interactorStyleCoronal = vtk.vtkInteractorStyleImage()
        self.interactorStyleSagittal = vtk.vtkInteractorStyleImage()
        self.renderWindowInteractorAxial = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractorCoronal = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractorSagittal = vtk.vtkRenderWindowInteractor()

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

        self.renderWindowCoronal.SetSize(400, 400)
        self.renderWindowCoronal.SetWindowName("Coronal view")
        self.renderWindowCoronal.SetInteractor(self.renderWindowInteractorCoronal)
        self.renderWindowCoronal.SetPosition(400, 0)

        self.renderWindowSagittal.SetSize(400, 400)
        self.renderWindowSagittal.SetWindowName("Sagittal view")
        self.renderWindowSagittal.SetInteractor(self.renderWindowInteractorSagittal)
        self.renderWindowSagittal.SetPosition(800, 0)

        # Initialize rotation matrix (y-axes)
        self.rotationMatrix.DeepCopy(
            (math.cos(math.radians(0)), 0, math.sin(math.radians(0)), 0, 
            0, 1, 0, 0, 
            -math.sin(math.radians(0)), 0, math.cos(math.radians(0)), 0, 
            0, 0, 0, 1)
        )
    
    def initCenterlineAxialView(self) -> None:
        self.greenLineAxial = vtk.vtkLineSource()
        self.greenLineAxialMapper = vtk.vtkPolyDataMapper()
        self.greenLineAxialActor = vtk.vtkActor()
        self.greenLineAxialMapper.SetInputConnection(self.greenLineAxial.GetOutputPort())
        self.greenLineAxialActor.SetMapper(self.greenLineAxialMapper)
        self.greenLineAxialActor.GetProperty().SetColor(self.colors.GetColor3d("Green"))
        self.greenLineAxialActor.GetProperty().SetLineWidth(1.5)

        self.blueLineAxial = vtk.vtkLineSource()
        self.blueLineAxialMapper = vtk.vtkPolyDataMapper()
        self.blueLineAxialActor = vtk.vtkActor()
        self.blueLineAxialMapper.SetInputConnection(self.blueLineAxial.GetOutputPort())
        self.blueLineAxialActor.SetMapper(self.blueLineAxialMapper)
        self.blueLineAxialActor.GetProperty().SetColor(self.colors.GetColor3d("Blue"))
        self.blueLineAxialActor.GetProperty().SetLineWidth(1.5)
    
    def initCenterlineCoronalView(self) -> None:
        self.greenLineCoronal = vtk.vtkLineSource()
        self.greenLineCoronalMapper = vtk.vtkPolyDataMapper()
        self.greenLineCoronalActor = vtk.vtkActor()
        self.greenLineCoronalMapper.SetInputConnection(self.greenLineCoronal.GetOutputPort())
        self.greenLineCoronalActor.SetMapper(self.greenLineCoronalMapper)
        self.greenLineCoronalActor.GetProperty().SetColor(self.colors.GetColor3d("Green"))
        self.greenLineCoronalActor.GetProperty().SetLineWidth(1.5)

        self.redLineCoronal = vtk.vtkLineSource()
        self.redLineCoronalMapper = vtk.vtkPolyDataMapper()
        self.redLineCoronalActor = vtk.vtkActor()
        self.redLineCoronalMapper.SetInputConnection(self.redLineCoronal.GetOutputPort())
        self.redLineCoronalActor.SetMapper(self.redLineCoronalMapper)
        self.redLineCoronalActor.GetProperty().SetColor(self.colors.GetColor3d("Red"))
        self.redLineCoronalActor.GetProperty().SetLineWidth(1.5)

    def initCenterlineSagittalView(self) -> None:
        self.blueLineSagittal = vtk.vtkLineSource()
        self.blueLineSagittalMapper = vtk.vtkPolyDataMapper()
        self.blueLineSagittalActor = vtk.vtkActor()
        self.blueLineSagittalMapper.SetInputConnection(self.blueLineSagittal.GetOutputPort())
        self.blueLineSagittalActor.SetMapper(self.blueLineSagittalMapper)
        self.blueLineSagittalActor.GetProperty().SetColor(self.colors.GetColor3d("Blue"))
        self.blueLineSagittalActor.GetProperty().SetLineWidth(1.5)

        self.redLineSagittal = vtk.vtkLineSource()
        self.redLineSagittalMapper = vtk.vtkPolyDataMapper()
        self.redLineSagittalActor = vtk.vtkActor()
        self.redLineSagittalMapper.SetInputConnection(self.redLineSagittal.GetOutputPort())
        self.redLineSagittalActor.SetMapper(self.redLineSagittalMapper)
        self.redLineSagittalActor.GetProperty().SetColor(self.colors.GetColor3d("Red"))
        self.redLineSagittalActor.GetProperty().SetLineWidth(1.5)

    def initWidgets(self) -> None:
        self.sphereWidgetAxial = vtk.vtkSphereWidget()
        self.sphereWidgetAxial.SetRadius(8)
        self.sphereWidgetAxial.SetInteractor(self.renderWindowInteractorAxial)
        self.sphereWidgetAxial.SetRepresentationToSurface()
        self.sphereWidgetAxial.GetSphereProperty().SetColor(self.colors.GetColor3d("Tomato"))
        self.sphereWidgetAxial.GetSelectedSphereProperty().SetOpacity(0)

        self.sphereWidgetInteractionRotateGreenLineAxial = vtk.vtkSphereWidget()
        self.sphereWidgetInteractionRotateGreenLineAxial.SetRadius(8)
        self.sphereWidgetInteractionRotateGreenLineAxial.SetInteractor(self.renderWindowInteractorAxial)
        self.sphereWidgetInteractionRotateGreenLineAxial.SetRepresentationToSurface()
        self.sphereWidgetInteractionRotateGreenLineAxial.GetSphereProperty().SetColor(self.colors.GetColor3d("Green"))
        self.sphereWidgetInteractionRotateGreenLineAxial.GetSelectedSphereProperty().SetOpacity(0)

        self.sphereWidgetCoronal = vtk.vtkSphereWidget()
        self.sphereWidgetCoronal.SetRadius(8)
        self.sphereWidgetCoronal.SetInteractor(self.renderWindowInteractorCoronal)
        self.sphereWidgetCoronal.SetRepresentationToSurface()
        self.sphereWidgetCoronal.GetSphereProperty().SetColor(self.colors.GetColor3d("Tomato"))
        self.sphereWidgetCoronal.GetSelectedSphereProperty().SetOpacity(0)

        self.sphereWidgetSagittal = vtk.vtkSphereWidget()
        self.sphereWidgetSagittal.SetRadius(8)
        self.sphereWidgetSagittal.SetInteractor(self.renderWindowInteractorSagittal)
        self.sphereWidgetSagittal.SetRepresentationToSurface()
        self.sphereWidgetSagittal.GetSphereProperty().SetColor(self.colors.GetColor3d("Tomato"))
        self.sphereWidgetSagittal.GetSelectedSphereProperty().SetOpacity(0)
    
    def showMPR(self, path_to_dir: str) -> None:
        # Reader
        self.reader.SetDirectoryName(path_to_dir)
        self.reader.Update()
        imageData = self.reader.GetOutput()
        center = imageData.GetCenter()
        (xMin, xMax, yMin, yMax, zMin, zMax) = imageData.GetBounds()

        # Set position of widgets
        self.sphereWidgetAxial.SetCenter(center)
        self.sphereWidgetCoronal.SetCenter(center)
        self.sphereWidgetSagittal.SetCenter(center)

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

        # Display dicom
        self.actorAxial.GetMapper().SetInputConnection(self.resliceAxial.GetOutputPort())
        self.actorCoronal.GetMapper().SetInputConnection(self.resliceCoronal.GetOutputPort())
        self.actorSagittal.GetMapper().SetInputConnection(self.resliceSagittal.GetOutputPort())

        # Set position and rotate dicom
        self.actorAxial.SetUserMatrix(self.axial)
        self.actorCoronal.SetUserMatrix(self.coronal)
        self.actorSagittal.SetUserMatrix(self.sagittal)

        # Renderers
        self.rendererAxial.SetBackground(0.3, 0.1, 0.1)
        self.rendererAxial.AddActor(self.actorAxial)
        self.rendererAxial.AddActor(self.greenLineAxialActor)
        self.rendererAxial.AddActor(self.blueLineAxialActor)
        self.cameraAxialView.SetPosition(center[0], center[1], 3*zMax)
        self.cameraAxialView.SetFocalPoint(center)
        self.cameraAxialView.SetViewUp(0, 1, 0)
        self.cameraAxialView.SetThickness(3*zMax)
        self.rendererAxial.SetActiveCamera(self.cameraAxialView)

        self.sphereWidgetAxial.SetCurrentRenderer(self.rendererAxial)
        self.sphereWidgetInteractionRotateGreenLineAxial.SetCurrentRenderer(self.rendererAxial)

        self.rendererCoronal.SetBackground(0.1, 0.3, 0.1)
        self.rendererCoronal.AddActor(self.actorCoronal)
        self.rendererCoronal.AddActor(self.greenLineCoronalActor)
        self.rendererCoronal.AddActor(self.redLineCoronalActor)
        self.cameraCoronalView.SetPosition(center[0], 3*yMax, center[2])
        self.cameraCoronalView.SetFocalPoint(center)
        self.cameraCoronalView.SetViewUp(0, 0, -1)
        self.cameraCoronalView.SetThickness(3*yMax)
        self.rendererCoronal.SetActiveCamera(self.cameraCoronalView)

        self.sphereWidgetCoronal.SetCurrentRenderer(self.rendererCoronal)

        self.rendererSagittal.SetBackground(0.1, 0.1, 0.3)
        self.rendererSagittal.AddActor(self.actorSagittal)
        self.rendererSagittal.AddActor(self.blueLineSagittalActor)
        self.rendererSagittal.AddActor(self.redLineSagittalActor)
        self.cameraSagittalView.SetPosition(3*xMax, center[1], center[2])
        self.cameraSagittalView.SetFocalPoint(center)
        self.cameraSagittalView.SetViewUp(0, 0, -1)
        self.cameraSagittalView.SetThickness(3.5*xMax)
        self.rendererSagittal.SetActiveCamera(self.cameraSagittalView)

        self.sphereWidgetSagittal.SetCurrentRenderer(self.rendererSagittal)

        # Render window
        self.renderWindowAxial.AddRenderer(self.rendererAxial)
        self.renderWindowAxial.Render()

        self.renderWindowCoronal.AddRenderer(self.rendererCoronal)
        self.renderWindowCoronal.Render()

        self.renderWindowSagittal.AddRenderer(self.rendererSagittal)
        self.renderWindowSagittal.Render()

        # Set lines in axial view
        self.greenLineAxial.SetPoint1(0, yMax, 0)
        self.greenLineAxial.SetPoint2(0, -yMax, 0)
        self.greenLineAxialActor.SetOrigin(0, 0, 0)
        self.greenLineAxialActor.SetPosition(center)
        self.blueLineAxial.SetPoint1(-xMax, 0, 0)
        self.blueLineAxial.SetPoint2(xMax, 0, 0)
        self.blueLineAxialActor.SetOrigin(0, 0, 0)
        self.blueLineAxialActor.SetPosition(center)

        self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter(center[0], (yMax + center[1])/2, center[2])

        # Set lines in coronal view
        self.greenLineCoronal.SetPoint1(0, 0, -zMax)
        self.greenLineCoronal.SetPoint2(0, 0, zMax)
        self.greenLineCoronalActor.SetOrigin(0, 0, 0)
        self.greenLineCoronalActor.SetPosition(center)
        self.redLineCoronal.SetPoint1(-xMax, 0, 0)
        self.redLineCoronal.SetPoint2(xMax, 0, 0)
        self.redLineCoronalActor.SetOrigin(0, 0, 0)
        self.redLineCoronalActor.SetPosition(center)

        # Set lines in sagittal view
        self.blueLineSagittal.SetPoint1(0, 0, -zMax)
        self.blueLineSagittal.SetPoint2(0, 0, zMax)
        self.blueLineSagittalActor.SetOrigin(0, 0, 0)
        self.blueLineSagittalActor.SetPosition(center)
        self.redLineSagittal.SetPoint1(0, -yMax, 0)
        self.redLineSagittal.SetPoint2(0, yMax, 0)
        self.redLineSagittalActor.SetOrigin(0, 0, 0)
        self.redLineSagittalActor.SetPosition(center)

        # Create callback function for sphere widget interaction
        currentSphereWidgetCenter = {
            "axial": self.sphereWidgetAxial.GetCenter(),
            "coronal": self.sphereWidgetCoronal.GetCenter(),
            "sagittal": self.sphereWidgetSagittal.GetCenter()
        }
        currentSphereWidgetCenterRotateLinesAxial = {
            "green": self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
        }
        def interactionEventHandleTranslateLines_AxialView(obj, event) -> None:
            newPosition = obj.GetCenter()
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]

            # Translate lines in axial view
            self.greenLineAxialActor.SetPosition(newPosition)
            self.blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Translate sphere widget in sagittal view
            self.sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagital view
            self.blueLineSagittalActor.SetPosition(newPosition)
            self.redLineSagittalActor.SetPosition(newPosition)

            self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Translate sphere widget in coronal view
            self.sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            self.greenLineCoronalActor.SetPosition(newPosition)
            self.redLineCoronalActor.SetPosition(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def interactionEventHandleTranslateLines_CoronalView(obj, event) -> None:
            newPosition = obj.GetCenter()
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["coronal"][i] for i in range(3)]

            # Translate lines in coronal view
            self.greenLineCoronalActor.SetPosition(newPosition)
            self.redLineCoronalActor.SetPosition(newPosition)

            self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Translate sphere widget in axial view
            self.sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            self.greenLineAxialActor.SetPosition(newPosition)
            self.blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            
            self.resliceSagittal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceSagittal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceSagittal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Translate sphere widget in sagittal view
            self.sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            self.blueLineSagittalActor.SetPosition(newPosition)
            self.redLineSagittalActor.SetPosition(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def interactionEventHandleTranslateLines_SagittalView(obj, event) -> None:
            newPosition = obj.GetCenter()
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["sagittal"][i] for i in range(3)]

            # Translate lines in sagittal view
            self.blueLineSagittalActor.SetPosition(newPosition)
            self.redLineSagittalActor.SetPosition(newPosition)

            self.resliceAxial.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceAxial.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceAxial.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Translate sphere widget in axial view
            self.sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            self.greenLineAxialActor.SetPosition(newPosition)
            self.blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([currentSphereWidgetCenterRotateLinesAxial["green"][i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            self.resliceCoronal.GetResliceAxes().SetElement(0, 3, newPosition[0])
            self.resliceCoronal.GetResliceAxes().SetElement(1, 3, newPosition[1])
            self.resliceCoronal.GetResliceAxes().SetElement(2, 3, newPosition[2])
            # Translate sphere widget in coronal view
            self.sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            self.greenLineCoronalActor.SetPosition(newPosition)
            self.redLineCoronalActor.SetPosition(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def interactionEventHandleRotateGreenLine_AxialView(obj, event) -> None:
            newPosition = obj.GetCenter()
            # Calculate rotation angle (degree unit)
            angle = calcAngleBetweenTwoVectors(currentSphereWidgetCenterRotateLinesAxial["green"], currentSphereWidgetCenter["axial"], newPosition)

            # Rotate lines in axial view
            self.greenLineAxialActor.RotateZ(-angle)
            self.blueLineAxialActor.RotateZ(-angle)

            # Set elements of rotation matrix (y-axes)
            self.rotationMatrix.SetElement(0, 0, math.cos(math.radians(angle)))
            self.rotationMatrix.SetElement(0, 2, math.sin(math.radians(angle)))
            self.rotationMatrix.SetElement(2, 0, -math.sin(math.radians(angle)))
            self.rotationMatrix.SetElement(2, 2, math.cos(math.radians(angle)))
            
            # Set transform matrix (sagittal view)
            vtk.vtkMatrix4x4.Multiply4x4(self.resliceSagittal.GetResliceAxes(), self.rotationMatrix, self.resultMatrix)
            for i in range(4):
                for j in range(4):
                    self.resliceSagittal.GetResliceAxes().SetElement(i, j, self.resultMatrix.GetElement(i, j))
            self.redLineSagittalActor.RotateZ(-angle)
            self.rendererSagittal.GetActiveCamera().Azimuth(angle)

            # Set transform matrix (coronal view)
            vtk.vtkMatrix4x4.Multiply4x4(self.resliceCoronal.GetResliceAxes(), self.rotationMatrix, self.resultMatrix)
            for i in range(4):
                for j in range(4):
                    self.resliceCoronal.GetResliceAxes().SetElement(i, j, self.resultMatrix.GetElement(i, j))
            self.redLineCoronalActor.RotateZ(-angle)
            self.rendererCoronal.GetActiveCamera().Azimuth(angle)

            currentSphereWidgetCenterRotateLinesAxial["green"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        self.sphereWidgetAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLines_AxialView)
        self.sphereWidgetInteractionRotateGreenLineAxial.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleRotateGreenLine_AxialView)
        self.sphereWidgetCoronal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLines_CoronalView)
        self.sphereWidgetSagittal.AddObserver(vtkCommand.InteractionEvent, interactionEventHandleTranslateLines_SagittalView)

        def mouseWheelEventHandle_AxialView(obj, event) -> None:
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
            # Translate sphere widget in axial view
            self.sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            self.greenLineAxialActor.SetPosition(newPosition)
            self.blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in coronal view
            self.sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            self.greenLineCoronalActor.SetPosition(newPosition)
            self.redLineCoronalActor.SetPosition(newPosition)

            # Translate sphere widget in sagittal view
            self.sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            self.blueLineSagittalActor.SetPosition(newPosition)
            self.redLineSagittalActor.SetPosition(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def mouseWheelEventHandle_CoronalView(obj, event) -> None:
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
            # Translate sphere widget in coronal view
            self.sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            self.greenLineCoronalActor.SetPosition(newPosition)
            self.redLineCoronalActor.SetPosition(newPosition)
            
            # Translate sphere widget in axial view
            self.sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            self.greenLineAxialActor.SetPosition(newPosition)
            self.blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()
            
            # Translate sphere widget in sagittal view
            self.sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            self.blueLineSagittalActor.SetPosition(newPosition)
            self.redLineSagittalActor.SetPosition(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()

        def mouseWheelEventHandle_SagittalView(obj, event) -> None:
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
            # Translate sphere widget in sagittal view
            self.sphereWidgetSagittal.SetCenter(newPosition)
            # Translate lines in sagittal view
            self.blueLineSagittalActor.SetPosition(newPosition)
            self.redLineSagittalActor.SetPosition(newPosition)

            # Translate sphere widget in axial view
            self.sphereWidgetAxial.SetCenter(newPosition)
            # Translate lines in axial view
            self.greenLineAxialActor.SetPosition(newPosition)
            self.blueLineAxialActor.SetPosition(newPosition)
            # Translate a rotation point on green line in axial view
            translationInterval = [newPosition[i] - currentSphereWidgetCenter["axial"][i] for i in range(3)]
            self.sphereWidgetInteractionRotateGreenLineAxial.SetCenter([self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()[i] + translationInterval[i] for i in range(3)])
            currentSphereWidgetCenterRotateLinesAxial["green"] = self.sphereWidgetInteractionRotateGreenLineAxial.GetCenter()

            # Translate sphere widget in coronal view
            self.sphereWidgetCoronal.SetCenter(newPosition)
            # Translate lines in coronal view
            self.greenLineCoronalActor.SetPosition(newPosition)
            self.redLineCoronalActor.SetPosition(newPosition)

            currentSphereWidgetCenter["axial"] = newPosition
            currentSphereWidgetCenter["coronal"] = newPosition
            currentSphereWidgetCenter["sagittal"] = newPosition

            self.renderWindowAxial.Render()
            self.renderWindowCoronal.Render()
            self.renderWindowSagittal.Render()
        
        self.interactorStyleAxial.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandle_AxialView)
        self.interactorStyleAxial.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandle_AxialView)
        self.interactorStyleCoronal.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandle_CoronalView)
        self.interactorStyleCoronal.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandle_CoronalView)
        self.interactorStyleSagittal.AddObserver(vtkCommand.MouseWheelForwardEvent, mouseWheelEventHandle_SagittalView)
        self.interactorStyleSagittal.AddObserver(vtkCommand.MouseWheelBackwardEvent, mouseWheelEventHandle_SagittalView)

        # Turn on widgets
        self.sphereWidgetAxial.On()
        self.sphereWidgetInteractionRotateGreenLineAxial.On()
        self.sphereWidgetCoronal.On()
        self.sphereWidgetSagittal.On()

        self.renderWindowInteractorAxial.Start()

if __name__ == "__main__":
    mpr = MPRViewer()
    mpr.showMPR(path_to_dir="D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat")
