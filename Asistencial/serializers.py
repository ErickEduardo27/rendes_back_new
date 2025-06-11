from django.contrib.auth.models import User, Group
from Asistencial.models import perfil,usuario,ipress,pacientes,usuarioIpress,etiologia,pacientesDialisis,fecha,unidadesActuales,unidadesActualesDetalles,red,eventosAccesosVasculares,morbilidadesHospitalarias,resultadosClinicos,calidadMicrobiologicas,vacunaciones,vacunacionesDetalles,modalidades,periodos,estados,periodoIpress,tipoPacientes,ubigeo
from rest_framework import serializers

from datetime import datetime
from dateutil.relativedelta import relativedelta

class perfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = perfil
        fields = '__all__' 

class usuarioSerializer(serializers.HyperlinkedModelSerializer):
    datosPerfil = perfilSerializer(source="id_perfil", read_only=True)
    class Meta:
        model = usuario
        fields = '__all__' 
        
class modalidadesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = modalidades
        fields = '__all__'

class ubigeoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__'


class redSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = red
        fields = '__all__'
        
class ipressSerializer(serializers.HyperlinkedModelSerializer):
    datosModalidad = modalidadesSerializer(source="id_modalidad", read_only=True)
    datosUbigeo = ubigeoSerializer(source="id_ubigeo", read_only=True)
    datosRed = redSerializer(source="id_red", read_only=True)
    class Meta:
        model = ipress
        fields = '__all__'

class pacienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pacientes
        fields = '__all__'

class tipoPacientesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tipoPacientes
        fields = '__all__'

class periodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = periodos
        fields = '__all__'

class usuarioIpressSerializer(serializers.HyperlinkedModelSerializer):
    datosUsuario = usuarioSerializer(source="id_usuario", read_only=True)
    datosIpress = ipressSerializer(source="id_ipress", read_only=True)
    class Meta:
        model = usuarioIpress
        fields = '__all__'

class periodoIpressSerializer(serializers.HyperlinkedModelSerializer):
    datosPeriodo = periodoSerializer(source="id_periodo", read_only=True)
    datosIpress = ipressSerializer(source="id_ipress", read_only=True)
    class Meta:
        model = periodoIpress
        fields = '__all__'

class etiologiaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = etiologia
        fields = '__all__'

class estadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = estados
        fields = '__all__'

class ubigeoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__'

class pacientesDialisisSerializer(serializers.HyperlinkedModelSerializer):
    datosEti = etiologiaSerializer(source="id_etiologia", read_only=True)
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    class Meta:
        model = pacientesDialisis
        fields = '__all__'

class fechaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = fecha
        fields = '__all__'

class redSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = red
        fields = '__all__'

class unidadesActualesSerializer(serializers.HyperlinkedModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosFecha = fechaSerializer(source="id_fecha", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    datosRed = redSerializer(source="id_red", read_only=True)
    class Meta:
        model = unidadesActuales
        fields = '__all__'

class unidadesActualesDetallesSerializer(serializers.HyperlinkedModelSerializer):
    datosUnidadesActuales = unidadesActualesSerializer(source="id_unidad_actual", read_only=True)
    class Meta:
        model = unidadesActualesDetalles
        fields = '__all__'

class eventosAccesosVascularesSerializer(serializers.HyperlinkedModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosFecha = fechaSerializer(source="id_fecha", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    class Meta:
        model = eventosAccesosVasculares
        fields = '__all__'

class morbilidadesHospitalariasSerializer(serializers.HyperlinkedModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosFecha = fechaSerializer(source="id_fecha", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    class Meta:
        model = morbilidadesHospitalarias
        fields = '__all__'

class resultadosClinicosSerializer(serializers.HyperlinkedModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosFecha = fechaSerializer(source="id_fecha", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    class Meta:
        model = resultadosClinicos
        fields = '__all__'

class calidadMicrobiologicasSerializer(serializers.HyperlinkedModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosFecha = fechaSerializer(source="id_fecha", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    class Meta:
        model = calidadMicrobiologicas
        fields = '__all__'

class vacunacionesSerializer(serializers.HyperlinkedModelSerializer):
    datosEstado = estadoSerializer(source="id_estado", read_only=True)
    datosFecha = fechaSerializer(source="id_fecha", read_only=True)
    datosPaciente = pacienteSerializer(source="id_paciente", read_only=True)
    datosUsuarioIpress = usuarioIpressSerializer(source="id_usuario_ipress", read_only=True)
    datosRed = redSerializer(source="id_red", read_only=True)
    class Meta:
        model = vacunaciones
        fields = '__all__'

class vacunacionesDetallesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = vacunacionesDetalles
        fields = '__all__'

class periodosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = periodos
        fields = '__all__'

class estadosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = estados
        fields = '__all__'