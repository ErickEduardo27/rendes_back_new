from django.contrib import admin
from django.urls import path, include 
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers, permissions
from appAsistencial.views import views as viewsAsis


router = routers.DefaultRouter() 
router.register(r'usuarios', viewsAsis.usuarioViewSet)
router.register(r'perfiles', viewsAsis.perfilViewSet)
router.register(r'pacientes', viewsAsis.pacienteViewSet, basename = 'pacientes_register')
router.register(r'ipress', viewsAsis.ipressViewSet)
router.register(r'periodos', viewsAsis.periodosViewSet)
router.register(r'periodoIpress', viewsAsis.periodoIpressViewSet)
router.register(r'indexIpress', viewsAsis.indexIpressViewSet, basename = 'index_ipress')
router.register(r'usuarioIpress', viewsAsis.usuarioIpressViewSet)
router.register(r'usuarioIpressFilter', viewsAsis.usuarioIpressFilterViewSet, basename = 'usuario_ipress')
router.register(r'paciente', viewsAsis.pacienteViewSet)
router.register(r'etiologia', viewsAsis.etiologiaViewSet)
router.register(r'pacientesDialisis', viewsAsis.pacientesDialisisViewSet)
router.register(r'unidadesActuales', viewsAsis.unidadesActualesViewSet)
router.register(r'morbilidadesHospitalarias', viewsAsis.morbilidadesHospitalariasViewSet)
router.register(r'eventosAccesosVasculares', viewsAsis.eventosAccesosVascularesViewSet)
router.register(r'vacunaciones', viewsAsis.vacunacionesViewSet)
router.register(r'resultadosClinicos', viewsAsis.resultadosClinicosViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resumen_registros/', viewsAsis.resumen_registros, name='resumen_registros_todos'),
    path('resumen_registros/<str:id_ipress>/', viewsAsis.resumen_registros, name='resumen_registros_ipress'),
    path('resumen_registros/<str:id_ipress>/<str:id_periodo>/', viewsAsis.resumen_registros, name='resumen_registros_completo'),
    path('api/token/', viewsAsis.CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/me/', viewsAsis.UsuarioMeView.as_view(), name='me'),

    path('api/register/', viewsAsis.UserRegistrationView.as_view(), name='user_register'),
    
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)), 
]
    