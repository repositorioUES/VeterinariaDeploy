from django.urls import path
from .views import index
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from Veterinaria.views import *
from .views import *

urlpatterns = [
    path('',index, name="index"),
    path('registro/',registro, name="registro"),
    path('registrar_clinica/',registrar_clinica, name="registrar_clinica"),
    path('listar_clinica/',listar_clinica, name="listar_clinica"),
    path('modificar_clinica/<id>/',modificar_clinica, name="modificar_clinica"),
    path('eliminar_clinica/<id>/',eliminar_clinica, name="eliminar_clinica"),
    path('listar_consultorio/<id>/',listar_consultorio, name="listar_consultorio"),
    path('registrar_consultorio/<id>/',registrar_consultorio, name="registrar_consultorio"),
    path('modificar_consultorio/<id>/',modificar_consultorio, name="modificar_consultorio"),
    path('eliminar_consultorio/<id>/',eliminar_consultorio, name="eliminar_consultorio"),
    # path('reporte_clinica/<id>/',reportePdfView.as_view(), name="reporte_clinica"),
    path('eliminar_empleado/<str:id>/',eliminar_empleado, name="eliminar_empleado"),
    path('eliminar_solicitud_ingreso/<id>/',eliminar_solicitud_ingreso, name="eliminar_solicitud_ingreso"),
    path('eliminar_solicitud_servicio/<id>/',eliminar_solicitud_servicio, name="eliminar_solicitud_servicio"),
    path('reporte_Paciente/<int:pk>',reportePaciente.as_view(), name="reporte_Paciente"),
    path('reporte_Consulta/<int:pk>',reporteConsulta.as_view(), name="reporte_Consulta"),
    path('reporte_Vacuna/<int:pk>',reporteVacuna.as_view(), name="reporte_Vacuna"),
    path('reporte_por_medico/<int:pk>',reportePorMedico.as_view(), name="reporte_por_medico"),
    path('reporte_por_fecha/<int:pk>',reportePorFecha.as_view(), name="reporte_por_fecha"),
    path('reporte_por_clinica',reportePorClinica.as_view(), name="reporte_por_clinica"),
    path('reporte_por_fecha_asoc',reportePorFechaAsoc.as_view(), name="reporte_por_fecha_asoc"),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]