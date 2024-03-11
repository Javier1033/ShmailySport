from django.urls import path
from . import views

urlpatterns = [
    #------------------------Index y login------------------------------------------

    path('', views.login_views, name='index'),
    path('home/', views.home, name='home'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    
    #-----------------------------------Empleado-----------------------------------
    path('empleado/empleado.html/', views.empleado, name='empleado'),
    path('registrarEmpleado/', views.registrarEmpleado, name='registrarEmpleado'),
    path('editarEmpleado/<idEmpleado>/', views.editarEmpleado, name='editarEmpleado'),
    
    #-----------------------------------Satelite-----------------------------------
    path('satelite/satelite.html/', views.satelite, name='satelite'),
    path('registrarSatelite/', views.registrarSatelite, name='registrarSatelite'),
    path('editarSatelite/<idSatelite>/', views.editarSatelite, name='editarSatelite'),
    
    #-----------------------------------Proveedor-----------------------------------
    path('proveedor/proveedor.html/', views.proveedores, name='proveedor'),
    path('registrarProveedor/', views.registrarProveedor, name='registrarProveedor'),
    path('editarProveedor/<idProveedor>/', views.editarProveedor, name='editarProveedor'),
    
    #-----------------------------------Cliente-----------------------------------
    path('cliente/cliente.html/', views.cliente, name='cliente'),
    path('registrarCliente/', views.registrarCliente, name='registrarCliente'),
    path('editarCliente/<idCliente>/', views.editarCliente, name='editarCliente'),
    
    #-----------------------------------FlujoInventario-----------------------------------
    path('flujoInventario/vistaSatelite.html/', views.vistaSatelite, name='vistaSatelite'),
    path('marcar_entregado/<idCorte>/', views.marcar_entregado, name='marcar_entregado'),
    path('flujoInventario/flujoInventario.html/', views.flujoInventario, name='flujoInventario'),
    path('registroFlujo/', views.registroFlujo, name='registroFlujo'),
    path('editarFlujo/<idComprovante>/', views.editarFlujo, name='editarFlujo'),
    path('flujoInventario/registrarCorte.html/', views.registrarCorte, name='registrarCorte'),
    
    #-----------------------------------MateriaPrima-----------------------------------
    path('materiaPrima/materiaPrima.html/', views.materiaPrima, name='materiaPrima'),
    path('registrarMaterial/', views.registrarMaterial, name='registrarMaterial'),
    path('editarMaterial/<idMaterial>/', views.editarMaterial, name='editarMaterial'),
    
    #-----------------------------------Productos-----------------------------------
    path('producto/producto.html/', views.productos, name='producto'),
    path('registrarProducto/', views.registrarProducto, name='registrarProducto'),
    path('editarProducto/<idProducto>/', views.editarProducto, name='editarProducto'),
    
    #-----------------------------------Devoluciones-----------------------------------
    path('devolucion/devolucion.html/', views.devolucion, name='devolucion'),
    path('registrarDevolucion/', views.registrarDevolucion, name='registrarDevolucion'),
    path('editarDevolucion/<idDevolucion>/', views.editarDevolucion, name='editarDevolucion'),
    
    #-----------------------------------Ventas-----------------------------------
    path('ventas/ventas.html/', views.ventas, name='ventas'),
    path('registrarVenta/', views.registrarVenta, name='registrarVenta'),
    path('editarVenta/<idComprovante>/', views.editarVenta, name='editarVenta'),
]