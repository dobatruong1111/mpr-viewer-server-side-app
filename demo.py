import vtk

# Tạo vtkLineSource
line_source = vtk.vtkLineSource()
line_source.SetPoint1(-1, 0, 0)  # Điểm đầu của đường thẳng
line_source.SetPoint2(1, 0, 0)   # Điểm cuối của đường thẳng

# Tính trung điểm của đường thẳng
center = [(line_source.GetPoint1()[i] + line_source.GetPoint2()[i]) / 2 for i in range(3)]

# Tạo ma trận biến đổi để xoay quanh trục y 45 độ
transform = vtk.vtkTransform()
# transform.Translate(center)    # Dịch chuyển tới trung điểm của đường thẳng
# transform.RotateY(45)          # Xoay quanh trục y 45 độ
# transform.Translate(-center)   # Dịch chuyển trở lại vị trí ban đầu

# Tạo một vtkTransformPolyDataFilter để áp dụng transform vào đường thẳng
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(line_source.GetOutputPort())
transform_filter.SetTransform(transform)
transform_filter.Update()

# Tạo mapper để hiển thị đường thẳng sau khi xoay
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(transform_filter.GetOutputPort())

# Tạo actor để hiển thị
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Tạo renderer và hiển thị đối tượng
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

# Tạo cửa sổ đồ họa
render_window = vtk.vtkRenderWindow()
render_window.SetSize(800, 600)
render_window.AddRenderer(renderer)

# Tạo cửa sổ đồ họa tương tác
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Hiển thị cửa sổ đồ họa
render_window.Render()
interactor.Start()
