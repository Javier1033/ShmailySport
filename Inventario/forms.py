from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from django.forms import DateInput
from .models import *
from django.contrib.auth.models import User

#----------------------------------Empleados----------------------------------
class RegistroEmpleadoForm(forms.ModelForm):
    documento = forms.IntegerField(label='Documento de identidad')
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Dirección de residencia', max_length=50)
    correo = forms.EmailField(label='Correo electrónico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de residencia', required=False)
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Género')
    contraseña = forms.CharField(label='Contraseña', max_length=30, min_length=8, widget=forms.PasswordInput,)

    arlEmpleado = forms.ModelChoiceField(queryset=Arl.objects.all(), label='ARL del empleado', required=False)
    epsEmpleado = forms.ModelChoiceField(queryset=Eps.objects.all(), label='EPS del empleado', required=False)
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), label='Cargo del empleado', required=False)

    nueva_arl = forms.CharField(label='Nueva ARL', required=False)
    nueva_eps = forms.CharField(label='Nueva EPS', required=False)
    nuevo_cargo = forms.CharField(label='Nuevo Cargo', required=False)

    class Meta:
        model = Empleado
        fields = ['documento', 'nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo', 'arlEmpleado', 'epsEmpleado', 'cargo', 'contraseña']

    def save(self, commit=True):
        persona = Personas.objects.create(
            documento=self.cleaned_data['documento'],
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            direccion=self.cleaned_data['direccion'],
            correo=self.cleaned_data['correo'],
            celular=self.cleaned_data['celular'],
            fechaNac=self.cleaned_data['fechaNac'],
            ciudadPersona=self.cleaned_data['ciudadPersona'],
            sexo=self.cleaned_data['sexo']
        )
        arl_empleado = self.cleaned_data['arlEmpleado']
        eps_empleado = self.cleaned_data['epsEmpleado']
        cargo_empleado = self.cleaned_data['cargo']

        if self.cleaned_data['nueva_arl']:
            arl_empleado = Arl.objects.create(arl=self.cleaned_data['nueva_arl'])
        if self.cleaned_data['nueva_eps']:
            eps_empleado = Eps.objects.create(eps=self.cleaned_data['nueva_eps'])
        if self.cleaned_data['nuevo_cargo']:
            cargo_empleado = Cargo.objects.create(cargo=self.cleaned_data['nuevo_cargo'])

        empleado = Empleado.objects.create(
            docEmpleado=persona,
            arlEmpleado=arl_empleado,
            epsEmpleado=eps_empleado,
            cargo=cargo_empleado,
            contraseña=self.cleaned_data['contraseña']  # Guardar la contraseña sin encriptar
        )

        username = self.cleaned_data['documento']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=self.cleaned_data['contraseña'])
            user.save()
        return empleado

class EditarEmpleadoForm(forms.ModelForm):
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento')
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia')
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    arlEmpleado = forms.ModelChoiceField(queryset=Arl.objects.all(), label='Arl del empleado')
    epsEmpleado = forms.ModelChoiceField(queryset=Eps.objects.all(), label='Eps del empleado')
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), label='Cargo del empleado')
    
    activo = forms.BooleanField(required=False)

    class Meta:
        model = Empleado
        fields = ['nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo', 'arlEmpleado', 'epsEmpleado', 'cargo', 'activo']

    def __init__(self, *args, **kwargs):
        empleado = kwargs.pop('empleado', None)
        super(EditarEmpleadoForm, self).__init__(*args, **kwargs)
        if empleado:
            self.fields['nombres'].initial = empleado.docEmpleado.nombres
            self.fields['apellidos'].initial = empleado.docEmpleado.apellidos
            self.fields['direccion'].initial = empleado.docEmpleado.direccion
            self.fields['correo'].initial = empleado.docEmpleado.correo
            self.fields['celular'].initial = empleado.docEmpleado.celular
            self.fields['fechaNac'].initial = empleado.docEmpleado.fechaNac
            self.fields['ciudadPersona'].initial = empleado.docEmpleado.ciudadPersona
            self.fields['sexo'].initial = empleado.docEmpleado.sexo

    def save(self, commit=True):
        empleado = super(EditarEmpleadoForm, self).save(commit=False)
        empleado.docEmpleado.nombres = self.cleaned_data['nombres']
        empleado.docEmpleado.apellidos = self.cleaned_data['apellidos']
        empleado.docEmpleado.direccion = self.cleaned_data['direccion']
        empleado.docEmpleado.correo = self.cleaned_data['correo']
        empleado.docEmpleado.celular = self.cleaned_data['celular']
        empleado.docEmpleado.fechaNac = self.cleaned_data['fechaNac']
        empleado.docEmpleado.ciudadPersona = self.cleaned_data['ciudadPersona']
        empleado.docEmpleado.sexo = self.cleaned_data['sexo']
        empleado.docEmpleado.save()
        if commit:
            empleado.save()
        return empleado
    
#----------------------------------Satelites----------------------------------
class RegistroSateliteForm(forms.ModelForm):
    documento = forms.IntegerField(label='Documento de identidad')
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento', widget=DateInput(attrs={'type': 'date'}))
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia', required=False)
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    class Meta:
        model = Satelites
        fields = ['documento', 'nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo']

    def save(self, commit=True):
        persona = Personas.objects.create(
            documento=self.cleaned_data['documento'],
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            direccion=self.cleaned_data['direccion'],
            correo=self.cleaned_data['correo'],
            celular=self.cleaned_data['celular'],
            fechaNac=self.cleaned_data['fechaNac'],
            ciudadPersona=self.cleaned_data['ciudadPersona'],
            sexo=self.cleaned_data['sexo']
        )

        satelite = Satelites.objects.create(
            docSatelite=persona
        )
        return satelite

class EditarSateliteForm(forms.ModelForm):
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento')
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia')
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    activo = forms.BooleanField(required=False)

    class Meta:
        model = Satelites
        fields = ['nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo', 'activo']

    def __init__(self, *args, **kwargs):
        satelite = kwargs.pop('satelite', None)
        super(EditarSateliteForm, self).__init__(*args, **kwargs)
        if satelite:
            self.fields['nombres'].initial = satelite.docSatelite.nombres
            self.fields['apellidos'].initial = satelite.docSatelite.apellidos
            self.fields['direccion'].initial = satelite.docSatelite.direccion
            self.fields['correo'].initial = satelite.docSatelite.correo
            self.fields['celular'].initial = satelite.docSatelite.celular
            self.fields['fechaNac'].initial = satelite.docSatelite.fechaNac
            self.fields['ciudadPersona'].initial = satelite.docSatelite.ciudadPersona
            self.fields['sexo'].initial = satelite.docSatelite.sexo

    def save(self, commit=True):
        satelite = super(EditarSateliteForm, self).save(commit=False)
        satelite.docSatelite.nombres = self.cleaned_data['nombres']
        satelite.docSatelite.apellidos = self.cleaned_data['apellidos']
        satelite.docSatelite.direccion = self.cleaned_data['direccion']
        satelite.docSatelite.correo = self.cleaned_data['correo']
        satelite.docSatelite.celular = self.cleaned_data['celular']
        satelite.docSatelite.fechaNac = self.cleaned_data['fechaNac']
        satelite.docSatelite.ciudadPersona = self.cleaned_data['ciudadPersona']
        satelite.docSatelite.sexo = self.cleaned_data['sexo']
        satelite.docSatelite.save()
        if commit:
            satelite.save()
        return satelite

#----------------------------------Proveedor----------------------------------
class RegistroProveedorForm(forms.ModelForm):
    documento = forms.IntegerField(label='Documento de identidad')
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento', widget=DateInput(attrs={'type': 'date'}))
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia', required=False)
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    class Meta:
        model = Proveedor
        fields = ['documento', 'nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo']

    def save(self, commit=True):
        persona = Personas.objects.create(
            documento=self.cleaned_data['documento'],
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            direccion=self.cleaned_data['direccion'],
            correo=self.cleaned_data['correo'],
            celular=self.cleaned_data['celular'],
            fechaNac=self.cleaned_data['fechaNac'],
            ciudadPersona=self.cleaned_data['ciudadPersona'],
            sexo=self.cleaned_data['sexo']
        )
        proveedor = Proveedor.objects.create(
            docProveedor=persona
        )
        return proveedor

class EditarProveedorForm(forms.ModelForm):
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento')
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia')
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    activo = forms.BooleanField(required=False)

    class Meta:
        model = Proveedor
        fields = ['nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo', 'activo']

    def __init__(self, *args, **kwargs):
        proveedores = kwargs.pop('proveedores', None)
        super(EditarProveedorForm, self).__init__(*args, **kwargs)
        if proveedores:
            self.fields['nombres'].initial = proveedores.docProveedor.nombres
            self.fields['apellidos'].initial = proveedores.docProveedor.apellidos
            self.fields['direccion'].initial = proveedores.docProveedor.direccion
            self.fields['correo'].initial = proveedores.docProveedor.correo
            self.fields['celular'].initial = proveedores.docProveedor.celular
            self.fields['fechaNac'].initial = proveedores.docProveedor.fechaNac
            self.fields['ciudadPersona'].initial = proveedores.docProveedor.ciudadPersona
            self.fields['sexo'].initial = proveedores.docProveedor.sexo

    def save(self, commit=True):
        proveedores = super(EditarProveedorForm, self).save(commit=False)
        proveedores.docProveedor.nombres = self.cleaned_data['nombres']
        proveedores.docProveedor.apellidos = self.cleaned_data['apellidos']
        proveedores.docProveedor.direccion = self.cleaned_data['direccion']
        proveedores.docProveedor.correo = self.cleaned_data['correo']
        proveedores.docProveedor.celular = self.cleaned_data['celular']
        proveedores.docProveedor.fechaNac = self.cleaned_data['fechaNac']
        proveedores.docProveedor.ciudadPersona = self.cleaned_data['ciudadPersona']
        proveedores.docProveedor.sexo = self.cleaned_data['sexo']
        proveedores.docProveedor.save()
        if commit:
            proveedores.save()
        return proveedores

#----------------------------------Cliente----------------------------------
class RegistroClienteForm(forms.ModelForm):
    documento = forms.IntegerField(label='Documento de identidad')
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento', widget=DateInput(attrs={'type': 'date'}))
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia', required=False)
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    class Meta:
        model = Cliente
        fields = ['documento', 'nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo']

    def save(self, commit=True):
        persona = Personas.objects.create(
            documento=self.cleaned_data['documento'],
            nombres=self.cleaned_data['nombres'],
            apellidos=self.cleaned_data['apellidos'],
            direccion=self.cleaned_data['direccion'],
            correo=self.cleaned_data['correo'],
            celular=self.cleaned_data['celular'],
            fechaNac=self.cleaned_data['fechaNac'],
            ciudadPersona=self.cleaned_data['ciudadPersona'],
            sexo=self.cleaned_data['sexo']
        )

        cliente = Cliente.objects.create(
            docCliente=persona
        )
        return cliente

class EditarClienteForm(forms.ModelForm):
    nombres = forms.CharField(label='Nombres', max_length=50)
    apellidos = forms.CharField(label='Apellidos', max_length=50)
    direccion = forms.CharField(label='Direccion de recidencia', max_length=50)
    correo = forms.EmailField(label='Correo electronico', max_length=50)
    celular = forms.IntegerField(label='No. de contacto')
    fechaNac = forms.DateField(label='Fecha de Nacimiento')
    ciudadPersona = forms.ModelChoiceField(queryset=Ciudad.objects.all(), label='Ciudad de recidencia')
    sexo = forms.ChoiceField(choices=Personas.sexos, label='Genero')

    activo = forms.BooleanField(required=False)

    class Meta:
        model = Cliente
        fields = ['nombres', 'apellidos', 'direccion', 'correo', 'celular', 'fechaNac', 'ciudadPersona', 'sexo', 'activo']

    def __init__(self, *args, **kwargs):
        clientes = kwargs.pop('clientes', None)
        super(EditarClienteForm, self).__init__(*args, **kwargs)
        if clientes:
            self.fields['nombres'].initial = clientes.docCliente.nombres
            self.fields['apellidos'].initial = clientes.docCliente.apellidos
            self.fields['direccion'].initial = clientes.docCliente.direccion
            self.fields['correo'].initial = clientes.docCliente.correo
            self.fields['celular'].initial = clientes.docCliente.celular
            self.fields['fechaNac'].initial = clientes.docCliente.fechaNac
            self.fields['ciudadPersona'].initial = clientes.docCliente.ciudadPersona
            self.fields['sexo'].initial = clientes.docCliente.sexo

    def save(self, commit=True):
        clientes = super(EditarClienteForm, self).save(commit=False)
        clientes.docCliente.nombres = self.cleaned_data['nombres']
        clientes.docCliente.apellidos = self.cleaned_data['apellidos']
        clientes.docCliente.direccion = self.cleaned_data['direccion']
        clientes.docCliente.correo = self.cleaned_data['correo']
        clientes.docCliente.celular = self.cleaned_data['celular']
        clientes.docCliente.fechaNac = self.cleaned_data['fechaNac']
        clientes.docCliente.ciudadPersona = self.cleaned_data['ciudadPersona']
        clientes.docCliente.sexo = self.cleaned_data['sexo']
        clientes.docCliente.save()
        if commit:
            clientes.save()
        return clientes

#----------------------------------SateliteInv----------------------------------
class SateliteCortesForm(forms.Form):
    satelite = forms.ModelChoiceField(queryset=Satelites.objects.filter(activo=True))
    cortes = forms.ModelMultipleChoiceField(queryset=Corte.objects.none(), required=False)
    entregado = forms.BooleanField(required=False, label='¿Entregado?')

    def __init__(self, *args, **kwargs):
        super(SateliteCortesForm, self).__init__(*args, **kwargs)
        if 'satelite' in self.data:
            try:
                idSatelite = int(self.data.get('satelite'))
                if idSatelite is not None:
                    satelite_obj = Satelites.objects.get(idSatelite=idSatelite)
                    self.fields['cortes'].queryset = Corte.objects.filter(satelite=satelite_obj)
            except (ValueError, TypeError, Satelites.DoesNotExist):
                pass

    def clean_cortes(self):
        data = self.cleaned_data.get('cortes')
        satelite = self.cleaned_data.get('satelite')
        if satelite is not None:
            return data.filter(satelite=satelite)
        return data

    
#----------------------------------FlujoInventario----------------------------------
class DetalleFlujoInventarioForm(forms.ModelForm):
    class Meta:
        model = DetalleFlujoInventario
        fields = ['materia_prima', 'cantidad']

DetalleFlujoInventarioFormSet = inlineformset_factory(FlujoInventario, DetalleFlujoInventario, form=DetalleFlujoInventarioForm, extra=1)

class FlujoInventarioForm(forms.ModelForm):
    docEmpleado = forms.ModelChoiceField(queryset=Empleado.objects.all(), label='Empleado', required=False)
    proveedorFlujo = forms.ModelChoiceField(queryset=Proveedor.objects.all(), label='Proveedor', required=False)
    materialFlu = forms.ModelChoiceField(queryset=MateriaPrima.objects.all(), label='Material', required=False)
    flujoCliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente', required=False)
    flujoSatelite = forms.ModelChoiceField(queryset=Satelites.objects.all(), label='Satélite', required=False)
    flujoProducto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto', required=False)
    flujoCorte = forms.ModelChoiceField(queryset=Corte.objects.all(), label='Corte', required=False)
    insumos = forms.ModelMultipleChoiceField(queryset=MateriaPrima.objects.all(), label='Insumos', required=False, widget=forms.CheckboxSelectMultiple)
    flujo = forms.ChoiceField(choices=FlujoInventario.flujos, label='Tipo de flujo', required=False)
    cantidadFlujo = forms.FloatField(label='Cantidad', required=False)

    class Meta:
        model = FlujoInventario
        fields = ['docEmpleado', 'proveedorFlujo', 'materialFlu', 'flujoCliente', 'flujoSatelite', 'flujoProducto', 'flujoCorte', 'insumos', 'flujo', 'cantidadFlujo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def save(self, commit=True):
        flujo_inventario = super().save(commit=False)

        if commit:
            flujo_inventario.save()
            self.save_m2m()
        return flujo_inventario
    
class DetalleFlujoInventarioEditForm(DetalleFlujoInventarioForm):
    class Meta(DetalleFlujoInventarioForm.Meta):
        fields = ['materia_prima', 'cantidad']

DetalleFlujoInventarioEditFormSet = inlineformset_factory(FlujoInventario, DetalleFlujoInventario, form=DetalleFlujoInventarioEditForm, extra=1)

class FlujoInventarioEditForm(FlujoInventarioForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['docEmpleado'].disabled = True

    class Meta(FlujoInventarioForm.Meta):
        fields = ['docEmpleado', 'proveedorFlujo', 'materialFlu', 'flujoSatelite', 'flujoProducto', 'flujoCorte', 'insumos', 'flujo', 'cantidadFlujo']
    
class CorteForm(forms.ModelForm):
    class Meta:
        model = Corte
        fields = ['materialCorte', 'cantidadCorte', 'medida', 'productoCorte']

    def __init__(self, *args, **kwargs):
        cortes_no_entregados = kwargs.pop('cortes_no_entregados', None)
        super(CorteForm, self).__init__(*args, **kwargs)
        if cortes_no_entregados:
            self.fields['productoCorte'].queryset = cortes_no_entregados

    def save(self, commit=True):
        corte = super().save(commit=False)
        if commit:
            # Restar la cantidad del materialCorte
            material = corte.materialCorte
            material.cantidadMaterial -= corte.cantidadCorte
            material.save()
            corte.save()
        return corte    

#----------------------------------MateriaPrima----------------------------------
class MateriaPrimaForm(forms.ModelForm):
    activo = forms.BooleanField(required=False)
    
    class Meta:
        model = MateriaPrima
        fields = ['material', 'cantidadMaterial', 'medida', 'activo']
        
    def update(self, instance):
        instance.material = self.cleaned_data['material']
        instance.cantidadMaterial = self.cleaned_data['cantidadMaterial']
        instance.medida = self.cleaned_data['medida']
        instance.save()

#----------------------------------Productos----------------------------------
class ProductoForm(forms.ModelForm):
    activo = forms.BooleanField(required=False)
    
    class Meta:
        model = Producto
        fields = ['producto', 'cantidadProducto', 'activo']
        
    def update(self, instance):
        instance.producto = self.cleaned_data['producto']
        instance.cantidadProducto = self.cleaned_data['cantidadProducto']
        instance.save()
        
#----------------------------------Productos---------------------------------- 
class DevolucionesForm(forms.ModelForm):
    class Meta:
        model = Devoluciones
        fields = ['devoEmpleado', 'devoSatelite', 'devoProveedor', 'devoProducto', 'devoMaterial', 'flujo', 'motivo', 'cantidadDevo']
        labels = {
            'devoEmpleado': 'Empleado',
            'devoSatelite': 'Satélite',
            'devoProveedor': 'Proveedor',
            'devoProducto': 'Producto',
            'devoMaterial': 'Materia Prima',
            'flujo': 'Flujo',
            'motivo': 'Motivo',
            'cantidadDevo': 'Cantidad de Devolución',
        }
        widgets = {
            # Aquí puedes definir widgets personalizados si es necesario
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer required=False para los campos que no deseas que sean obligatorios
        self.fields['devoSatelite'].required = False
        self.fields['devoProveedor'].required = False
        self.fields['devoProducto'].required = False
        self.fields['devoMaterial'].required = False

#----------------------------------Productos---------------------------------- 
class VentasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VentasForm, self).__init__(*args, **kwargs)
        self.fields['docEmpleado'].queryset = Empleado.objects.filter(cargo__cargo__iexact='vendedor')
    
    docEmpleado = forms.ModelChoiceField(queryset=None, label='Vendedor')
    flujoCliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(activo=True), label='Cliente')
    flujoProducto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo=True), label='Producto')
    flujo = forms.ChoiceField(choices=FlujoInventario.flujos, label='Tipo de flujo')
    cantidadFlujo = forms.FloatField(label='Cantidad')

    class Meta:
        model = FlujoInventario
        fields = ['docEmpleado', 'flujoCliente', 'flujoProducto', 'flujo', 'cantidadFlujo']
    
    def clean(self):
        cleaned_data = super().clean()
        flujo = cleaned_data.get("flujo")
        cantidad_flujo = cleaned_data.get("cantidadFlujo")
        flujo_producto = cleaned_data.get("flujoProducto")

        if flujo == 'venta':
            if flujo_producto.cantidadProducto < cantidad_flujo or flujo_producto.cantidadProducto < 5:
                raise forms.ValidationError(f"No hay suficiente cantidad de {flujo_producto} disponible para realizar la venta.")

class ReporteForm(forms.Form):
    flujo = forms.ChoiceField(choices=[('', '--Selecciona un flujo--'), ('entrada', 'Entrada'), ('salida', 'Salida'), ('venta', 'Venta')], required=False)
    fecha_inicio = forms.DateField(required=False)
    fecha_fin = forms.DateField(required=False)
    
    