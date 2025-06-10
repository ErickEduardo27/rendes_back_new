from appAsistencial.models.models import perfil,usuario
from rest_framework import serializers

class perfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = perfil
        fields = '__all__' 

class usuarioSerializer(serializers.ModelSerializer):
    datosPerfil = perfilSerializer(source="id_perfil", read_only=True)
    class Meta:
        model = usuario
        fields = '__all__' 