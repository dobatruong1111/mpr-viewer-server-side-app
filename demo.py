import vtk

def main():
    
    colors = vtk.vtkNamedColors()

    # Sphere
    sphere = vtk.vtkSphereSource()
    sphereMapper = vtk.vtkPolyDataMapper()
    sphereActor = vtk.vtkActor()

    sphere.SetRadius(5)
    sphereMapper.SetInputConnection(sphere.GetOutputPort())
    sphereActor.SetMapper(sphereMapper)
    sphereActor.GetProperty().SetColor(colors.GetColor3d("tomato"))
    sphereActor.SetPosition(0, 0, 0)

    # Line
    line = vtk.vtkLineSource()
    transform = vtk.vtkTransform()
    transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
    mapper = vtk.vtkPolyDataMapper()
    actor = vtk.vtkActor()
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()

    # Setup render window
    renderWindow.SetSize(800, 400)
    renderWindow.SetWindowName("Line")
    renderWindowInteractor.SetInteractorStyle(interactorStyle)
    renderWindowInteractor.SetRenderWindow(renderWindow)

    line.SetPoint1(0, 0, 0)
    line.SetPoint1(0, 100, 0)

    transform.RotateX(45)

    transformPolyDataFilter.SetInputConnection(line.GetOutputPort())
    transformPolyDataFilter.SetTransform(transform)
    transformPolyDataFilter.Update()

    mapper.SetInputConnection(transformPolyDataFilter.GetOutputPort())

    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Green"))

    renderer.AddActor(actor)
    renderer.AddActor(sphereActor)
    renderer.SetBackground(0.1, 0.1, 0.3)

    print(line.GetPoint1())
    print(line.GetPoint2())

    renderWindow.AddRenderer(renderer)
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
