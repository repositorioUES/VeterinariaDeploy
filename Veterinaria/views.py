from django.views.generic.edit import View, UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import View, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from xhtml2pdf import pisa

from Veterinaria.forms import *
from .filters import *
from .forms import CustomUserCreationForm, ClinicaForm


# Create your views here.
def index(request):
    return render(request, 'index.html')

# Vista REGISTRAR USUARIO -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
def registro(request):
    data={
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario=CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user=authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request, "Registro exitoso")
            return redirect(to="index")
        data["form"]=formulario
    return render(request, 'registration/registro.html', data)

# Vista REGISTRAR CLINICA -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def registrar_clinica(request):

    data = {
        'form' : ClinicaForm()
    }

    if request.method == 'POST':
        formulario=ClinicaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Clinica registrada exitosamente")
            return redirect(to="listar_clinica")
        else:
            data['form'] = formulario
    return render(request, 'clinica/agregarClinica.html',data)

# Vista LISTAR CLINICA  -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def listar_clinica(request):
    clinicas = Clinica.objects.all()
    page = request.GET.get('page',1)

    clinicasId = [] #Arreglo para guardar los id's de las clinicas que si tienen registros asociados
    expedientes = Expediente.objects.all()
    consultorios = Consultorio.objects.all()
    empleados = Empleado.objects.all()
    horarios = Horario.objects.all()
    citas = Cita.objects.all()
    consultas = Consulta.objects.all()

    for ex in expedientes:
        clinicasId.append(ex.clinica_id)
    
    for c in consultorios:
        clinicasId.append(c.clinica_id)
    
    for em in empleados:
        clinicasId.append(em.clinica_id)

    for h in horarios:
        clinicasId.append(h.clinica_id)

    for ci in citas:
        clinicasId.append(ci.clinica_id)

    for co in consultas:
        clinicasId.append(co.clinica_id)
    
    clinicasId = set(clinicasId)

    filter = ClinicaFilter(request.GET, queryset=clinicas)
    clinicas = filter.qs

    try:
        paginator = Paginator(clinicas,10)
        clinicas = paginator.page(page)

    except:
        raise Http404

    data = {
        'entity': clinicas,
        'paginator': paginator,
        'filter' : filter,
        'clinicasId' : clinicasId
    }

    return render(request, 'clinica/listarClinica.html', data)

# Vista MODIFICAR CLINICA  -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def modificar_clinica(request, id):

    clinica = get_object_or_404(Clinica, id=id)
    data ={
        'form' : ClinicaForm(instance=clinica)
    }

    if request.method == 'POST':
        formulario = ClinicaForm(data=request.POST, instance=clinica)
        if formulario.is_valid():
            formulario.save()
            messages.success(request," Modificado correctamente")
            return redirect(to="listar_clinica")
        data['form'] = formulario
    return render(request, 'clinica/modificarClinica.html', data)

# Vista ELIMINAR CLINICA  -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def eliminar_clinica(request, id):
    clinica = get_object_or_404(Clinica, id=id)
    clinica.delete()
    messages.success(request," Clinica eliminada correctamente")
    return redirect(to="listar_clinica")

# Vista REGISTRAR CONSULTORIO -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def registrar_consultorio(request, id):
    clinica = Clinica.objects.get(id=id)
    data = {
        'form' : ConsultorioForm(initial={'clinica': clinica})
    }

    if request.method == 'POST':
        formulario=ConsultorioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Consultorio registrado exitosamente")
            return redirect('listar_consultorio', clinica.id )
        else:
            data['form'] = formulario
    return render(request, 'consultorio/agregarConsultorio.html',data)

# Vista LISTAR CONSULTORIO  -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def listar_consultorio(request,id):
    clinica = Clinica.objects.get(id=id)
    consultorios = clinica.consultorio_set.all()

    empleados = clinica.empleado_set.all()

    filter = ConsultorioFilter(request.GET, queryset=consultorios)
    consultorios = filter.qs

    filter2 = EmpleadoFilter(request.GET, queryset=empleados)
    empleados = filter2.qs

    consultoriosId = [] #Arreglo para guardar los id's de las clinicas que si tienen registros asociados
    expedientes = Expediente.objects.all()
    emp = Empleado.objects.all()
    citas = Cita.objects.all()
    consultas = Consulta.objects.all()

    for ex in expedientes:
        consultoriosId.append(ex.consultorio_id)
    
    for em in emp:
        consultoriosId.append(em.consultorio_id)

    for ci in citas:
        consultoriosId.append(ci.consultorio_id)

    for co in consultas:
        consultoriosId.append(co.consultorio_id)
    
    consultoriosId = set(consultoriosId)

    data = {
        'clinica' : clinica,
        'consultorios' : consultorios,
        'filter' : filter,
        'filter2' : filter2,
        'empleados' : empleados,
        'consultoriosId':consultoriosId,
    }
    
    return render(request, 'consultorio/listarConsultorio.html', data)

# Vista MODIFICAR CONSULTORIO  -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def modificar_consultorio(request, id):

    consultorio = get_object_or_404(Consultorio, id=id)
    data ={
        'form' : ConsultorioForm(instance=consultorio)
    }

    if request.method == 'POST':
        formulario = ConsultorioForm(data=request.POST, instance=consultorio)
        if formulario.is_valid():
            formulario.save()
            messages.success(request," Consultorio modificado correctamente")
            return redirect('listar_consultorio', consultorio.clinica.id)
        data['form'] = formulario
    return render(request, 'consultorio/modificarConsultorio.html', data)

# Vista ELIMINAR CONSULTORIO  -------------------------------------------------------------------
#Programador y Analista: Christian Garcia
@login_required
def eliminar_consultorio(request, id):
    consultorio = get_object_or_404(Consultorio, id=id)
    consultorio.delete()
    messages.success(request," Consultorio eliminado correctamente")
    return redirect('listar_consultorio', consultorio.clinica.id)

# Vista REGISTRAR PACIENTE -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
class RegistrarPaciente(CreateView):
    model = Paciente
    template_name = 'Plantillas/registrarPaciente.html'
    form_class = PacienteForm
    second_form_class = PropietarioForm
    third_form_class = ExpedienteForm
    success_url = reverse_lazy('listado_pacientes')

    def get_context_data (self , **kwargs):
        context = super(RegistrarPaciente, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        return context
    
    def post (self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        form2 = self.second_form_class(request.POST, request.FILES or None)
        form3 = self.third_form_class(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            paciente = form.save(commit=False)
            paciente.propietario = form2.save()
            paciente.activo = 1
            expediente = form3.save(commit=False)
            expediente.pacienteId = form.save()
            expediente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form = form, form2 = form2, form3 = form3))

# Vista MODIFICAR PACIENTE -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
class ModificarPaciente(UpdateView):
    model = Paciente
    second_model = Propietario
    template_name = 'Plantillas/modificarPaciente.html'
    form_class = PacienteForm
    second_form_class = PropietarioForm
    success_url = reverse_lazy('listado_pacientes')

    def get_context_data (self , **kwargs):
        context = super(ModificarPaciente, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        paciente = self.model.objects.get(id=pk)
        propietario = self.second_model.objects.get(dui=paciente.propietario_id)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=propietario)
        context['id'] = pk
        return context
    
    def post (self, request, *args, **kwargs):
        self.object = self.get_object
        id_paciente = kwargs['pk']
        paciente = self.model.objects.get(id=id_paciente)
        propietario = self.second_model.objects.get(dui=paciente.propietario_id)
        form = self.form_class(request.POST, request.FILES, instance=paciente)
        form2 = self.second_form_class(request.POST, request.FILES or None, instance=propietario)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            #paciente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form = form, form2 = form2))
    
# Vista DETALLE DE PACIENTES -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
def DetallePaciente(request,pk):
    paciente = Paciente.objects.get(id = pk)
    consultas = Consulta.objects.filter(pacienteId_id = paciente.id).first() # Vemos si tiene almenos 1 consulta
    citas = Cita.objects.filter(pacienteId_id = paciente.id).first() # Vemos si tiene almenos 1 cita
    vacunas = Vacuna.objects.filter(paciente_id = paciente.id).first() # Vemos si tiene almenos 1 vacuna
    
    if consultas or citas or vacunas: # Si tiene almenos 1 cita y/o 1 consulta y/o vacuna
        borrar = 0 #No lo podremos borrar
    else:
        borrar = 1 # Si no tiene ni una cita y consulta, si se podrá borrar

    return render(request, 'Plantillas/detallePaciente.html', {'paciente':paciente,'borrar':borrar})

# Vista ELIMINAR PACIENTE -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
@login_required
def eliminarPaciente(request, pk):
    paciente = Paciente.objects.get(id = pk) # Buscamos al paciente
    expediente = Expediente.objects.get(pacienteId_id = paciente.id) # Buscamos su expediente

# Si el propietario solo tienen 1 mascota registrada, al borrar la mascota se borrará el propietario
# Si tiene 2 o +, NO se borrará el propietario.
    propietario = Propietario.objects.get(dui = paciente.propietario_id)# Obtener al propietario del paciente.
    mascotas = Paciente.objects.filter(propietario_id = propietario.dui) 
    cantidadMascotas = 0 # Acumulador de cantidad de mascotas de este propietario

    for m in mascotas:
        cantidadMascotas += 1

    if request.method == 'POST':
        if cantidadMascotas == 1: # Si tiene solo 1 mascotas
            propietario.delete() # Se borra el propietario
            print(cantidadMascotas)
    
        expediente.delete() # Borramos 1º al Expediente para que no de error por la FK protegida
        paciente.delete() # Borramos al paciente
        return redirect('listado_pacientes')

    return render(request,'Plantillas/eliminarPaciente.html', {'paciente':paciente, 'cant':cantidadMascotas})

# Vista LSITADO DE PACIENTES -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
class ListadoPacientes(ListView):
    model = Paciente
    template_name = 'Plantillas/listadoPacientes.html'
    context_object_name = 'pacientes'

# Vista BUSCAR PACIENTE -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
def BuscarPaciente(request):
    queryset = request.GET.get('buscar')
    context={}
    if queryset:
        pacientes = Paciente.objects.filter(nombrePac__icontains=queryset)
        if pacientes:
            context = {'pacientes':pacientes}
        else:
            p = Propietario.objects.filter(Q(nombre__icontains=queryset) | Q(apellido__icontains=queryset) | Q(dui=queryset))
            if p:
                for prop in p:
                    pacientes |= Paciente.objects.filter(propietario_id=prop.dui)
                context = {'pacientes':pacientes}
        
    return render(request,'Plantillas/buscarPaciente.html', context)

# Vista DETALLE DE PROPIETARIO -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
class DetallePropietario(DetailView):
    model = Propietario
    template_name = 'Plantillas/detallePropietario.html'
    form_class = PropietarioForm
    context_object_name = 'prop'

class CrearEmpleado(CreateView):
    model = Empleado
    template_name = 'Plantillas/crearEmpleado.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('listado_empleados')

class ListarEmpleados(ListView):
    model = Empleado
    template_name = 'Plantillas/listadoEmpleados.html'
    context_object_name = 'empleados'

class DetalleEmpleado(DetailView):
    model = Empleado
    template_name = 'Plantillas/detalleEmpleado.html'
    form_class = EmpleadoForm
    context_object_name = 'empleado'

@login_required
def cambiarEstadoEmpleado(request, duiEmp):
    empleado = Empleado.objects.filter(duiEmp = duiEmp).first()

    if request.method == 'POST':
        if empleado.activo == True:
            empleado.activo = False
        else:
            empleado.activo = True

        empleado.save()

        return redirect('listado_empleados')
    return render(request,'Plantillas/modificarEmpleado.html', {'empleado':empleado})

class CrearSolicitud(CreateView):
    model = Solicitudes
    template_name = 'Plantillas/crearSolicitud.html'
    form_class = SolicitudForm
    success_url = reverse_lazy('solicitud_enviada')

def SolicitudEnviada(request):
    return render(request, 'Plantillas/solicitudEnviada.html')

class ListarSolicitudes(ListView):
    model = Solicitudes
    template_name = 'Plantillas/listadoSolicitudes.html'
    context_object_name = 'solicitudes'

class DetalleSolicitud(DetailView):
    model = Solicitudes
    template_name = 'Plantillas/detalleSolicitud.html'
    form_class = SolicitudForm
    context_object_name = 'solicitud'


# REGISTARA SOLO PACIENTE  -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
def TipoRegistro(request):
    return render(request, 'Plantillas/tipoRegistro.html')

class RegistrarSoloPaciente(CreateView):
    model = Paciente
    template_name = 'Plantillas/registrarSoloPaciente.html'
    form_class = SoloPacienteForm
    second_form_class = ExpedienteForm
    success_url = reverse_lazy('listado_pacientes')

    def get_context_data (self , **kwargs):
        context = super(RegistrarSoloPaciente, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    
    def post (self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        form2 = self.second_form_class(request.POST, request.FILES or None)
        if form.is_valid() and form2.is_valid():
            expediente = form2.save(commit=False)
            form.activo = 1
            expediente.pacienteId = form.save()
            expediente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form = form, form2 = form2))

def PacientesInactivos(request):
    pacientes = Paciente.objects.filter(activo = 0)
    return render(request,'Plantillas/pacientesInactivos.html', {'pacientes':pacientes})

##  CITAS-------------------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
class CrearCita(CreateView):
    model = Cita
    template_name = 'Plantillas/crearCita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listado_citas')

class ModificarCita(UpdateView):
    model = Cita
    template_name = 'Plantillas/modificarCita.html'
    form_class = CitaForm
    success_url = reverse_lazy('listado_citas')

def ListadoCitas(request):
    hoy = datetime.now().date() # Fecha de hoy
    citasHoy = Cita.objects.filter(fechaCita__contains = hoy) # Citas SOLO de HOY
    return render(request,'Plantillas/listadoCitas.html', {'citasHoy':citasHoy})

# Vista BUSCAR CITA -------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
def BuscarCita(request):
    pac = request.GET.get('buscar') # Filtro por paciente
    fec = request.GET.get('buscarFecha') # Filtro por fecha
    cli = request.GET.get('buscarClinica') # Filtro por clinica

    citasHoy = Cita.objects.none()
    citasFuturo = Cita.objects.none()
    citasPasado = Cita.objects.none()


    context={}
    hoy = datetime.now().date() # Fecha de hoy

    paciente = Paciente.objects.filter(nombrePac__iexact = pac).first()
    clinica = Clinica.objects.filter(nombre__iexact = cli).first()
    
    if pac!="" and fec!="" and cli!="": # Si mandamos info en los 3 campos
        if paciente and clinica:
            citasHoy = Cita.objects.filter(fechaCita__contains = hoy).filter(pacienteId=paciente.id).filter(fechaCita__contains = fec).filter(clinica_id = clinica.id) # Cita para Hoy
            citasFuturo = Cita.objects.filter(fechaCita__gt = hoy).filter(pacienteId=paciente.id).filter(fechaCita__contains = fec).filter(clinica_id = clinica.id) # Citas a Futuro
            citasPasado = Cita.objects.filter(fechaCita__lt = hoy).filter(pacienteId=paciente.id).filter(fechaCita__contains = fec).filter(clinica_id = clinica.id) # Citas ya Pasadas
    else:
        if pac!="" and cli!="": # Si mandamos solo paciente y clinica
            if paciente and clinica:
                citasHoy = Cita.objects.filter(fechaCita__contains = hoy).filter(pacienteId=paciente.id).filter(clinica_id = clinica.id) # Cita para Hoy
                citasFuturo = Cita.objects.filter(fechaCita__gt = hoy).filter(pacienteId=paciente.id).filter(clinica_id = clinica.id) # Citas a Futuro
                citasPasado = Cita.objects.filter(fechaCita__lt = hoy).filter(pacienteId=paciente.id).filter(clinica_id = clinica.id) # Citas ya Pasadas
               
        if pac!="" and fec!="": # Si mandamos solo paciente y fecha
            if paciente:
                citasHoy = Cita.objects.filter(fechaCita__contains = fec).filter(fechaCita__contains = hoy).filter(pacienteId=paciente.id) # Cita para Hoy
                citasFuturo = Cita.objects.filter(fechaCita__icontains = fec).filter(fechaCita__gt=hoy).filter(pacienteId=paciente.id)
                citasPasado = Cita.objects.filter(fechaCita__icontains=fec).filter(fechaCita__lt=hoy).filter(pacienteId=paciente.id)
                
        if fec!="" and cli!="": # Si solo mandamos fecha y clinica
            if clinica:
                citasHoy = Cita.objects.filter(clinica_id = clinica.id).filter(fechaCita__icontains = fec).filter(fechaCita__contains=hoy)
                citasFuturo = Cita.objects.filter(clinica_id = clinica.id).filter(fechaCita__icontains = fec).filter(fechaCita__gt=hoy)
                citasPasado = Cita.objects.filter(clinica_id = clinica.id).filter(fechaCita__icontains=fec).filter(fechaCita__lt=hoy)
                
        if pac and fec=="" and cli=="": # Si mandamos solo paciente
            if paciente:
                citasHoy = Cita.objects.filter(fechaCita__contains = hoy).filter(pacienteId=paciente.id) # Cita para Hoy
                citasFuturo = Cita.objects.filter(fechaCita__gt=hoy).filter(pacienteId=paciente.id)
                citasPasado = Cita.objects.filter(fechaCita__lt=hoy).filter(pacienteId=paciente.id)

        if cli and fec=="" and pac=="": # Si mandamos solo clinica
            if clinica:
                citasHoy = Cita.objects.filter(fechaCita__contains = hoy).filter(clinica_id = clinica.id) # Cita para Hoy
                citasFuturo = Cita.objects.filter(fechaCita__gt = hoy).filter(clinica_id = clinica.id) # Citas a Futuro
                citasPasado = Cita.objects.filter(fechaCita__lt = hoy).filter(clinica_id = clinica.id) # Citas ya Pasadas
               
        if fec and pac=="" and cli=="": # Si solo mandamos fecha
            citasHoy = Cita.objects.filter(fechaCita__contains = fec).filter(fechaCita__contains=hoy)
            citasFuturo = Cita.objects.filter(fechaCita__contains = fec).filter(fechaCita__gt=hoy)
            citasPasado = Cita.objects.filter(fechaCita__icontains=fec).filter(fechaCita__lt=hoy)

    if citasHoy.exists() or citasFuturo.exists() or citasPasado.exists():   
        context = {'citasHoy':citasHoy,'citasFuturo':citasFuturo,'citasPasado':citasPasado}
   
    return render(request,'Plantillas/buscarCita.html', context)

@login_required
def DetalleCita(request, pk):
    cita = Cita.objects.get(id = pk)
    servicios = Servicio.objects.filter(cita__id = cita.id)
    print(servicios)
    return render(request, 'Plantillas/detalleCita.html', {'cita':cita,'servicios':servicios})

@login_required
def DetalleCitaPasada(request, pk):
    cita = Cita.objects.get(id = pk)
    servicios = Servicio.objects.filter(cita__id = cita.id)
    print(servicios)
    return render(request, 'Plantillas/detalleCitaPasada.html', {'cita':cita,'servicios':servicios})

class CancelarCita(DeleteView):
    template_name = 'Plantillas/cancelarCita.html'
    model = Cita
    success_url = reverse_lazy('listado_citas')

## HORARIOS-------------------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
class CrearHorario(CreateView):
    model = Horario
    template_name = 'Plantillas/crearHorario.html'
    form_class = HorarioForm
    success_url = reverse_lazy('listado_horarios')

@login_required
def cambiarEstadoHorario(request, pk):
    horario = Horario.objects.filter(id = pk).first()

    if request.method == 'POST':
        if horario.activo == True:
            horario.activo = False
        else:
            horario.activo = True

        horario.save()

        return redirect('listado_horarios')
    return render(request,'Plantillas/modificarHorario.html', {'horario':horario})

def ListadoHorarios(request):
    horarios = Horario.objects.all().order_by('id')
    citas = Cita.objects.all()
    horaCita = Horario.objects.none()
    horaBorrar = Horario.objects.none()

    for c in citas:
        horaCita |= Horario.objects.filter(id = c.horaCita_id)

    horaId = []
    for hC in horaCita:
        horaId.append(hC.id)

    for h in horarios:
        if h.id not in horaId:
            horaBorrar |= Horario.objects.filter(id = h.id)
    
    return render(request, 'Plantillas/listadoHorarios.html', {'horarios':horarios, 'horaBorrar':horaBorrar})

def HorariosInactivos(request):
    horarios = Horario.objects.filter(activo = 0)
    citas = Cita.objects.all()
    horaCita = Horario.objects.none()
    horaBorrar = Horario.objects.none()

    for c in citas:
        horaCita |= Horario.objects.filter(id = c.horaCita_id)

    horaId = []
    for hC in horaCita:
        horaId.append(hC.id)

    for h in horarios:
        if h.id not in horaId:
            horaBorrar |= Horario.objects.filter(id = h.id)

    return render(request,'Plantillas/horariosInactivos.html', {'horarios':horarios, 'horaBorrar':horaBorrar})

@login_required
def borrarHorario(request, pk):
    horario = Horario.objects.filter(id = pk).first()

    if request.method == 'POST':
        horario.delete()

        return redirect('listado_horarios')
    return render(request,'Plantillas/borrarHorario.html', {'horario':horario})

## CONSULTA-------------------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez 
@login_required
def RegistrarConsulta(request, pk):
    paciente = Paciente.objects.get(id=pk)
    data = {
        'form' : ConsultaForm(initial={'pacienteId': paciente})
    }

    if request.method == 'POST':
        formulario=ConsultaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('expediente', paciente.id )
        else:
            data['form'] = formulario
    return render(request, 'Plantillas/registrarConsulta.html',data)
    
class DetalleConsulta(DetailView):
    model = Consulta
    template_name = 'Plantillas/detalleConsulta.html'
    form_class = ConsultaForm
    context_object_name = 'consulta'

## EXPEDIENTE-------------------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez
def DetalleExpediente (request, pk):
    vacunas = Vacuna.objects.filter(paciente_id = pk)
    sinVacunas = 0

    if request.method == 'GET':
        if vacunas.exists() == False: # Si no tiene vacunas
            sinVacunas = 1 #Ponemos esto a 1
    
        exp = Expediente.objects.filter(pacienteId_id = pk).first()
        consultas = Consulta.objects.filter(pacienteId_id = pk)

    return render(request, 'Plantillas/detalleExpediente.html', {'exp':exp,'cons':consultas,'sinVacunas':sinVacunas,'vacunas':vacunas})

class CrearServicio(CreateView):
    model = Servicio
    template_name = 'Plantillas/crearServicio.html'
    form_class = ServicioForm
    success_url = reverse_lazy('listado_servicios')

class ListarServicio(ListView):
    model = Servicio
    template_name = 'Plantillas/listadoServicios.html'
    context_object_name = 'servicios'

def ServiciosInactivos(request):
    servicios = Servicio.objects.filter(estadoServicio = 'Inactiva')
    return render(request,'Plantillas/serviciosInactivos.html', {'servicios':servicios})

class DetalleServicio(DetailView):
    model = Servicio
    template_name = 'Plantillas/detalleServicio.html'
    form_class = ServicioForm
    context_object_name = 'servicio'

class ModificarServicio(UpdateView):
    model = Servicio
    template_name = 'Plantillas/modificarServicio.html'
    form_class= ServicioForm
    success_url = reverse_lazy('listado_servicios')

def ServiciosParaBorrar(request):
    citas = Cita.objects.all()
    servicios = Servicio.objects.filter(estadoServicio='Activa')
    asignados = Servicio.objects.none()
    noAsignados = Servicio.objects.none()

    for c in citas:
        asignados |= Servicio.objects.filter(cita__id = c.id)
    idAsignados = []

    for a in asignados:
        idAsignados.append(a.idServicio)
    
    for s in servicios:
        if s.idServicio not in idAsignados:
            noAsignados |= Servicio.objects.filter(idServicio = s.idServicio)
    
    return render(request, 'Plantillas/serviciosParaBorrar.html',{'servicios':noAsignados})

class BorrarServicio(DeleteView):
    model = Servicio
    template_name = 'Plantillas/borrarServicio.html'
    success_url = reverse_lazy('listado_servicios')

class CrearSolicitudServicio(CreateView):
    model = SolicitudServicio
    template_name = 'Plantillas/crearSolicitudServicio.html'
    form_class = SolicitudServicioForm
    success_url = reverse_lazy('solicitud_servicio_enviado')

def SolicitudServicioEnviado(request):
    return render(request, 'Plantillas/solicitudServicioEnviado.html')

class ListarSolicitudServicio(ListView):
    model = SolicitudServicio
    template_name = 'Plantillas/listadoSolicitudServicio.html'
    context_object_name = 'soliservicios'

class DetalleSolicitudServicio(DetailView):
    model = SolicitudServicio
    template_name = 'Plantillas/detalleSolicitudServicio.html'
    form_class = SolicitudServicioForm
    context_object_name = 'soliservi'

## VACUNAS -------------------------------------------------------------------------------
#Programador y Analista: Ruddy Alfredo Pérez 
@login_required
def AgregarVacuna(request, pk):
    paciente = Paciente.objects.get(id=pk)
    vacunas = Vacuna.objects.filter(paciente_id = paciente.id)
    sinVacunas = 0

    if vacunas.exists() == False: # Si no tiene vacunas
        sinVacunas = 1 #Ponemos esto a 1

    data = {
        'form' : VacunaForm(initial={'paciente': paciente}),
        'vacunas':vacunas,
        'sinVacunas':sinVacunas,
        'paciente':paciente,
    }
       
    if request.method == 'POST':
        formulario=VacunaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('expediente', paciente.id )
        else:
            data['form'] = formulario
            data['vacunas'] = vacunas
            data['sinVacunas'] = sinVacunas
            data['paciente'] = paciente

    return render(request, 'Plantillas/agregarVacuna.html',data)



class reportePaciente(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:
            
            template = get_template('reportePaciente.html')
            context = {'titulo1': 'Asociación de Veterinarios de El Salvador',
                        'titulo2' : 'Ficha de Identificación de Paciente',
                        'paciente' : Paciente.objects.get( pk=self.kwargs['pk']),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('listado_pacientes'))


class reporteConsulta(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:
            
            template = get_template('reporteConsulta.html')
            context = {'titulo1': 'Asociación de Veterinarios de El Salvador',
                        'JVPMV' : 'JVPMV ####',
                        'titulo2' : 'Servicio Medico Veterinario y Quirurjurgico',
                        'consulta' : Consulta.objects.get( pk=self.kwargs['pk']),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('expediente'))


class reporteVacuna(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:
            
            template = get_template('reporteVacuna.html')
            context = {'vacuna' : Vacuna.objects.get( pk=self.kwargs['pk']),
                        'paciente' : Paciente.objects.get( pk=self.kwargs['pk']),
                        'vacunas' : Vacuna.objects.filter(pk = self.kwargs['pk']),
                        'consulta' : Consulta.objects.get( pk=self.kwargs['pk']),

            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('expediente'))

@login_required
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, duiEmp = id)

    if request.method == 'POST':
        empleado.delete()
        messages.success(request," Empleado eliminado correctamente")
        return redirect('listado_empleados')
    return render(request,'Plantillas/borrarEmpleado.html', {'empleado':empleado})

@login_required
def eliminar_solicitud_servicio(request, id):
    solicitud = get_object_or_404(SolicitudServicio, id=id)

    if request.method == 'POST':
        solicitud.delete()
        messages.success(request," Solicitud de Servicio eliminada correctamente")
        return redirect('listado_solicitud_servicio')
    return render(request,'Plantillas/borrarSolicitudServicio.html', {'solicitud':solicitud})

@login_required
def eliminar_solicitud_ingreso(request, id):
    solicitud = get_object_or_404(Solicitudes, id=id)

    if request.method == 'POST':
        solicitud.delete()
        messages.success(request," Solicitd de Ingreso eliminada correctamente")
        return redirect('listado_solicitudes')
    return render(request,'Plantillas/borrarSolicitudIngreso.html', {'solicitud':solicitud})

@login_required
def Consolidados(request, pk):
    clinica = Clinica.objects.get(id = pk)
    return render(request,'Plantillas/consolidados.html', {'clinica':clinica})

@login_required
def ConsolidadosAsoc(request):
    return render(request,'Plantillas/consolidadosAsoc.html')

class reportePorMedico(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:

            clinica = Clinica.objects.get(id=self.kwargs['pk'])
            consultas = Consulta.objects.filter(clinica_id=self.kwargs['pk'])
            medicos = []

            for c in consultas:
                medicos.append(c.medico)

            medicos = set(medicos)
            print(medicos)
            
            template = get_template('reportePorMedico.html')
            context = {'medicos' : medicos,
                        'consultas' : consultas,
                        'titulo1': 'Asociación de Veterinarios de El Salvador',
                        'titulo2' : 'Servicio Medico Veterinario y Quirurjurgico',
                        'titulo3' : 'Consolidado de Consultas Atendidas Por cada Médico en la Clinica: ' + str(clinica.nombre),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('consolidados'))

class reportePorFecha(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:
            clinica = Clinica.objects.get(id=self.kwargs['pk'])
            consultas = Consulta.objects.filter(clinica_id=self.kwargs['pk'])
            fechas = []

            for c in consultas:
                fechas.append(c.fechaConsulta)

            fechas = set(fechas)
            print(fechas)
            
            template = get_template('reportePorFecha.html')
            context = {'fechas' : fechas,
                        'consultas' : consultas,
                        'titulo1': 'Asociación de Veterinarios de El Salvador',
                        'titulo2' : 'Servicio Medico Veterinario y Quirurjurgico',
                        'titulo3' : 'Consolidado de Consultas Atendidas Por Fecha de la Clínica: ' + str(clinica.nombre),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('consolidados'))

class reportePorClinica(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:

            consultas = Consulta.objects.all()
            clinicas = Clinica.objects.all()
            clinicasId = []

            for c in consultas:
                clinicasId.append(c.clinica_id)

            clinicasId = set(clinicasId)
            print(clinicasId)
            
            template = get_template('reportePorClinica.html')
            context = {'clinicasId' : clinicasId,
                        'consultas' : consultas,
                        'clinicas' : clinicas,
                        'titulo1': 'Asociación de Veterinarios de El Salvador',
                        'titulo2' : 'Servicio Medico Veterinario y Quirurjurgico',
                        'titulo3' : 'Consolidado de Consultas Atendidas Por Clínica',
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('consolidados'))

class reportePorFechaAsoc(View):

    def link_callback(self,uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


    def get(self,request, *args, **kwargs):
        try:
           
            consultas = Consulta.objects.all()
            fechas = []

            for c in consultas:
                fechas.append(c.fechaConsulta)

            fechas = set(fechas)
            print(fechas)
            
            template = get_template('reportePorFecha.html')
            context = {'fechas' : fechas,
                        'consultas' : consultas,
                        'titulo1': 'Asociación de Veterinarios de El Salvador',
                        'titulo2' : 'Servicio Medico Veterinario y Quirurjurgico',
                        'titulo3' : 'Consolidado de Consultas Atendidas Por Fecha de Todas las Clínicas',
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response,link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('consolidados'))