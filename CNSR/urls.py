
from django.contrib import admin
from django.urls import include, path
from Asistencial import views as viewsAsis
from rest_framework import routers, permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from .views.imports.pre_carga_f1  import pre_carga_f1
router = routers.DefaultRouter() 

router.register(r'usuario', viewsAsis.usuarioViewSet)
router.register(r'perfil', viewsAsis.perfilViewSet)
router.register(r'ipress', viewsAsis.ipressViewSet)
router.register(r'indexIpress', viewsAsis.indexIpressViewSet, basename = 'index_ipress')
router.register(r'usuarioIpress', viewsAsis.usuarioIpressViewSet)
router.register(r'usuarioIpressFilter', viewsAsis.usuarioIpressFilterViewSet, basename = 'usuario_ipress')
router.register(r'paciente', viewsAsis.pacienteViewSet)
router.register(r'etiologia', viewsAsis.etiologiaViewSet)
router.register(r'pacientesDialisis', viewsAsis.pacientesDialisisViewSet)
router.register(r'fecha', viewsAsis.fechaViewSet)
router.register(r'red', viewsAsis.redViewSet)
router.register(r'unidadesActuales', viewsAsis.unidadesActualesViewSet)
router.register(r'unidadesActualesDetalles', viewsAsis.unidadesActualesDetallesViewSet)
router.register(r'eventosAccesosVasculares', viewsAsis.eventosAccesosVascularesViewSet)
router.register(r'morbilidadesHospitalarias', viewsAsis.morbilidadesHospitalariasViewSet)
router.register(r'resultadosClinicos', viewsAsis.resultadosClinicosViewSet)
router.register(r'calidadMicrobiologicas', viewsAsis.calidadMicrobiologicasViewSet)
router.register(r'vacunaciones', viewsAsis.vacunacionesViewSet)
router.register(r'vacunacionesDetalles', viewsAsis.vacunacionesDetallesViewSet)
router.register(r'modalidades', viewsAsis.modalidadesViewSet)
router.register(r'periodos', viewsAsis.periodosViewSet)
router.register(r'estados', viewsAsis.estadosViewSet)
router.register(r'periodoIpress', viewsAsis.periodoIpressViewSet)
router.register(r'tipoPacientes', viewsAsis.tipoPacientesViewSet)
router.register(r'ubigeo', viewsAsis.ubigeoViewSet)

urlpatterns = [
    path('users/', viewsAsis.UsersViewSet, name = 'users'),
    path('login/', viewsAsis.LoginViewSet, name = 'login'),
    path('carga_masiva/', viewsAsis.carga_masiva),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('scritpFecha/', viewsAsis.scritpFecha),
    path('calcular_avance_por_paciente/', viewsAsis.calcular_avance_por_paciente),
    path('consulta_periodo_activo/', viewsAsis.consulta_periodo_activo),
    path('consulta_periodo_inactivo/', viewsAsis.consulta_periodo_inactivo),
    path('consulta_periodo_actualizacion/', viewsAsis.consulta_periodo_actualizacion),
    path('pre_carga/', viewsAsis.pre_carga),
    path('cantidad_registros_abiertos/', viewsAsis.cantidad_registros_abiertos),
    path('cantidad_registros_cerrados/', viewsAsis.cantidad_registros_cerrados),
    path('cerrar_mes/', viewsAsis.cerrar_mes),
    path('reporte_home/', viewsAsis.reporte_home),
    path('reporte_inicio/', viewsAsis.reporte_inicio),
    path('consulta_periodo/', viewsAsis.consulta_periodo),
    path('consulta_periodo_ipress/', viewsAsis.consulta_periodo_ipress),
    path('consulta_periodo_ipress/', viewsAsis.consulta_periodo_ipress),
    path('pre_carga_f1/', pre_carga_f1),
    path('consulta_ipress/', viewsAsis.consulta_ipress),
    path('consulta_precarga/', viewsAsis.consulta_precarga),
    path('registrar_periodo_ipress/', viewsAsis.registrar_periodo_ipress),
    path('cantidad_registros/', viewsAsis.cantidad_registros),
    path('consulta_periodo_estado/', viewsAsis.consulta_periodo_estado),
    path('crear_periodo_ipress/', viewsAsis.crear_periodo_ipress),
    path('reporte_pacientes_dialisis/', viewsAsis.reporte_pacientes_dialisis),
    path('reporte_unidades_actuales/', viewsAsis.reporte_unidades_actuales),
    path('reporte_eventos_accesos_vasculares/', viewsAsis.reporte_eventos_accesos_vasculares),
    path('reporte_morbilidades_hospitalarias/', viewsAsis.reporte_morbilidades_hospitalarias),
    path('reporte_resultados_clinicos/', viewsAsis.reporte_resultados_clinicos),
    path('reporte_calidad_microbiologicas/', viewsAsis.reporte_calidad_microbiologicas),
    path('reporte_vacunaciones/', viewsAsis.reporte_vacunaciones),
    path('consultar-dni/', viewsAsis.consultar_dni, name='consultar_dni'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 