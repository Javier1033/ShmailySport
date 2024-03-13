from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import *


# Create your views here.

#--------------------------------Index y Login--------------------------------------
def login_views(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        doc_empleado = request.POST.get('documento')

        if not doc_empleado.isdigit():
            messages.error(request, "Credenciales incorrectas.")
            return redirect('index')

        contrasena = request.POST.get('contrasena')

        # Buscar el empleado por el documento proporcionado
        try:
            empleado = Empleado.objects.get(docEmpleado=doc_empleado)
        except Empleado.DoesNotExist:
            messages.error(request, "Empleado no encontrado.")
            return redirect('index')

        # Obtener la contraseña del cargo del empleado
        contrasena_empleado = empleado.contraseña

        # Verificar la contraseña
        if check_password(contrasena, contrasena_empleado):
            # Almacenar el documento del empleado en la sesión
            request.session['documento'] = doc_empleado
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas.")
            return redirect('index')

    # Renderizar el formulario de inicio de sesión
    return render(request, 'index.html')

def home(request):
    if 'documento' in request.session:
        doc_empleado = request.session['documento']
        try:
            empleado = Empleado.objects.get(docEmpleado=doc_empleado)
            persona = empleado.docEmpleado
            nombre_completo = f"{persona.nombres} {persona.apellidos}"
            cargo_empleado = empleado.cargo.cargo
            return render(request, 'home.html', {'nombre_completo': nombre_completo, 'cargo_empleado': cargo_empleado})
        except Empleado.DoesNotExist:
            messages.error(request, "No tienes permiso para acceder a este perfil.")
            return redirect('index')
    else:
        return redirect('index')

def cerrar_sesion(request):
    if 'documento' in request.session:
        del request.session['documento']
        messages.info(request, "¡Sesión cerrada correctamente!")
    return redirect('index')


#-------------------------------------Empleado-------------------------------------
def empleado(request):
    empleados_activos = Empleado.objects.filter(activo=True)
    empleados_inactivos = Empleado.objects.filter(activo=False)
    persona = Personas.objects.all()
    arls = Arl.objects.all()
    epss = Eps.objects.all()
    cargos = Cargo.objects.all()
    
    return render(request, 'empleado/empleado.html', {"empleados_activos": empleados_activos, "empleados_inactivos": empleados_inactivos, "persona": persona, "arls": arls, "epss": epss, "cargos": cargos})

def registrarEmpleado(request):
    if request.method == 'POST':
        form = RegistroEmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleado') 
    else:
        form = RegistroEmpleadoForm()
    
    return render(request, 'empleado/registrarEmpleado.html', {'form': form})

def editarEmpleado(request, idEmpleado):
    empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
    if request.method == 'POST':
        form = EditarEmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('empleado') 
    else:
        form = EditarEmpleadoForm(instance=empleado, empleado=empleado)
    
    return render(request, 'empleado/editarEmpleado.html', {'form': form, 'empleado': empleado})

#-------------------------------------Satelite-------------------------------------
def satelite(request):
    satelite_activo = Satelites.objects.filter(activo=True)
    satelite_inactivo = Satelites.objects.filter(activo=False)
    persona = Personas.objects.all()
    
    return render(request, 'satelite/satelite.html', {"satelite_activo": satelite_activo, "satelite_inactivo": satelite_inactivo, "persona": persona})

def registrarSatelite(request):
    if request.method == 'POST':
        form = RegistroSateliteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('satelite') 
    else:
        form = RegistroSateliteForm()
    
    return render(request, 'satelite/registrarSatelite.html', {'form': form})

def editarSatelite(request, idSatelite):
    satelite = get_object_or_404(Satelites, idSatelite=idSatelite)
    if request.method == 'POST':
        form = EditarSateliteForm(request.POST, instance=satelite)
        if form.is_valid():
            form.save()
            return redirect('satelite') 
    else:
        form = EditarSateliteForm(instance=satelite, satelite=satelite)
    
    return render(request, 'satelite/editarSatelite.html', {'form': form, 'satelite': satelite})

#-------------------------------------Proveedor-------------------------------------
def proveedores(request):
    proveedores_activos = Proveedor.objects.filter(activo=True)
    proveedores_inactivos = Proveedor.objects.filter(activo=False)
    persona = Personas.objects.all()
    
    return render(request, 'proveedor/proveedor.html', {"proveedores_activos": proveedores_activos, "proveedores_inactivos": proveedores_inactivos, "persona": persona})

def registrarProveedor(request):
    if request.method == 'POST':
        form = RegistroProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor') 
    else:
        form = RegistroProveedorForm()
    
    return render(request, 'proveedor/registrarProveedor.html', {'form': form})

def editarProveedor(request, idProveedor):
    proveedores = get_object_or_404(Proveedor, idProveedor=idProveedor)
    if request.method == 'POST':
        form = EditarProveedorForm(request.POST, instance=proveedores)
        if form.is_valid():
            form.save()
            return redirect('proveedor') 
    else:
        form = EditarProveedorForm(instance=proveedores, proveedores=proveedores)
    
    return render(request, 'proveedor/editarProveedor.html', {'form': form, 'proveedores': proveedores})

#-------------------------------------Cliente-------------------------------------
def cliente(request):
    clientes_activos = Cliente.objects.filter(activo=True)
    clientes_inactivos = Cliente.objects.filter(activo=False)
    persona = Personas.objects.all()
    
    return render(request, 'cliente/cliente.html', {"clientes_activos": clientes_activos, "clientes_inactivos": clientes_inactivos, "persona": persona})

def registrarCliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente') 
    else:
        form = RegistroClienteForm()
    
    return render(request, 'cliente/registrarCliente.html', {'form': form})

def editarCliente(request, idCliente):
    clientes = get_object_or_404(Cliente, idCliente=idCliente)
    if request.method == 'POST':
        form = EditarClienteForm(request.POST, instance=clientes)
        if form.is_valid():
            form.save()
            return redirect('cliente') 
    else:
        form = EditarClienteForm(instance=clientes, clientes=clientes)
    
    return render(request, 'cliente/editarCliente.html', {'form': form, 'clientes': clientes})

#-------------------------------------SatelitesCorte-------------------------------------

def vistaSatelite(request):
    satelites = Satelites.objects.all()
    satelite_seleccionado = None
    cortes_entregados = None
    cortes_no_entregados = None
    
    if request.method == 'POST':
        idSatelite = request.POST.get('satelite')
        satelite_seleccionado = Satelites.objects.get(idSatelite=idSatelite)
        cortes = Corte.objects.filter(satelite=satelite_seleccionado)
        cortes_entregados = cortes.filter(entregado=True)
        cortes_no_entregados = cortes.filter(entregado=False)
    
    return render(request, 'flujoInventario/vistaSatelite.html', {'satelites': satelites, 'satelite_seleccionado': satelite_seleccionado, 'cortes_entregados': cortes_entregados, 'cortes_no_entregados': cortes_no_entregados})

def marcar_entregado(request, idCorte):
    corte = Corte.objects.get(pk=idCorte)
    corte.entregado = True
    corte.save()
    return redirect('vistaSatelite')

#-------------------------------------FlujoInventario-------------------------------------
def flujoInventario(request):
    flujoInventario = FlujoInventario.objects.all()
    empleados = Empleado.objects.all()
    proveedores = Proveedor.objects.all()
    material = MateriaPrima.objects.all()
    satelite = Satelites.objects.all()
    cortes = Corte.objects.all()
    
    if not messages.get_messages(request):
        messages.success(request, 'Flujos Listados')
        
    return render(request, 'flujoInventario/FlujoInventario.html', {"flujoInventario": flujoInventario, "empleados": empleados, "proveedores": proveedores, "material": material, "satelite": satelite, "cortes": cortes})

def registroFlujo(request):
    if request.method == 'POST':
        form = FlujoInventarioForm(request.POST)
        if form.is_valid():
            flujo_inventario = form.save(commit=False)
            flujo = flujo_inventario.flujo

            if flujo == 'entrada':  
                flujo_inventario.save()
                if flujo_inventario.flujoProducto:
                    producto = flujo_inventario.flujoProducto
                    producto.cantidadProducto += flujo_inventario.cantidadFlujo
                    producto.save()
                elif flujo_inventario.materialFlu:
                    material = flujo_inventario.materialFlu
                    material.cantidadMaterial += flujo_inventario.cantidadFlujo
                    material.save()
            elif flujo == 'salida':  
                flujo_inventario.save()
                if flujo_inventario.flujoProducto:
                    producto = flujo_inventario.flujoProducto
                    producto.cantidadProducto -= flujo_inventario.cantidadFlujo
                    producto.save()
                elif flujo_inventario.materialFlu:
                    material = flujo_inventario.materialFlu
                    material.cantidadMaterial -= flujo_inventario.cantidadFlujo
                    material.save()

            if flujo_inventario.flujoCorte and flujo_inventario.flujoSatelite:
                flujo_inventario.flujoCorte.satelite = flujo_inventario.flujoSatelite
                flujo_inventario.flujoCorte.save()

            return redirect('flujoInventario')  # Redirigir a la página de flujo de inventario después de guardar

    else:
        form = FlujoInventarioForm()

    return render(request, 'flujoInventario/registroFlujo.html', {'form': form})

def editarFlujo(request, idComprovante):
    flujo = FlujoInventario.objects.get(idComprovante=idComprovante)
    if request.method == 'POST':
        form = FlujoInventarioEditForm(request.POST, instance=flujo)
        formset = DetalleFlujoInventarioEditFormSet(request.POST, instance=flujo)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('flujoInventario')
    else:
        form = FlujoInventarioEditForm(instance=flujo)
        formset = DetalleFlujoInventarioEditFormSet(instance=flujo)
    return render(request, 'flujoInventario/editarFlujo.html', {'form': form, 'formset': formset})

def registrarCorte(request):
    if request.method == 'POST':
        form = CorteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registroFlujo')  
    else:
        cortes_no_entregados = Corte.objects.filter(entregado=False)
        form = CorteForm(initial={'productoCorte': cortes_no_entregados})
    return render(request, 'flujoInventario/registrarCorte.html', {'form': form})

#-------------------------------------MateriaPrima-------------------------------------
def materiaPrima(request):
    materias_primas_activas = MateriaPrima.objects.filter(activo=True)
    materias_primas_inactivas = MateriaPrima.objects.filter(activo=False)
    return render(request, 'materiaPrima/materiaPrima.html', {'materias_primas_activas': materias_primas_activas, 'materias_primas_inactivas': materias_primas_inactivas})

def registrarMaterial(request):
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materiaPrima')  # Redirige a la página de lista de materias primas después de guardar
    else:
        form = MateriaPrimaForm()
    return render(request, 'materiaPrima/registrarMaterial.html', {'form': form})

def editarMaterial(request, idMaterial):
    materia_prima = get_object_or_404(MateriaPrima, idMaterial=idMaterial)
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST, instance=materia_prima)
        if form.is_valid():
            form.update(materia_prima)
            return redirect('materiaPrima')
    else:
        form = MateriaPrimaForm(instance=materia_prima)
    return render(request, 'materiaPrima/editarMaterial.html', {'form': form})

#-------------------------------------Productos-------------------------------------
def productos(request):
    productos_activos = Producto.objects.filter(activo=True)
    productos_inactivos = Producto.objects.filter(activo=False)
    return render(request, 'producto/producto.html', {'productos_activos': productos_activos, 'productos_inactivos': productos_inactivos})

def registrarProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto')  # Redirige a la página de lista de productos después de guardar
    else:
        form = ProductoForm()
    return render(request, 'producto/registrarProducto.html', {'form': form})

def editarProducto(request, idProducto):
    producto = get_object_or_404(Producto, idProducto=idProducto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto')  
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto/editarProducto.html', {'form': form})

#-------------------------------------Devoluciones-------------------------------------
def devolucion(request):
    devolucion = Devoluciones.objects.all()
    empleados = Empleado.objects.all()
    proveedores = Proveedor.objects.all()
    material = MateriaPrima.objects.all()
    satelite = Satelites.objects.all()
    producto = Producto.objects.all()
    
    return render(request, 'devolucion/devolucion.html', {"devolucion": devolucion, "empleados": empleados, "proveedores": proveedores, "material": material, "satelite": satelite, "producto": producto})

def registrarDevolucion(request):
    if request.method == 'POST':
        form = DevolucionForm(request.POST)
        if form.is_valid():
            devolucion = form.save(commit=False)
            flujo = devolucion.flujo

            # Verificar si es una entrada o salida
            if flujo == 'Entrada':  # Entrada
                devolucion.save()
                # Lógica para sumar al producto o material
                if devolucion.devoProducto:
                    producto = devolucion.devoProducto
                    producto.cantidadProducto += devolucion.cantidadDevo
                    producto.save()
                elif devolucion.devoMaterial:
                    material = devolucion.devoMaterial
                    material.cantidadMaterial += devolucion.cantidadDevo
                    material.save()
            elif flujo == 'Salida':  # Salida
                # Lógica para restar del producto o material
                devolucion.save()
                if devolucion.devoProducto:
                    producto = devolucion.devoProducto
                    producto.cantidadProducto -= devolucion.cantidadDevo
                    producto.save()
                elif devolucion.devoMaterial:
                    material = devolucion.devoMaterial
                    material.cantidadMaterial -= devolucion.cantidadDevo
                    material.save()

            return redirect('devolucion')  # Redirige a donde quieras
    else:
        form = DevolucionForm()
    return render(request, 'devolucion/registrarDevolucion.html', {'form': form})

def editarDevolucion(request, idDevolucion):
    devolucion = Devoluciones.objects.get(pk=idDevolucion)
    if request.method == 'POST':
        form = DevolucionForm(request.POST, instance=devolucion)
        if form.is_valid():
            devolucion_actualizada = form.save(commit=False)
            flujo_anterior = devolucion.flujo
            flujo_nuevo = devolucion_actualizada.flujo

            # Verificar si el flujo cambió de entrada a salida o viceversa
            if flujo_anterior != flujo_nuevo:
                # Restar la cantidad de la devolución anterior
                if flujo_anterior == 'E':  # Si la devolución anterior era una entrada
                    # Lógica para restar del producto o material correspondiente
                    if devolucion.devoProducto:
                        producto = devolucion.devoProducto
                        producto.cantidadProducto -= devolucion.cantidadDevo
                        producto.save()
                    elif devolucion.devoMaterial:
                        material = devolucion.devoMaterial
                        material.cantidadMaterial -= devolucion.cantidadDevo
                        material.save()
                elif flujo_anterior == 'S':  # Si la devolución anterior era una salida
                    # Lógica para sumar al producto o material correspondiente
                    if devolucion.devoProducto:
                        producto = devolucion.devoProducto
                        producto.cantidadProducto += devolucion.cantidadDevo
                        producto.save()
                    elif devolucion.devoMaterial:
                        material = devolucion.devoMaterial
                        material.cantidadMaterial += devolucion.cantidadDevo
                        material.save()

                # Sumar la cantidad de la nueva devolución
                if flujo_nuevo == 'E':  # Si la nueva devolución es una entrada
                    # Lógica para sumar al producto o material correspondiente
                    if devolucion_actualizada.devoProducto:
                        producto = devolucion_actualizada.devoProducto
                        producto.cantidadProducto += devolucion_actualizada.cantidadDevo
                        producto.save()
                    elif devolucion_actualizada.devoMaterial:
                        material = devolucion_actualizada.devoMaterial
                        material.cantidadMaterial += devolucion_actualizada.cantidadDevo
                        material.save()
                elif flujo_nuevo == 'S':  # Si la nueva devolución es una salida
                    # Lógica para restar del producto o material correspondiente
                    if devolucion_actualizada.devoProducto:
                        producto = devolucion_actualizada.devoProducto
                        producto.cantidadProducto -= devolucion_actualizada.cantidadDevo
                        producto.save()
                    elif devolucion_actualizada.devoMaterial:
                        material = devolucion_actualizada.devoMaterial
                        material.cantidadMaterial -= devolucion_actualizada.cantidadDevo
                        material.save()

            devolucion_actualizada.save()
            return redirect('devolucion')  # Redirige a donde quieras después de la edición
    else:
        form = DevolucionForm(instance=devolucion)
    
    return render(request, 'devolucion/editarDevolucion.html', {'form': form})

#-------------------------------------Ventas-------------------------------------
def ventas(request):
    ventas = FlujoInventario.objects.filter(flujo='venta')
    return render(request, 'ventas/ventas.html', {'ventas': ventas})

def registrarVenta(request):
    if request.method == 'POST':
        form = VentasForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.save()

            # Verificar si el flujo es de tipo 'venta'
            if venta.flujo == 'venta':
                # Restar la cantidad de la venta a la cantidad del producto
                producto = venta.flujoProducto
                producto.cantidadProducto -= venta.cantidadFlujo
                producto.save()

            return redirect('ventas')  # Cambia 'ventas' por la URL a la que quieres redirigir después de guardar la venta
    else:
        form = VentasForm()
    return render(request, 'ventas/registrarVenta.html', {'form': form})

def editarVenta(request, idComprovante):
    venta = FlujoInventario.objects.get(pk=idComprovante)

    if request.method == 'POST':
        form = VentasForm(request.POST, instance=venta)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.save()

            # Verificar si el flujo es de tipo 'venta'
            if venta.flujo == 'venta':
                # Restar la cantidad de la venta a la cantidad del producto
                producto = venta.flujoProducto
                producto.cantidadProducto -= venta.cantidadFlujo
                producto.save()

            return redirect('ventas')  # Cambia 'ventas' por la URL a la que quieres redirigir después de guardar la venta editada
    else:
        form = VentasForm(instance=venta)
    return render(request, 'ventas/editarVenta.html', {'form': form})

