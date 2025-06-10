from appAsistencial.models.models import usuario,perfil
from appAsistencial.serializers.serializers import perfilSerializer,usuarioSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticated


class usuarioViewSet(viewsets.ModelViewSet):
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['=usuario']

class perfilViewSet(viewsets.ModelViewSet):
    queryset = perfil.objects.all()
    serializer_class = perfilSerializer 
    permission_classes = [permissions.IsAuthenticated]