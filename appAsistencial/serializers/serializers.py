from appAsistencial.models import perfil,usuario,modalidades,red,ipress,pacientes,usuarioIpress,etiologia,pacientesDialisis,ubigeo,tipoPacientes,periodos,periodoIpress,estados
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class perfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = perfil
        fields = '__all__' 

class usuarioSerializer(serializers.ModelSerializer):
    datosPerfil = perfilSerializer(source="id_perfil", read_only=True)
    class Meta:
        model = User
        exclude = ['id_perfil', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions']

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
from django.contrib.auth import authenticate

class CustomLoginSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('usuario')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError("Credenciales inválidas. Usuario o contraseña incorrectos.")

        if not user.is_active:
            raise serializers.ValidationError("La cuenta de usuario está inactiva.")

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    

# --- NUEVO SERIALIZER PARA REGISTRO DE USUARIOS ---
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    id_perfil = serializers.PrimaryKeyRelatedField(
        queryset=perfil.objects.all(),
        required=True,
        write_only=True 
    )

    perfil = serializers.CharField(source='id_perfil.perfil', read_only=True)


    class Meta:
        model = User 
        fields = (
            'id_usuario', 
            'usuario',
            'password',
            'documento',
            'nombre',
            'estado',
            'is_active',
            'is_staff',
            'id_perfil',      
            'perfil' 
        )
        extra_kwargs = {
            'estado': {'required': False, 'default': 'Activo'}, 
            'is_active': {'required': False, 'default': True},
            'is_staff': {'required': False, 'default': False},
        }

    # Método para crear el usuario
    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_instance = validated_data.pop('id_perfil') 

        user = User.objects.create_user(
            password=password,
            id_perfil=profile_instance,
            **validated_data
        )
        
        user.save() 
        return user
