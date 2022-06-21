from django import forms
from django.contrib.admin import widgets
from django.forms import fields
from django.forms.forms import Form
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import SelectMultiple
from Veterinaria.models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
	input_type = 'date'


class PacienteForm(forms.ModelForm):
	class Meta:
		model = Paciente
		fields = [
			 'activo','foto','nombrePac','sexo', 'especie','raza','color','fechaNacimPac','observaciones','personaInscrip',
		]
		labels = {
			'activo': 'Activo',
			'foto':'Foto *',
			'nombrePac':'Nombre de Paciente *',
		    'sexo':'Sexo *',
		    'especie':'Especie *',
		    'raza':'Raza *',
		    'color':'Color *',
		    'fechaNacimPac':'Fecha de Nacimiento *',
            'observaciones':'Observaciones',
			'personaInscrip':'Persona que Inscribió *'
		}
		widgets = {
			'observaciones':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
			'fechaNacimPac': DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control',}),
		}


		
class PropietarioForm(forms.ModelForm):
	class Meta:
		model = Propietario
		fields = [
			'dui','nombre', 'apellido','fechaNacim','edad','direccion','departamento','municipio','telefono','correo',
		]
		labels = {
			'dui':'Número de DUI*',
			'nombre':'Nombre*',
			'apellido':'Apellido*',
		    'fechaNacim':'Fecha de Nacimiento*',
            'edad':'Edad*',
            'direccion':'Dirección*',
            'departamento':'Departamento*',
            'municipio':'Municipio*',
            'telefono':'Telefono*',
            'correo':'Correo Electrónico*',
		}
		widgets = {
			'edad':forms.TextInput(attrs={'class':'form-contol'}),
			'fechaNacim': DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control'}),
		}

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',"first_name","last_name", "email", "password1","password2"]

class ClinicaForm(forms.ModelForm):
    class Meta:
        model = Clinica
        fields = [
			'propietario','nombre','direccion', 'horarios', 'telefono', 'correoElectronico', 'estado',
		]

class ConsultorioForm(forms.ModelForm):
        # servicios = forms.ModelMultipleChoiceField(
        #         widget = forms.CheckboxSelectMultiple(attrs={'rows':3}),
        #         queryset = Servicio.objects.all()
        #     )

        class Meta:
            model = Consultorio
            fields = '__all__'
		    
        direccion = forms.Textarea(
			#widget=forms.Textarea(attrs={'rows':3}),
		)

class EmpleadoForm(forms.ModelForm):
	class Meta:
		model = Empleado
		fields = [
			'duiEmp','nombreEmp', 'apellidoEmp','telefonoEmp','cargo','salario','clinica','consultorio',
		]
		labels = {
			'duiEmp':'Número de DUI*',
			'nombreEmp':'Nombre*',
			'apellidoEmp':'Apellido*',
            'telefonoEmp':'Telefono*',
            'cargo':'Cargo que Desempeña*',
			'salario':'Salario*',
			'clinica':'Clínica *',
			'consultorio':'Consultorio en que Trabaja*',
		}

class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitudes
		fields = [
			'solicitante','nombreClinica', 'direccionClinica', 'horariosClinica', 'telefonoClinica','serviciosClinica',
		]
		labels = {
			'solicitante':'Nombre del Dueño',
			'nombreClinica':'Nombre de la Clínica',
			'direccionClinica':'Dirección',
            'horariosClinica':'Horarios',
            'telefonoClinica':'Telefono',
			'serviciosClinica':'Servicios que Presta',
		}
		widgets = {
			'horariosClinica':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
			'serviciosClinica':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
		}


class HorarioForm(forms.ModelForm):
	class Meta:
		model = Horario
		fields = [
			 'clinica','hora','indicador','activo',
		]
		labels = {
			'clinica':'Clínica *',
			'hora':'Hora *',
			'indicador':'Indicador *',
			'activo':'Activo ',
		}


class CitaForm(forms.ModelForm):
	class Meta:
		model = Cita
		fields = [
			 'pacienteId','clinica','consultorio','servicio','fechaCita','horaCita',
		]
		labels = {
			'pacienteId':'Paciente *',
			'clinica':'Clínica *',
			'consultorio':'Consultorio *',
			'servicio':'Servicios Solicitados *',
			'fechaCita':'Fecha de Cita *',
		    'horaCita':'Hora de Cita *',
		}
		widgets = {
			'fechaCita': DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control',}),
		}

class SoloPacienteForm(forms.ModelForm):
	class Meta:
		model = Paciente
		fields = [
			 'activo','foto','nombrePac','sexo', 'especie','raza','color','fechaNacimPac','observaciones','personaInscrip','propietario',
		]
		labels = {
			'activo': 'Activo',
			'foto':'Foto *',
			'nombrePac':'Paciente *',
		    'sexo':'Sexo *',
		    'especie':'Especie *',
		    'raza':'Raza *',
		    'color':'Color *',
		    'fechaNacimPac':'Fecha de Nacimiento *',
            'observaciones':'Observaciones',
			'personaInscrip':'Persona que Inscribió *',
			'propietario':'Propietario *',
		}
		widgets = {
			'observaciones':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
			'fechaNacimPac': DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control',}),
		}

class ConsultaForm(forms.ModelForm):
	class Meta:
		model = Consulta
		fields = [
			 'medico','pacienteId','edad','peso','hora','observaciones','medicamento','examenes', 'clinica','consultorio','proximoCont',
		]
		labels = {
			'medico': 'Medico Veterinario *',
			'pacienteId':'Paciente *',
			'edad':'Edad *',
			'peso':'Peso *',
			'hora':'Hora *',
			'observaciones':'Observaciones',
			'medicamento':'Medicamentos',
			'examenes':'Exámenes',
			'clinica':'Clínica *',
			'consultorio':'Consultorio *',
			'proximoCont':'Proximo Control *',
		}
		widgets = {
			'observaciones':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
			'medicamento':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
			'examenes':forms.Textarea(attrs={'class':'form-contol','rows':'4'}),
			'proximoCont': DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control',}),
		}

class ExpedienteForm(forms.ModelForm):
	class Meta:
		model = Expediente
		fields = [
			 'clinica','consultorio',
		]
		labels = {
			'clinica':'Clínica *',
			'consultorio':'Consultorio *',
		}

class ServicioForm(forms.ModelForm):
	class Meta:
		model = Servicio
		fields = [
			'nombreServicio','descServicio','catServicio', 'estadoServicio', 
		]
		labels = {
			'nombreServicio':'Nombre del servicio',
			'descServicio':'Descripción',
			'catServicio':'Categoria',
			'estadoServicio':'Estado',
		}
		widgets = {
			'descServicio':forms.Textarea(attrs={'class':'form-contol', 'rows':'4'}),
		}

class SolicitudServicioForm(forms.ModelForm):
	class Meta:
		model = SolicitudServicio
		fields = [
			'solicitante','nombreClinica','nombreServicio','razonSolicitud','catSolicitud',
		]
		labels = {
			'solicitante':'Nombre del Dueño*',
			'nombreClinica':'Nombre de la Clínica*',
			'nombreServicio':'Nombre del servicio*',
			'razonSolicitud':'Razón de la solicitud*',
			'catSolicitud':'Categoría sugerida de su solicitud*',
		}
		widgets = {
			'razonSolicitud':forms.Textarea(attrs={'rows':'4'}),
		}

class VacunaForm(forms.ModelForm):
	class Meta:
		model = Vacuna
		fields = [
			 'paciente','nombre','lote','fechaProx','aplicador',
		]
		labels = {
			'paciente':'Paciente *',
			'nombre':'Nombre Vacuna *',
			'lote':'Lote Vacuna *',
			'fechaProx':'Próxima Aplicación *',
			'aplicador':'Médico que la Aplicó *',
		}
		widgets = {
			'fechaProx': DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control',}),
		}