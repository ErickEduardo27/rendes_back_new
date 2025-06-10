from django.contrib import admin
from django.urls import path, include 
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers, permissions
from appAsistencial.views import views as viewsAsis

router = routers.DefaultRouter() 
router.register(r'usuario', viewsAsis.usuarioViewSet)
router.register(r'perfil', viewsAsis.perfilViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)), 
]
