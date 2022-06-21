"""ProyectoVeterinaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from Veterinaria.views import *
from Veterinaria.ajax import load_Municipios, load_Propietario, load_Paciente, load_Clinica, load_Horarios, load_Consultorio,  load_Consultorio_Edit, load_Servicios, load_Clinica_Activa
from django.contrib.auth.decorators import login_required

app_name = 'Veterinaria'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Veterinaria.urls')),
    path('registrarPaciente/', login_required(RegistrarPaciente.as_view()), name='registrar_paciente'),
    path('modificarPaciente/<int:pk>', login_required(ModificarPaciente.as_view()), name='modificar_paciente'),
    path('detallePaciente/<int:pk>', login_required(DetallePaciente), name='detalle_paciente'),
    path('eliminarPaciente/<int:pk>',login_required(eliminarPaciente),name='eliminar_paciente'),
    path('listadoPacientes/', login_required(ListadoPacientes.as_view()), name='listado_pacientes'),
    path('detallePropietario/<str:pk>', login_required(DetallePropietario.as_view()), name='detalle_propietario'),
    path('buscarPaciente/', login_required(BuscarPaciente), name='buscar_paciente'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT,}),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ajax/load_Municipio/', load_Municipios, name='load_Municipio'),
    path('registrarEmpleado/', login_required(CrearEmpleado.as_view()), name='crear_empleado'),
    path('listadoEmpleados/', login_required(ListarEmpleados.as_view()), name='listado_empleados'),
    path('detalleEmpleado/<str:pk>', login_required(DetalleEmpleado.as_view()), name='detalle_empleado'),
    path('solicitudIngreso/', CrearSolicitud.as_view(), name='crear_solicitud'),
    path('solicitudEnviada/', SolicitudEnviada, name='solicitud_enviada'),
    path('listadoSolicitudes/', login_required(ListarSolicitudes.as_view()), name='listado_solicitudes'),
    path('detalleSolicitud/<int:pk>', login_required(DetalleSolicitud.as_view()), name='detalle_solicitud'),
    path('listadoCitas/', login_required(ListadoCitas), name='listado_citas'),
    path('crearCita/', login_required(CrearCita.as_view()), name='crear_cita'),
    path('detalleCita/<int:pk>', login_required(DetalleCita), name='detalle_cita'),
    path('detalleCitaPasada/<int:pk>', login_required(DetalleCitaPasada), name='detalle_cita_pasada'),
    path('modificarCita/<int:pk>', login_required(ModificarCita.as_view()), name='modificar_cita'),
    path('buscarCita/', login_required(BuscarCita), name='buscar_cita'),
    path('cancelarCita/<int:pk>/', login_required(CancelarCita.as_view()), name = 'cancelar_cita'),
    path('listadoHorarios/', login_required(ListadoHorarios), name='listado_horarios'),
    path('horariosInactivos/', login_required(HorariosInactivos), name='horarios_inactivos'),
    path('crearHorario/', login_required(CrearHorario.as_view()), name='crear_horario'),
    path('modificarHorario/<int:pk>', login_required(cambiarEstadoHorario), name='modificar_horario'),
    path('borrarHorario/<int:pk>', login_required(borrarHorario), name='borrar_horario'),
    path('tipoRegistro/', login_required(TipoRegistro), name = 'tipo_registro'),
    path('registrarSoloPaciente/', login_required(RegistrarSoloPaciente.as_view()), name='registrar_solo_paciente'),
    path('registrarConsulta/<int:pk>', login_required(RegistrarConsulta), name='registrar_consulta'),
    path('detalleConsulta/<int:pk>', login_required(DetalleConsulta.as_view()), name='detalle_consulta'),
    path('expediente/<int:pk>', login_required(DetalleExpediente), name='expediente'),
    path('pacientesInactivos/', login_required(PacientesInactivos), name='pacientes_inactivos'),
    path('ajax/load_Propietario/', load_Propietario, name='load_Propietario'),
    path('ajax/load_Paciente/', load_Paciente, name='load_Paciente'),
    path('ajax/load_Clinica/', load_Clinica, name='load_Clinica'),
    path('ajax/load_Clinica_Activa/', load_Clinica_Activa, name='load_Clinica_Activa'),
    path('ajax/load_Horario/', load_Horarios, name='load_Horario'),
    path('ajax/load_Consultorio/', load_Consultorio, name='load_consultorio'),
    path('ajax/load_Consultorio_Edit/', load_Consultorio_Edit, name='load_consultorio_edit'),
    path('ajax/load_Servicios/', load_Servicios, name='load_servicio'),
    path('listadoServicios/',login_required(ListarServicio.as_view()), name='listado_servicios'),
    path('detalleServicio/<int:pk>',login_required(DetalleServicio.as_view()),name='detalle_servicios'),
    path('crearServicio/',login_required(CrearServicio.as_view()),name='crear_servicio'),
    path('modificarServicio/<int:pk>',login_required(ModificarServicio.as_view()), name='modificar_servicio'),
    path('borrarServicio/<int:pk>',login_required(BorrarServicio.as_view()),name='borrar_servicio'),
    path('solicitudServicioIngreso/',login_required(CrearSolicitudServicio.as_view()),name ='crear_solicitud_servicio'),
    path('solicitudServicioEnviado/',SolicitudServicioEnviado, name='solicitud_servicio_enviado'),
    path('listadoSolicitudServicio/',login_required(ListarSolicitudServicio.as_view()),name='listado_solicitud_servicio'),
    path('detalleSolicitudServicio/<int:pk>',login_required(DetalleSolicitudServicio.as_view()),name='detalle_solicitud_servicio'),    
    path('serviciosInactivos/', login_required(ServiciosInactivos),name='servicios_inactivos'),
    path('servicioParaBorrar/',login_required(ServiciosParaBorrar),name='servicio_para_borrar'),
    path('agregarVacuna/<int:pk>', login_required(AgregarVacuna), name='agregar_vacuna'),
    path('estadoEmpleado/<str:duiEmp>', login_required(cambiarEstadoEmpleado), name='cambiar_estado'),
    path('consolidados/<int:pk>', login_required(Consolidados), name='consolidados'),
    path('consolidadosAsoc/', login_required(ConsolidadosAsoc), name='consolidadosAsoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)