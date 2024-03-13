from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Arl(models.Model):
    idArl = models.AutoField(primary_key=True)
    arl = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idArl, self.arl)
    
class Eps(models.Model):
    idEps = models.AutoField(primary_key=True)
    eps = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idEps, self.eps)
    
class Ciudad(models.Model):
    idCiudad = models.AutoField(primary_key=True)
    ciudad = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idCiudad, self.ciudad)

class Cargo(models.Model):
    idCargo = models.AutoField(primary_key=True)
    cargo = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.cargo

class MateriaPrima(models.Model):
    idMaterial = models.AutoField(primary_key=True)
    material = models.CharField(max_length=30)
    cantidadMaterial = models.FloatField(default=0.0)
    medidas = [
        ('m','metros'),
        ('k','kilos'),
        ('u','unidaddes')
    ]
    medida = models.CharField(max_length=1, choices=medidas, default='m')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        txt = "{0}, {1} en stok: {2} {3}"
        return txt.format(self.idMaterial, self.material, self.cantidadMaterial, self.medida)
    
class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    producto = models.CharField(max_length=30)
    cantidadProducto = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        txt = "{0}, {1} en stok: {2} unidades"
        return txt.format(self.idProducto, self.producto, self.cantidadProducto)

class Personas(models.Model):
    documento = models.PositiveIntegerField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, default='Calle/Carrera 00 sur/norte #00-00')
    correo = models.CharField(max_length=50)
    celular = models.PositiveIntegerField()
    fechaNac = models.DateField()
    ciudadPersona = models.ForeignKey(Ciudad, null=False, blank=False, default=1, on_delete=models.CASCADE)
    sexos = [
        ('F', 'Femenino'),
        ('M', 'Masculino')
    ]
    sexo = models.CharField(max_length=1, choices=sexos, default='F')
    
    def __str__(self):
        txt = "{0}, {1} {2} cel:{3}"
        return txt.format(self.documento, self.nombres, self.apellidos, self.celular)
    
class Satelites(models.Model):
    idSatelite = models.AutoField(primary_key=True)
    docSatelite = models.ForeignKey(Personas, null=False, blank=False, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def tiene_cortes_activos(self):
        return self.cortes.filter(entregado=False).exists()

    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idSatelite, self.docSatelite.apellidos)

class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    docProveedor = models.ForeignKey(Personas, null=False, blank=False, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idProveedor, self.docProveedor.apellidos)

class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)
    docCliente = models.ForeignKey(Personas, null=False, blank=False, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idCliente, self.docCliente.apellidos)

class Empleado(models.Model):
    idEmpleado = models.AutoField(primary_key=True)
    docEmpleado = models.ForeignKey(Personas, null=False, blank=False, on_delete=models.CASCADE)
    arlEmpleado = models.ForeignKey(Arl, null=False, blank=False, on_delete=models.CASCADE)
    epsEmpleado = models.ForeignKey(Eps, null=False, blank=False, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, null=False, blank=False, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    contraseña = models.CharField(max_length=30, default='')

    def __str__(self) -> str:
        txt = "{0}, {1}, ({2}, {3})"
        return txt.format(self.idEmpleado, self.docEmpleado.apellidos, self.arlEmpleado.arl, self.epsEmpleado.eps)
    
    def save(self, *args, **kwargs):
        if not self.idEmpleado:  
            self.contraseña = make_password(self.contraseña)  
        super().save(*args, **kwargs)
    
class Corte(models.Model):
    idCorte = models.AutoField(primary_key=True)
    materialCorte = models.ForeignKey(MateriaPrima, null=False, blank=False, on_delete=models.CASCADE)
    cantidadCorte = models.FloatField(default=0.0)
    medidas = [
        ('m','metros'),
        ('k','kilos')
    ]
    medida = models.CharField(max_length=1, choices=medidas, default='m')
    productoCorte = models.ForeignKey(Producto, null=False, blank=False, on_delete=models.CASCADE)
    entregado = models.BooleanField(default=False)
    fechaCorte = models.DateTimeField(auto_now_add=True)
    
    satelite = models.ForeignKey(Satelites, related_name='cortes', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        txt = "{0}, Material: {1}, Producto Final: {2}, {3}"
        return txt.format(self.idCorte, self.materialCorte.material, self.productoCorte.producto, self.fechaCorte)    
    
class FlujoInventario(models.Model):
    idComprovante = models.AutoField(primary_key=True)
    docEmpleado = models.ForeignKey(Empleado, null=False, blank=False, on_delete=models.CASCADE)
    proveedorFlujo = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.CASCADE)
    materialFlu = models.ForeignKey(MateriaPrima, null=True, blank=True, on_delete=models.CASCADE)
    flujoCliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    flujoSatelite = models.ForeignKey(Satelites, null=True, blank=True, on_delete=models.CASCADE)
    flujoProducto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.CASCADE)
    flujoCorte = models.ForeignKey(Corte, null=True, blank=True, on_delete=models.CASCADE)
    insumos = models.ManyToManyField(MateriaPrima, related_name='flujos_inventario')
    flujos = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('venta', 'Venta'),
    ]
    flujo = models.CharField(max_length=20, choices=flujos, default='entrada')
    fechaFlujo = models.DateTimeField(auto_now_add=True)
    cantidadFlujo = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        txt = "{0}, {1}, {2}: {3} {4}"
        return txt.format(self.idComprovante, self.docEmpleado, self.flujo, self.fechaFlujo, self.cantidadFlujo)
    
class DetalleFlujoInventario(models.Model):
    flujo_inventario = models.ForeignKey(FlujoInventario, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    
class Devoluciones(models.Model):
    idDevolucion = models.AutoField(primary_key=True)
    devoEmpleado = models.ForeignKey(Empleado, default=None, null=False, blank=False, on_delete=models.CASCADE)
    devoSatelite = models.ForeignKey(Satelites, default=None, null=True, blank=True, on_delete=models.CASCADE)
    devoProveedor = models.ForeignKey(Proveedor, default=None, null=True, blank=True, on_delete=models.CASCADE)
    devoProducto = models.ForeignKey(Producto, default=None, null=True, blank=True, on_delete=models.CASCADE)
    devoMaterial = models.ForeignKey(MateriaPrima, default=None, null=True, blank=True, on_delete=models.CASCADE)
    flujos = [
        ('E', 'Entrada'),
        ('S', 'Salida')
    ]
    flujo = models.CharField(max_length=1, choices=flujos, default='E')
    motivo = models.CharField(max_length=255, default="")
    cantidadDevo = models.FloatField(null=False, blank=False, default=0.0)
    fechaDevolucion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        txt = "{0}, {1}"
        return txt.format(self.idDevolucion, self.fechaDevolucion)
    
    