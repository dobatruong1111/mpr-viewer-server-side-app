import vtk

A = vtk.vtkMatrix4x4()
for i in range(4):
    for j in range(4):
        A.SetElement(i, j, 1)

B = vtk.vtkMatrix4x4()
for i in range(4):
    for j in range(4):
        B.SetElement(i, j, 2)

C = vtk.vtkMatrix4x4()

vtk.vtkMatrix4x4().Multiply4x4(A, B, A)

for i in range(4):
    for j in range(4):
        print(A.GetElement(i, j), end=" ")
    print()
