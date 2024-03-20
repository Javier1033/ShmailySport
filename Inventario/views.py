from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Create your views here.

#--------------------------------Index y Login--------------------------------------
def login_views(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        docEmpleado = request.POST.get('documento')
        contraseña = request.POST.get('contrasena')

        # Autenticar al usuario
        try:
            empleado = Empleado.objects.get(docEmpleado__documento=docEmpleado)
            contraseña_empleado = empleado.contraseña
            if check_password(contraseña, contraseña_empleado):
                # Las contraseñas coinciden
                user = User.objects.get(username=docEmpleado)
                login(request, user)
                return redirect('home')
            else:
                # Las contraseñas no coinciden
                print("La autenticación ha fallado.")
                messages.error(request, "Credenciales incorrectas.")
                return redirect('index')
        except Empleado.DoesNotExist:
            # Agregar mensaje de depuración
            print("El empleado asociado al usuario autenticado no fue encontrado.")
            messages.error(request, "Credenciales incorrectas.")
            return redirect('index')

    # Renderizar el formulario de inicio de sesión
    return render(request, 'index.html')

def cerrar_sesion(request):
    # Cerrar la sesión del usuario
    logout(request)
    messages.info(request, "¡Sesión cerrada correctamente!")
    return redirect('index')

@login_required
def home(request):
    if request.user.is_authenticated:
        try:
            empleado = Empleado.objects.get(docEmpleado=request.user.username)
            persona = empleado.docEmpleado
            nombre_completo = f"{persona.nombres} {persona.apellidos}"
            cargo_empleado = empleado.cargo.cargo
            return render(request, 'home.html', {'nombre_completo': nombre_completo, 'cargo_empleado': cargo_empleado})
        except Empleado.DoesNotExist:
            # Agregar mensaje de depuración
            print("El empleado asociado al usuario autenticado no fue encontrado.")
            messages.error(request, "No tienes permiso para acceder a este perfil.")
            return redirect('index')
    else:
        return redirect('index')
    
#-------------------------------------Correos-------------------------------------
@login_required
def enviar_correo(request):
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        destinatarios_str = request.POST.get('destinatario')
        destinatarios = [email.strip() for email in destinatarios_str.split(',')]

        adjuntos = request.FILES.getlist('adjuntos')

        try:
            email = EmailMessage(
                subject=asunto,
                body=mensaje,
                to=destinatarios
            )

            # Adjuntar archivos
            for adjunto in adjuntos:
                email.attach(adjunto.name, adjunto.read(), adjunto.content_type)

            # Enviar correo electrónico
            email.send()

            return render(request, 'enviar_correo.html', {'mensaje': 'Correo enviado correctamente.'})
        except Exception as e:
            return render(request, 'enviar_correo.html', {'error': str(e)})

    return render(request, 'enviar_correo.html')

#-------------------------------------Reportes PDF-------------------------------------
@login_required
def generar_reporte_pdf(request):
    return render(request, 'generar_reporte_pdf.html')

@login_required
def generar_reporte(request):
    flujo = request.GET.get('flujo')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    flujos = FlujoInventario.objects.all()
    if flujo:
        flujos = flujos.filter(flujo=flujo)
    if fecha_inicio and fecha_fin:
        flujos = flujos.filter(fechaFlujo__range=[fecha_inicio, fecha_fin])

    # Lista de títulos de columna
    column_titles = ['ID', 'Empleado', 'Proveedor', 'Material', 'Cliente', 'Satélite', 'Producto', 'Corte', 'Flujo', 'Fecha', 'Cantidad']

    data = []

    # Agregar encabezados de tabla como una fila completa
    data.append(column_titles)

    # Agregar datos de flujos de inventario a la tabla
    for flujo in flujos:
        empleado = flujo.docEmpleado.docEmpleado.apellidos if flujo.docEmpleado else ""
        proveedor = flujo.proveedorFlujo.docProveedor.apellidos if flujo.proveedorFlujo else ""
        material = flujo.materialFlu.material if flujo.materialFlu else ""
        cliente = flujo.flujoCliente.docCliente.apellidos if flujo.flujoCliente else ""
        satelite = flujo.flujoSatelite.docSatelite.apellidos if flujo.flujoSatelite else ""
        producto = flujo.flujoProducto.producto if flujo.flujoProducto else ""
        corte = flujo.flujoCorte.idCorte if flujo.flujoCorte else ""
        flujo_nombre = flujo.flujo
        fecha = flujo.fechaFlujo.strftime('%Y-%m-%d %H:%M:%S') if flujo.fechaFlujo else ""
        cantidad = flujo.cantidadFlujo if flujo.cantidadFlujo else ""

        # Agregar la fila solo si al menos uno de los campos tiene un valor no vacío
        if any([empleado, proveedor, material, cliente, satelite, producto, corte, flujo_nombre, fecha, cantidad]):
            data.append([flujo.idComprovante, empleado, proveedor, material, cliente, satelite, producto, corte, flujo_nombre, fecha, cantidad])

    # Si hay datos para mostrar, generar el reporte
    if data:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)

        # Crear la tabla
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                                   ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                                   ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                   ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0,0), (-1,0), 12),
                                   ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                                   ('GRID', (0,0), (-1,-1), 1, colors.black)]))

        # Agregar la tabla al documento
        doc.build([table])

        return response
    else:
        # Si no hay datos para mostrar, retornar una respuesta vacía
        return HttpResponse("No hay datos para mostrar en el reporte.")

#-------------------------------------Empleado-------------------------------------
@login_required
def empleado(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        empleados_activos = Empleado.objects.filter(activo=True)
        empleados_inactivos = Empleado.objects.filter(activo=False)
        persona = Personas.objects.all()
        arls = Arl.objects.all()
        epss = Eps.objects.all()
        cargos = Cargo.objects.all()

        return render(request, 'empleado/empleado.html', {"empleados_activos": empleados_activos, "empleados_inactivos": empleados_inactivos, "persona": persona, "arls": arls, "epss": epss, "cargos": cargos})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarEmpleado(request):
    # Verificar si el usuario pertenece a alguno de los roles permitidos
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        if request.method == 'POST':
            form = RegistroEmpleadoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('empleado') 
        else:
            form = RegistroEmpleadoForm()
        
        return render(request, 'empleado/registrarEmpleado.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarEmpleado(request, idEmpleado):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
        if request.method == 'POST':
            form = EditarEmpleadoForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                return redirect('empleado') 
        else:
            form = EditarEmpleadoForm(instance=empleado, empleado=empleado)
        
        return render(request, 'empleado/editarEmpleado.html', {'form': form, 'empleado': empleado})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------Satelite-------------------------------------
@login_required
def satelite(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'JefeBodega']).exists():
        satelite_activo = Satelites.objects.filter(activo=True)
        satelite_inactivo = Satelites.objects.filter(activo=False)
        persona = Personas.objects.all()
        
        return render(request, 'satelite/satelite.html', {"satelite_activo": satelite_activo, "satelite_inactivo": satelite_inactivo, "persona": persona})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

@login_required
def registrarSatelite(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        if request.method == 'POST':
            form = RegistroSateliteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('satelite') 
        else:
            form = RegistroSateliteForm()
        
        return render(request, 'satelite/registrarSatelite.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

@login_required
def editarSatelite(request, idSatelite):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        satelite = get_object_or_404(Satelites, idSatelite=idSatelite)
        if request.method == 'POST':
            form = EditarSateliteForm(request.POST, instance=satelite)
            if form.is_valid():
                form.save()
                return redirect('satelite') 
        else:
            form = EditarSateliteForm(instance=satelite, satelite=satelite)
        
        return render(request, 'satelite/editarSatelite.html', {'form': form, 'satelite': satelite})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------Proveedor-------------------------------------
@login_required
def proveedores(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        proveedores_activos = Proveedor.objects.filter(activo=True)
        proveedores_inactivos = Proveedor.objects.filter(activo=False)
        persona = Personas.objects.all()
        
        return render(request, 'proveedor/proveedor.html', {"proveedores_activos": proveedores_activos, "proveedores_inactivos": proveedores_inactivos, "persona": persona})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarProveedor(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        if request.method == 'POST':
            form = RegistroProveedorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('proveedor') 
        else:
            form = RegistroProveedorForm()
        
        return render(request, 'proveedor/registrarProveedor.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarProveedor(request, idProveedor):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        proveedores = get_object_or_404(Proveedor, idProveedor=idProveedor)
        if request.method == 'POST':
            form = EditarProveedorForm(request.POST, instance=proveedores)
            if form.is_valid():
                form.save()
                return redirect('proveedor') 
        else:
            form = EditarProveedorForm(instance=proveedores, proveedores=proveedores)
        
        return render(request, 'proveedor/editarProveedor.html', {'form': form, 'proveedores': proveedores})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------Cliente-------------------------------------
@login_required
def cliente(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'Vendedor']).exists():
        clientes_activos = Cliente.objects.filter(activo=True)
        clientes_inactivos = Cliente.objects.filter(activo=False)
        persona = Personas.objects.all()
        
        return render(request, 'cliente/cliente.html', {"clientes_activos": clientes_activos, "clientes_inactivos": clientes_inactivos, "persona": persona})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarCliente(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'Vendedor']).exists():
        if request.method == 'POST':
            form = RegistroClienteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('cliente') 
        else:
            form = RegistroClienteForm()
        
        return render(request, 'cliente/registrarCliente.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

@login_required
def editarCliente(request, idCliente):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'Vendedor']).exists():
        clientes = get_object_or_404(Cliente, idCliente=idCliente)
        if request.method == 'POST':
            form = EditarClienteForm(request.POST, instance=clientes)
            if form.is_valid():
                form.save()
                return redirect('cliente') 
        else:
            form = EditarClienteForm(instance=clientes, clientes=clientes)
        
        return render(request, 'cliente/editarCliente.html', {'form': form, 'clientes': clientes})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------SatelitesCorte-------------------------------------
@login_required
def vistaSatelite(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'JefeBodega', 'auxiliar']).exists():
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
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def marcar_entregado(request, idCorte):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'JefeBodega']).exists():
        corte = Corte.objects.get(pk=idCorte)
        corte.entregado = True
        corte.save()
        return redirect('vistaSatelite')
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------FlujoInventario-------------------------------------
@login_required
def flujoInventario(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'JefeBodega']).exists():
        flujoInventario = FlujoInventario.objects.all()
        empleados = Empleado.objects.all()
        proveedores = Proveedor.objects.all()
        material = MateriaPrima.objects.all()
        satelite = Satelites.objects.all()
        cortes = Corte.objects.all()
            
        return render(request, 'flujoInventario/FlujoInventario.html', {"flujoInventario": flujoInventario, "empleados": empleados, "proveedores": proveedores, "material": material, "satelite": satelite, "cortes": cortes})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registroFlujo(request):
    if request.user.groups.filter(name__in=['JefeBodega', 'Administrador', 'Gerente']).exists():
        insumos = MateriaPrima.objects.filter(activo=True)
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

        return render(request, 'flujoInventario/registroFlujo.html', {'form': form, 'insumos': insumos})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarFlujo(request, idComprovante):
    if request.user.groups.filter(name__in=['JefeBodega', 'Administrador', 'Gerente']).exists():
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
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarCorte(request):
    if request.user.groups.filter(name__in=['JefeBodega', 'Administrador', 'Gerente']).exists():
        if request.method == 'POST':
            form = CorteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('registroFlujo')  
        else:
            cortes_no_entregados = Corte.objects.filter(entregado=False)
            form = CorteForm(initial={'productoCorte': cortes_no_entregados})
        return render(request, 'flujoInventario/registrarCorte.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def eliminarFlujo(request, idComprovante):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        flujo = FlujoInventario.objects.get(idComprovante=idComprovante)
        flujo.delete()

        return redirect('flujoInventario')
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------MateriaPrima-------------------------------------
@login_required
def materiaPrima(request):
    if request.user.groups.filter(name__in=['JefeBodega', 'Administrador', 'Gerente']).exists():
        materias_primas_activas = MateriaPrima.objects.filter(activo=True)
        materias_primas_inactivas = MateriaPrima.objects.filter(activo=False)
        return render(request, 'materiaPrima/materiaPrima.html', {'materias_primas_activas': materias_primas_activas, 'materias_primas_inactivas': materias_primas_inactivas})
    else:
            # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('home')
        
@login_required
def registrarMaterial(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        if request.method == 'POST':
            form = MateriaPrimaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('materiaPrima')  # Redirige a la página de lista de materias primas después de guardar
        else:
            form = MateriaPrimaForm()
        return render(request, 'materiaPrima/registrarMaterial.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarMaterial(request, idMaterial):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        materia_prima = get_object_or_404(MateriaPrima, idMaterial=idMaterial)
        if request.method == 'POST':
            form = MateriaPrimaForm(request.POST, instance=materia_prima)
            if form.is_valid():
                form.update(materia_prima)
                return redirect('materiaPrima')
        else:
            form = MateriaPrimaForm(instance=materia_prima)
        return render(request, 'materiaPrima/editarMaterial.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------Productos-------------------------------------
@login_required
def productos(request):
    if request.user.groups.filter(name__in=['JefeBodega', 'Vendedor', 'Auxiliar', 'Administrador', 'Gerente']).exists():
        productos_activos = Producto.objects.filter(activo=True)
        productos_inactivos = Producto.objects.filter(activo=False)
        return render(request, 'producto/producto.html', {'productos_activos': productos_activos, 'productos_inactivos': productos_inactivos})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarProducto(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        if request.method == 'POST':
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('producto')  # Redirige a la página de lista de productos después de guardar
        else:
            form = ProductoForm()
        return render(request, 'producto/registrarProducto.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarProducto(request, idProducto):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        producto = get_object_or_404(Producto, idProducto=idProducto)
        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return redirect('producto')  
        else:
            form = ProductoForm(instance=producto)
        return render(request, 'producto/editarProducto.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------Devoluciones-------------------------------------
@login_required
def devolucion(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'auxiliar', 'JefeBodega']).exists():
        devolucion = Devoluciones.objects.all()
        empleados = Empleado.objects.all()
        proveedores = Proveedor.objects.all()
        material = MateriaPrima.objects.all()
        satelite = Satelites.objects.all()
        producto = Producto.objects.all()
        
        return render(request, 'devolucion/devolucion.html', {"devolucion": devolucion, "empleados": empleados, "proveedores": proveedores, "material": material, "satelite": satelite, "producto": producto})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarDevolucion(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'JefeBodega', 'auxiliar']).exists():
        if request.method == 'POST':
            form = DevolucionesForm(request.POST)
            if form.is_valid():
                devolucion = form.save(commit=False)
                flujo = devolucion.flujo

                # Verificar si es una entrada o salida
                if flujo == 'entrada':  # Entrada
                    # Lógica para sumar al producto o material
                    if devolucion.devoProducto:
                        producto = devolucion.devoProducto
                        producto.cantidadProducto += devolucion.cantidadDevo
                        producto.save()
                    elif devolucion.devoMaterial:
                        material = devolucion.devoMaterial
                        material.cantidadMaterial += devolucion.cantidadDevo
                        material.save()
                elif flujo == 'salida':  # Salida
                    # Lógica para restar del producto o material
                    if devolucion.devoProducto:
                        producto = devolucion.devoProducto
                        producto.cantidadProducto -= devolucion.cantidadDevo
                        producto.save()
                    elif devolucion.devoMaterial:
                        material = devolucion.devoMaterial
                        material.cantidadMaterial -= devolucion.cantidadDevo
                        material.save()

                # Guardar la devolución después de actualizar la cantidad
                devolucion.save()

                return redirect('devolucion')  # Redirige a donde quieras
        else:
            form = DevolucionesForm()
        return render(request, 'devolucion/registrarDevolucion.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarDevolucion(request, pk):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        # Obtener la devolución por su clave primaria (pk)
        devolucion = get_object_or_404(Devoluciones, pk=pk)

        if request.method == 'POST':
            # Llenar el formulario con los datos de la devolución
            form = DevolucionesForm(request.POST, instance=devolucion)
            if form.is_valid():
                devolucion = form.save(commit=False)
                flujo = devolucion.flujo

                # Verificar si es una entrada o salida
                if flujo == 'entrada':  # Entrada
                    # Lógica para actualizar la cantidad en el producto o material
                    if devolucion.devoProducto:
                        producto = devolucion.devoProducto
                        producto.cantidadProducto += devolucion.cantidadDevo
                        producto.save()
                    elif devolucion.devoMaterial:
                        material = devolucion.devoMaterial
                        material.cantidadMaterial += devolucion.cantidadDevo
                        material.save()
                elif flujo == 'salida':  # Salida
                    # Lógica para actualizar la cantidad en el producto o material
                    if devolucion.devoProducto:
                        producto = devolucion.devoProducto
                        producto.cantidadProducto -= devolucion.cantidadDevo
                        producto.save()
                    elif devolucion.devoMaterial:
                        material = devolucion.devoMaterial
                        material.cantidadMaterial -= devolucion.cantidadDevo
                        material.save()

                # Guardar los cambios en la devolución
                devolucion.save()

                return redirect('devolucion')  # Redirige a donde quieras
        else:
            # Llenar el formulario con los datos de la devolución
            form = DevolucionesForm(instance=devolucion)
        
        return render(request, 'devolucion/editarDevolucion.html', {'form': form})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def eliminarDevolucion(request, idDevolucion):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        devolucion = Devoluciones.objects.get(idDevolucion=idDevolucion)
        devolucion.delete()

        return redirect('devolucion')
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
#-------------------------------------Ventas-------------------------------------
@login_required
def ventas(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'Vendedor']).exists():
        ventas = FlujoInventario.objects.filter(flujo='venta')
        return render(request, 'ventas/ventas.html', {'ventas': ventas})
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def registrarVenta(request):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'Vendedor']).exists():
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
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def editarVenta(request, idComprovante):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente', 'Vendedor']).exists():
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
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
@login_required
def eliminarVenta(request, idComprovante):
    if request.user.groups.filter(name__in=['Administrador', 'Gerente']).exists():
        venta = FlujoInventario.objects.get(idComprovante=idComprovante)
        venta.delete()

        return redirect('ventas')
    else:
        # Si el usuario no tiene permisos, mostrar un mensaje de error y redirigirlo a otra página
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
    