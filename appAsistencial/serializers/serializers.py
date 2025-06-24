from appAsistencial.models.models import perfil,usuario,modalidades,red,ipress,pacientes,usuarioIpress,etiologia,pacientesDialisis,ubigeo,tipoPacientes,periodos,periodoIpress,estados
from rest_framework import serializers

class perfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = perfil
        fields = '__all__' 

class usuarioSerializer(serializers.ModelSerializer):
    datosPerfil = perfilSerializer(source="id_perfil", read_only=True)
    class Meta:
        model = usuario
        exclude = ['id_perfil'] 

class modalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = modalidades
        fields = '__all__'

class ubigeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__'


class redSerializer(serializers.ModelSerializer):
    class Meta:
        model = red
        fields = '__all__'
        
class ipressSerializer(serializers.ModelSerializer):
    datosModalidad = modalidadesSerializer(source="id_modalidad", read_only=True)
    datosUbigeo = ubigeoSerializer(source="id_ubigeo", read_only=True)
    datosRed = redSerializer(source="id_red", read_only=True)
    class Meta:
        model = ipress
        fields = '__all__'

class pacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = pacientes
        fields = '__all__'

class tipoPacientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = tipoPacientes
        fields = '__all__'

class periodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = periodos
        fields = '__all__'

class usuarioIpressSerializer(serializers.ModelSerializer):
    datosUsuario = usuarioSerializer(source="id_usuario", read_only=True)
    datosIpress = ipressSerializer(source="id_ipress", read_only=True)
    class Meta:
        model = usuarioIpress
        fields = '__all__'

class periodoIpressSerializer(serializers.ModelSerializer):
    datosPeriodo = periodoSerializer(source="id_periodo", read_only=True)
    datosIpress = ipressSerializer(source="id_ipress", read_only=True)
    class Meta:
        model = periodoIpress
        fields = '__all__'

class etiologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = etiologia
        fields = '__all__'

class estadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = estados
        fields = '__all__'

class ubigeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__'

class pacientesDialisisSerializer(serializers.ModelSerializer):
    datosEti = etiologiaSerializer(source="id_etiologia", read_only=True)
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    class Meta:
        model = pacientesDialisis
        fields = '__all__'

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomLoginSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('usuario')
        password = attrs.get('password')

        user = usuario.objects.filter(usuario=username, clave=password).first()
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }