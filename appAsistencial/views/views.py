from appAsistencial.models import usuario,perfil,Ipress, usuarioIpress,periodoIpress,pacientes,etiologia,pacientesDialisis,estados,Periodos,unidadesActuales,morbilidadesHospitalarias,eventosAccesosVasculares,vacunaciones,resultadosClinicos,red,PacienteRegistro,Asignacion
from appAsistencial.serializers.serializers import perfilSerializer,usuarioSerializer,ipressSerializer,usuarioIpressSerializer,periodoIpressSerializer,pacienteSerializer,etiologiaSerializer,pacientesDialisisSerializer, CustomLoginSerializer, UserRegistrationSerializer,periodoSerializer,unidadesActualesSerializer,morbilidadesHospitalariasSerializer,eventosAccesosVascularesSerializer,vacunacionesSerializer,resultadosClinicosSerializer,redSerializer,UsuarioCreateSerializer,UsuarioDetailSerializer,UsuarioUpdateSerializer,PacienteRegistroSerializer,AsignacionSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import connection
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
""" class usuarioViewSet(viewsets.ModelViewSet):
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario','documento'] """

User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff  # solo staff crea/edita

class usuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id_usuario')
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario','documento']

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UsuarioUpdateSerializer
        return UsuarioDetailSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cambiar_password(self, request, pk=None):
        """
        Endpoint dedicado para cambiar la contraseña de un usuario.
        Body esperado: {"password": "NuevaClaveSegura123"}
        """
        user = self.get_object()
        password = request.data.get('password', '')
        if not password or len(password) < 8:
            return Response({'detail': 'Password requerido (mínimo 8 caracteres).'}, status=400)
        user.set_password(password)
        user.save(update_fields=['password'])
        return Response({'detail': 'Contraseña actualizada correctamente.'}, status=200)

class indexRedViewSet(viewsets.ModelViewSet):
    queryset = red.objects.all()
    serializer_class = redSerializer
class redViewSet(viewsets.ModelViewSet):
    queryset = red.objects.all()
    serializer_class = redSerializer
    pagination_class = None

class perfilViewSet(viewsets.ModelViewSet):
    queryset = perfil.objects.all()
    serializer_class = perfilSerializer 
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

class indexPerfilViewSet(viewsets.ModelViewSet):
    queryset = perfil.objects.all()
    serializer_class = perfilSerializer 
    permission_classes = [permissions.IsAuthenticated]

class ipressViewSet(viewsets.ModelViewSet):
    queryset = Ipress.objects.all().order_by('-id_ipress')
    serializer_class = ipressSerializer  # Asigna la clase serializadora correspondient
    permission_classes = [permissions.IsAuthenticated]    
    search_fields = ['estado']
    pagination_class = None

class indexIpressViewSet(viewsets.ModelViewSet):
    serializer_class = ipressSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['ipress','estado']

    def get_queryset(self):
        queryset = Ipress.objects.all()
        ipressParam = self.request.query_params.get('ipress')
        estado = self.request.query_params.get('estado')
        # Aplicar filtros
        if ipressParam:
            queryset = queryset.filter(ipress__icontains=ipressParam)
        if estado:
            queryset = queryset.filter(estado=estado)
        # Tomar una rebanada del queryset
        return queryset

class usuarioIpressViewSet(viewsets.ModelViewSet):
    queryset = usuarioIpress.objects.all()
    serializer_class = usuarioIpressSerializer 
    search_fields = ['=id_usuario__usuario','^estado']


class periodoIpressViewSet(viewsets.ModelViewSet):
    queryset = periodoIpress.objects.all()
    serializer_class = periodoIpressSerializer  
    permission_classes = [permissions.IsAuthenticated]    
    search_fields = ['=id_']
    pagination_class= None

class pacienteViewSet(viewsets.ModelViewSet):
    queryset = pacientes.objects.all()
    serializer_class = pacienteSerializer
    pagination_class=None
    def get_queryset(self):
        queryset = self.queryset
        estados = self.request.query_params.get('estado')
        documento = self.request.query_params.get('documento')
        paciente = self.request.query_params.get('paciente')

        if estados:
            estados_lista = estados.split(',')
            queryset = queryset.filter(estado__in=estados_lista)
        if documento:
            queryset = queryset.filter(documento__icontains=documento)
        if paciente:
            queryset = queryset.filter(paciente__icontains=paciente)
        return queryset
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            if 'rd_pacientes_documento_key' in str(e):
                return Response(
                    {'error': 'El número de documento ya existe en la base de datos.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Error de integridad en la base de datos.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class indexPacienteViewSet(viewsets.ModelViewSet):
    queryset = pacientes.objects.all()
    serializer_class = pacienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['paciente','documento']

class usuarioIpressFilterViewSet(viewsets.ModelViewSet):
    serializer_class = usuarioIpressSerializer 
    search_fields = ['=id_usuario']

    def get_queryset(self):
        queryset = usuarioIpress.objects.all()
        id_usuario = self.request.query_params.get('id_usuario', None)
        if id_usuario is not None:
            queryset = queryset.filter(id_usuario=id_usuario)
        return queryset

class periodosViewSet(viewsets.ModelViewSet):
    queryset = Periodos.objects.all()
    serializer_class = periodoSerializer 
    pagination_class = None

class etiologiaViewSet(viewsets.ModelViewSet):
    queryset = etiologia.objects.all()
    serializer_class = etiologiaSerializer 
    search_fields = ['=codigo']

class pacientesDialisisViewSet(viewsets.ModelViewSet):
    queryset = pacientesDialisis.objects.all()
    serializer_class = pacientesDialisisSerializer 
    search_fields = ['=id_paciente']
    pagination_class=None
    def get_queryset(self):
        queryset = super().get_queryset()
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        id_paciente = self.request.query_params.get('id_paciente')

        if id_periodo_ipress == 'null':
            queryset = queryset.filter(id_periodo_ipress__isnull=True)
        elif id_periodo_ipress:
            queryset = queryset.filter(id_periodo_ipress=id_periodo_ipress)

        if id_paciente:
            queryset = queryset.filter(id_paciente=id_paciente).order_by('-id_paciente_dialisis')

        return queryset

class CustomLoginView(APIView):
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UsuarioMeView(APIView):
    """ permission_classes = [IsAuthenticated] """
    def get(self, request):
        try:
            user_autenticado = request.user
            
            serializer = usuarioSerializer(user_autenticado)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Error al obtener datos del usuario: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



# --- NUEVA VISTA PARA REGISTRO DE USUARIOS ---
class UserRegistrationView(APIView):
    permission_classes = [AllowAny] # Permite que usuarios no autenticados se registren

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() 
            
            return Response(usuarioSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def resumen_registros(request, id_ipress=None, id_periodo=None):
    # Convertir "null" (string) a None
    if id_ipress == "null" or id_ipress is None:
        id_ipress_int = None
    else:
        try:
            id_ipress_int = int(id_ipress)
        except ValueError:
            return JsonResponse({"error": "ID IPRESS inválido"}, status=400)

    if id_periodo == "null" or id_periodo is None:
        id_periodo_int = None
    else:
        try:
            id_periodo_int = int(id_periodo)
        except ValueError:
            return JsonResponse({"error": "ID PERIODO inválido"}, status=400)

    # Ejecutar función en base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rendes_resumen_registros(%s, %s)", [id_ipress_int, id_periodo_int])
        datos = [fila[0] for fila in cursor.fetchall()]

    return JsonResponse(datos, safe=False)

def reporte_resultados(request, id_ipress=None, id_periodo=None):
    # Convertir "null" (string) a None
    if id_ipress == "null" or id_ipress is None:
        id_ipress_int = None
    else:
        try:
            id_ipress_int = int(id_ipress)
        except ValueError:
            return JsonResponse({"error": "ID IPRESS inválido"}, status=400)

    if id_periodo == "null" or id_periodo is None:
        id_periodo_int = None
    else:
        try:
            id_periodo_int = int(id_periodo)
        except ValueError:
            return JsonResponse({"error": "ID PERIODO inválido"}, status=400)

    # Ejecutar función en base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rendes_reporte_resultados(%s, %s)", [id_ipress_int, id_periodo_int])
        print(cursor.fetchall())
        datos = [fila[0] for fila in cursor.fetchall()]

    return JsonResponse(datos, safe=False)

class vacunacionesViewSet(viewsets.ModelViewSet):
    queryset = vacunaciones.objects.all()
    serializer_class = vacunacionesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda libre con ?search=
    search_fields = ['id_paciente__paciente', 'id_paciente__documento']
    def get_queryset(self):
        qs = super().get_queryset()
        # NUNCA recortes con [:1] si quieres paginación/búsqueda
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        if id_periodo_ipress:
            qs = qs.filter(id_periodo_ipress=id_periodo_ipress)
        return qs

class resultadosClinicosViewSet(viewsets.ModelViewSet):
    queryset = resultadosClinicos.objects.all()
    serializer_class = resultadosClinicosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda libre con ?search=
    search_fields = ['id_paciente__paciente', 'id_paciente__documento']
    def get_queryset(self):
        qs = super().get_queryset()
        # NUNCA recortes con [:1] si quieres paginación/búsqueda
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        if id_periodo_ipress:
            qs = qs.filter(id_periodo_ipress=id_periodo_ipress)
        return qs



class unidadesActualesViewSet(viewsets.ModelViewSet):
    queryset = unidadesActuales.objects.all()
    serializer_class = unidadesActualesSerializer 
    pagination_class = None  #
    def get_queryset(self):
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')

        if id_periodo_ipress:
            return unidadesActuales.objects.filter(
                id_periodo_ipress=id_periodo_ipress
            ).order_by('-fecha_creacion_acceso_actual')[:1]

        # Retorna todos si no hay filtro
        return unidadesActuales.objects.all()

""" class unidadesActualesPagViewSet(viewsets.ModelViewSet):
    queryset = unidadesActuales.objects.all()
    serializer_class = unidadesActualesSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['datosPaciente__paciente', 'datosPaciente__documento']
    def get_queryset(self):
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')

        if id_periodo_ipress:
            return unidadesActuales.objects.filter(
                id_periodo_ipress=id_periodo_ipress
            ).order_by('-fecha_creacion_acceso_actual')[:1]

        # Retorna todos si no hay filtro
        return unidadesActuales.objects.all() """

class unidadesActualesPagViewSet(viewsets.ModelViewSet):
    queryset = unidadesActuales.objects.all()
    serializer_class = unidadesActualesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda libre con ?search=
    search_fields = ['id_paciente__paciente', 'id_paciente__documento']

    # Ordenamiento opcional
    ordering_fields = ['fecha_creacion_acceso_actual']
    ordering = ['-fecha_creacion_acceso_actual']

    def get_queryset(self):
        qs = super().get_queryset()
        # NUNCA recortes con [:1] si quieres paginación/búsqueda
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        if id_periodo_ipress:
            qs = qs.filter(id_periodo_ipress=id_periodo_ipress)
        return qs

class morbilidadesHospitalariasViewSet(viewsets.ModelViewSet):

    queryset = morbilidadesHospitalarias.objects.all()
    serializer_class = morbilidadesHospitalariasSerializer 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda libre con ?search=
    search_fields = ['id_paciente__paciente', 'id_paciente__documento']
    def get_queryset(self):
        qs = super().get_queryset()
        # NUNCA recortes con [:1] si quieres paginación/búsqueda
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        if id_periodo_ipress:
            qs = qs.filter(id_periodo_ipress=id_periodo_ipress)
        return qs

class eventosAccesosVascularesViewSet(viewsets.ModelViewSet):
    queryset = eventosAccesosVasculares.objects.all()
    serializer_class = eventosAccesosVascularesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda libre con ?search=
    search_fields = ['id_paciente__paciente', 'id_paciente__documento']
    def get_queryset(self):
        qs = super().get_queryset()
        # NUNCA recortes con [:1] si quieres paginación/búsqueda
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        if id_periodo_ipress:
            qs = qs.filter(id_periodo_ipress=id_periodo_ipress)
        return qs
    
class PacienteRegistroViewSet(viewsets.ModelViewSet):
    queryset = PacienteRegistro.objects.all()
    serializer_class = PacienteRegistroSerializer 
    pagination_class = None

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    pagination_class = None
