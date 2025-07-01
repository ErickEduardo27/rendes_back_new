from appAsistencial.models import usuario,perfil,ipress, usuarioIpress,periodoIpress,pacientes,etiologia,pacientesDialisis,estados
from appAsistencial.serializers.serializers import perfilSerializer,usuarioSerializer,ipressSerializer,usuarioIpressSerializer,periodoIpressSerializer,pacienteSerializer,etiologiaSerializer,pacientesDialisisSerializer, CustomLoginSerializer, UserRegistrationSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class usuarioViewSet(viewsets.ModelViewSet):
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer
    search_fields = ['=usuario']

class perfilViewSet(viewsets.ModelViewSet):
    queryset = perfil.objects.all()
    serializer_class = perfilSerializer 
    permission_classes = [permissions.IsAuthenticated]

class ipressViewSet(viewsets.ModelViewSet):
    queryset = ipress.objects.all().order_by('-id_ipress')
    serializer_class = ipressSerializer  # Asigna la clase serializadora correspondient
    permission_classes = [permissions.IsAuthenticated]    
    search_fields = ['estado']

class indexIpressViewSet(viewsets.ModelViewSet):
    serializer_class = ipressSerializer
    permission_classes = [permissions.IsAuthenticated]    
    search_fields = ['ipress','estado']

    def get_queryset(self):
        queryset = ipress.objects.all()
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
    def get_queryset(self):
        queryset = ipress.objects.all()
        id_ipress = self.request.query_params.get('id_ipress')
        id_periodo = self.request.query_params.get('id_periodo')
        estado = self.request.query_params.get('id_ipress')
        # Aplicar filtros
        if id_ipress:
            queryset = queryset.filter(ipress__icontains=id_ipress)
        if id_periodo:
            queryset = queryset.filter(ipress__icontains=id_periodo)
        if estado:
            queryset = queryset.filter(ipress__icontains=estado)
        # Tomar una rebanada del queryset
        queryset = queryset[:100]

        return queryset

class pacienteViewSet(viewsets.ModelViewSet):
    queryset = pacientes.objects.all()
    serializer_class = pacienteSerializer
    
    permission_classes = [permissions.IsAuthenticated]    
    search_fields = ['=id_paciente']

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

class usuarioIpressFilterViewSet(viewsets.ModelViewSet):
    serializer_class = usuarioIpressSerializer 
    search_fields = ['=id_usuario']

    def get_queryset(self):
        queryset = usuarioIpress.objects.all()
        id_usuario = self.request.query_params.get('id_usuario', None)
        if id_usuario is not None:
            queryset = queryset.filter(id_usuario=id_usuario)
        return queryset

class etiologiaViewSet(viewsets.ModelViewSet):
    queryset = etiologia.objects.all()
    serializer_class = etiologiaSerializer 
    search_fields = ['=codigo']

class pacientesDialisisViewSet(viewsets.ModelViewSet):
    queryset = pacientesDialisis.objects.all()
    serializer_class = pacientesDialisisSerializer 
    search_fields = ['=id_paciente']
    def get_queryset(self):
        queryset = super().get_queryset()
        id_usuario_ipress = self.request.query_params.get('id_usuario_ipress')
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        id_paciente = self.request.query_params.get('id_paciente')

        if id_usuario_ipress:
            queryset = queryset.filter(id_usuario_ipress=id_usuario_ipress)
        if id_periodo_ipress:
            queryset = queryset.filter(id_periodo_ipress=id_periodo_ipress)
        if id_paciente:
            queryset = queryset.filter(id_paciente=id_paciente)
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