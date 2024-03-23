#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkCleanPolyData
)
from vtkmodules.vtkFiltersSources import (
    vtkLineSource,
    vtkConeSource,
    vtkSphereSource
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import vtk

def main():
    colors = vtkNamedColors()
    colors.SetColor('BkgColor', [0.3, 0.2, 0.1, 1.0])

    sphereSource = vtkLineSource()
    sphereSource.SetPoint1(1, 0, 0)
    sphereSource.SetPoint2(-1, 0, 0)
    sphereSource.Update()
    sphereSource = sphereSource.GetOutput()

    colorss = vtk.vtkUnsignedCharArray()
    colorss.SetNumberOfComponents(3)
    colorss.SetNumberOfTuples(sphereSource.GetNumberOfCells())
    for c in range(sphereSource.GetNumberOfCells()):
        colorss.SetTuple(c, [255, 0, 0])
    sphereSource.GetCellData().SetScalars(colorss)

    coneSource = vtkLineSource()
    coneSource.SetPoint1(0, -1, 0)
    coneSource.SetPoint2(0, 1, 0)
    coneSource.Update()
    coneSource = coneSource.GetOutput()

    colorss = vtk.vtkUnsignedCharArray()
    colorss.SetNumberOfComponents(3)
    colorss.SetNumberOfTuples(coneSource.GetNumberOfCells())
    for c in range(coneSource.GetNumberOfCells()):
        colorss.SetTuple(c, [0, 255, 0])
    coneSource.GetCellData().SetScalars(colorss)

    # Append the two meshes
    appendFilter = vtkAppendPolyData()
    appendFilter.AddInputData(sphereSource)
    appendFilter.AddInputData(coneSource)
    appendFilter.Update()

    # Remove any duplicate points.
    # cleanFilter = vtkCleanPolyData()
    # cleanFilter.SetInputConnection(appendFilter.GetOutputPort())
    # cleanFilter.Update()

    connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
    connectivityFilter.SetInputConnection(appendFilter.GetOutputPort())
    connectivityFilter.SetExtractionModeToAllRegions()
    connectivityFilter.Update()

    # Create a mapper and actor
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(connectivityFilter.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetOrigin(0, 0, 0)

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderer.SetBackground(colors.GetColor3d('deep_ochre'))
    renderer.GetActiveCamera().Zoom(0.9)
    renderer.AddActor(actor)

    renderWindow = vtkRenderWindow()
    renderWindow.SetWindowName('CombinePolyData')
    renderWindow.AddRenderer(renderer)
    renderWindow.Render()

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Start()

if __name__ == '__main__':
    main()
