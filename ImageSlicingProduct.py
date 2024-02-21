#!/usr/bin/env python

# This example shows how to load a 3D image into VTK and then reformat
# that image into a different orientation for viewing.  It uses
# vtkImageReslice for reformatting the image, and uses vtkImageActor
# and vtkInteractorStyleImage to display the image.  This InteractorStyle
# forces the camera to stay perpendicular to the XY plane.

import vtk

def main(path_to_dir):
    # Markup by sphere widget
    colors = vtk.vtkNamedColors()
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
    interactorStyle = vtk.vtkInteractorStyleImage()

    # Setup render window
    renderWindow.SetSize(800, 400)
    renderWindow.SetWindowName("MPR Viewer")
    interactorStyle.SetInteractionModeToImageSlicing()
    renderWindowInteractor.SetInteractorStyle(interactorStyle)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Reader
    reader.SetDirectoryName(path_to_dir)
    reader.Update()
    imageData = reader.GetOutput()
    center = imageData.GetCenter()
    bounds = imageData.GetBounds()
    xMax = bounds[1]
    yMax = bounds[3]
    zMax = bounds[5]

    # Setup sphere widget
    sphereWidgetAxial.SetRadius(10)
    sphereWidgetAxial.SetCenter(center)
    sphereWidgetAxial.SetInteractor(renderWindowInteractor)
    sphereWidgetAxial.SetRepresentationToSurface()
    sphereWidgetAxial.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    sphereWidgetCoronal.SetRadius(10)
    sphereWidgetCoronal.SetCenter(center)
    sphereWidgetCoronal.SetInteractor(renderWindowInteractor)
    sphereWidgetCoronal.SetRepresentationToSurface()
    sphereWidgetCoronal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    sphereWidgetSagittal.SetRadius(10)
    sphereWidgetSagittal.SetCenter(center)
    sphereWidgetSagittal.SetInteractor(renderWindowInteractor)
    sphereWidgetSagittal.SetRepresentationToSurface()
    sphereWidgetSagittal.GetSphereProperty().SetColor(colors.GetColor3d("Tomato"))

    # Matrices for axial, coronal, and sagittal view orientations
    # Model matrix = Translation matrix
    axial.DeepCopy((1, 0, 0, center[0],
                    0, 1, 0, center[1],
                    0, 0, 1, center[2],
                    0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix(X)
    coronal.DeepCopy((1, 0, 0, center[0],
                    0, 0, 1, center[1],
                    0,-1, 0, center[2],
                    0, 0, 0, 1))
    # Model matrix = Translation matrix . Rotation matrix(X) . Rotation matrix(Y)
    sagittal.DeepCopy((0, 0,-1, center[0],
                    1, 0, 0, center[1],
                    0,-1, 0, center[2],
                    0, 0, 0, 1))

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
    actorAxial.SetPosition(center)
    actorCoronal.SetPosition(center)
    actorCoronal.RotateX(-90)
    actorSagittal.SetPosition(center)
    actorSagittal.RotateX(-90)
    actorSagittal.RotateY(-90)

    # Renderers
    rendererAxial.AddActor(actorAxial)
    rendererAxial.SetViewport(0, 0, 0.5, 1)
    rendererAxial.SetBackground(0.3, 0.1, 0.1)
    rendererAxial.GetActiveCamera().SetFocalPoint(center)
    rendererAxial.GetActiveCamera().SetPosition(center[0], center[1], zMax)
    rendererAxial.GetActiveCamera().ParallelProjectionOn()
    rendererAxial.GetActiveCamera().SetViewUp(0, 1, 0)
    rendererAxial.ResetCamera()
    sphereWidgetAxial.SetCurrentRenderer(rendererAxial)

    rendererCoronal.AddActor(actorCoronal)
    rendererCoronal.SetViewport(0.5, 0, 1, 0.5)
    rendererCoronal.SetBackground(0.1, 0.3, 0.1)
    rendererCoronal.GetActiveCamera().SetFocalPoint(center)
    rendererCoronal.GetActiveCamera().SetPosition(center[0], yMax, center[2])
    rendererCoronal.GetActiveCamera().ParallelProjectionOn()
    rendererCoronal.GetActiveCamera().SetViewUp(0, 0, -1)
    rendererCoronal.ResetCamera()
    sphereWidgetCoronal.SetCurrentRenderer(rendererCoronal)

    rendererSagittal.AddActor(actorSagittal)
    rendererSagittal.SetViewport(0.5, 0.5, 1, 1)
    rendererSagittal.SetBackground(0.1, 0.1, 0.3)
    rendererSagittal.GetActiveCamera().SetFocalPoint(center)
    rendererSagittal.GetActiveCamera().SetPosition(xMax, center[1], center[2])
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
    def sphereWidgetInteractorCallbackFunction_Axial(obj, event) -> None:
        newPosition = obj.GetCenter()

        matrix = resliceCoronal.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, newPosition[2])
        resliceCoronal.Update()

        matrix = resliceSagittal.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, newPosition[2])
        resliceSagittal.Update()

        renderWindow.Render()

    def sphereWidgetInteractorCallbackFunction_Coronal(obj, event) -> None:
        newPosition = obj.GetCenter()

        matrix = resliceAxial.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, newPosition[2])

        matrix = resliceSagittal.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, newPosition[2])

        renderWindow.Render()

    def sphereWidgetInteractorCallbackFunction_Sagittal(obj, event) -> None:
        newPosition = obj.GetCenter()

        matrix = resliceAxial.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, newPosition[2])

        matrix = resliceCoronal.GetResliceAxes()
        matrix.SetElement(0, 3, newPosition[0])
        matrix.SetElement(1, 3, newPosition[1])
        matrix.SetElement(2, 3, newPosition[2])

        renderWindow.Render()

    sphereWidgetAxial.AddObserver("InteractionEvent", sphereWidgetInteractorCallbackFunction_Axial)
    sphereWidgetCoronal.AddObserver("InteractionEvent", sphereWidgetInteractorCallbackFunction_Coronal)
    sphereWidgetSagittal.AddObserver("InteractionEvent", sphereWidgetInteractorCallbackFunction_Sagittal)

    # Turn on sphere widget
    sphereWidgetAxial.On()
    sphereWidgetCoronal.On()
    sphereWidgetSagittal.On()

    renderWindowInteractor.Start()

if __name__ == "__main__":
    path = "D:/workingspace/Python/dicom-data/220277460 Nguyen Thanh Dat"
    main(path)
