from appAsistencial.models import perfil,usuario,modalidades,red,Ipress,pacientes,usuarioIpress,etiologia,pacientesDialisis,ubigeo,tipoPacientes,periodoIpress,estados,Periodos,unidadesActuales,morbilidadesHospitalarias,eventosAccesosVasculares,vacunaciones,resultadosClinicos
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

class UsuarioCreateSerializer(serializers.ModelSerializer):
    # Solo para creación; write_only evita que se devuelva en la respuesta
    password = serializers.CharField(write_only=True, min_length=1, trim_whitespace=False)

    class Meta:
        model = User
        # Incluye los campos que necesitas crear (ajusta según tu modelo)
        fields = [
            'id_usuario', 'id_perfil', 'documento', 'nombre', 'usuario',
            'estado', 'is_active', 'password'
        ]
        read_only_fields = ['id_usuario', 'is_active']  # 'is_active' si no quieres que lo seteen

    def validate_usuario(self, value):
        # Normaliza si quieres (por ejemplo, quitar espacios)
        return value.strip()

    def create(self, validated_data):
        """
        Crea el usuario usando el manager para que set_password() hashee.
        """
        password = validated_data.pop('password')
        # Opción A (recomendada): usa el manager
        user = User.objects.create_user(password=password, **validated_data)

        # Opción B (alternativa): si prefieres, set_password manual
        # user = User(**validated_data)
        # user.set_password(password)
        # user.save()

        return user


class UsuarioDetailSerializer(serializers.ModelSerializer):
    datosPerfil = perfilSerializer(source="id_perfil", read_only=True)
    class Meta:
        model = User
        fields = [
            'id_usuario', 'id_perfil', 'documento', 'nombre', 'usuario','datosPerfil',
            'estado', 'is_active', 'is_staff', 'is_superuser', 'last_login'
        ]
        read_only_fields = fields  # si no quieres permitir updates con este serializer


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """
    Para actualizar datos y (opcionalmente) cambiar password.
    Si viene 'password', se hashea; si no, se ignora.
    """
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id_perfil', 'documento', 'nombre', 'usuario', 'estado', 'is_active', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user
    
class modalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = modalidades
        fields = '__all__'

class ubigeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__'

class PeriodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodos
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
        model = Ipress
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
        model = Periodos
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
    ipress = serializers.CharField(source='ipress.ipress', read_only=True)  # nombre visible
    id_ipress = serializers.PrimaryKeyRelatedField(queryset=Ipress.objects.all(), source="ipress",
    required=False )
    """ periodo = serializers.CharField(source='ipress.nombre', read_only=True)  # nombre visible
    id_periodo = serializers.PrimaryKeyRelatedField(queryset=Ipress.objects.all(), source="ipress",
    required=False ) """
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
    # Este campo permite enviar el ID del paciente en POST
    id_paciente = serializers.PrimaryKeyRelatedField(queryset=pacientes.objects.all())

    # Este campo solo muestra el nombre del paciente en GET
    paciente = serializers.CharField(source='id_paciente.paciente', read_only=True)
    documento = serializers.CharField(source='id_paciente.documento', read_only=True)
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

class unidadesActualesSerializer(serializers.ModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    datosRed = redSerializer(source="id_red", read_only=True)
    class Meta:
        model = unidadesActuales
        fields = '__all__'

class eventosAccesosVascularesSerializer(serializers.ModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    class Meta:
        model = eventosAccesosVasculares
        fields = '__all__'

class morbilidadesHospitalariasSerializer(serializers.ModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    class Meta:
        model = morbilidadesHospitalarias
        fields = '__all__'

class vacunacionesSerializer(serializers.ModelSerializer):
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosRed = redSerializer(source="id_red", read_only=True)
    class Meta:
        model = vacunaciones
        fields = '__all__'

class resultadosClinicosSerializer(serializers.ModelSerializer):
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    class Meta:
        model = resultadosClinicos
        fields = '__all__'



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
