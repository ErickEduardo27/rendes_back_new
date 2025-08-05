from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El campo "usuario" es obligatorio para el Custom User.')
        
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db) 
        return user

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        
        try:
            admin_profile = perfil.objects.get(perfil='ADMIN')
            extra_fields['id_perfil'] = admin_profile
        except perfil.DoesNotExist:
            raise ValueError("El perfil 'ADMIN' no existe en la base de datos. Por favor, créalo primero.")
        
        return self.create_user(usuario, password, **extra_fields)
    

class estados (models.Model):

    id_estado= models.AutoField(primary_key=True)
    estado = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_estados'

    def __str__(self):
        return (self.estado)


class perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    perfil = models.CharField(max_length=1000)
    class Meta:
        db_table = 'rd_perfiles' 

    def __str__(self):
        return (self.perfil)

class usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario=models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(perfil, on_delete=models.CASCADE, db_column='id_perfil',null=True,blank=True)   
    documento =models.CharField(max_length=15, unique=True)
    nombre =models.CharField(max_length=50)
    usuario =models.CharField(max_length=30, unique=True)
    estado =models.CharField(max_length=15)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario' 
    REQUIRED_FIELDS = ['documento', 'nombre'] 

    objects = UsuarioManager()

    class Meta:
        db_table = 'rd_usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    @property
    def id(self):
        return self.id_usuario

    def __str__(self):
        return (self.usuario) 

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser 

    def get_full_name(self):
        return self.nombre

    def get_short_name(self):
        return self.usuario

class modalidades (models.Model):

    id_modalidad= models.AutoField(primary_key=True)
    modalidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_modalidades'

    def __str__(self):
        return (self.modalidad)

class ubigeo (models.Model):

    id_ubigeo= models.AutoField(primary_key=True)
    ubigeo_reniec = models.CharField(max_length=100)
    ubigeo_inei = models.CharField(max_length=100)
    codDepartamento_inei = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codProvincia_inei = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_ubigeos'

    def __str__(self):
        return (self.ubigeo_reniec)

class red(models.Model):
    id_red = models.AutoField(primary_key=True)
    red = models.CharField(max_length=20)

    class Meta:
        db_table = 'rd_redes'

    def __str__(self):
        return (self.red)
        
class Ipress(models.Model):
    id_ipress = models.AutoField(primary_key=True)
    ipress =models.CharField(max_length=15)
    nombre_corto =models.CharField(max_length=50)
    tipo_unidad =models.CharField(max_length=50)
    estado =models.CharField(max_length=15)
    id_modalidad=models.ForeignKey(modalidades, on_delete=models.CASCADE, db_column='id_modalidad')
    id_ubigeo=models.ForeignKey(ubigeo, on_delete=models.CASCADE, db_column='id_ubigeo')
    id_red=models.ForeignKey(red, on_delete=models.CASCADE, db_column='id_red')

    class Meta:
        db_table = 'rd_ipress' 

    def __str__(self):
        return (self.ipress)

class usuarioIpress(models.Model):
    id_usuario_ipress = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_ipress = models.ForeignKey(Ipress, on_delete=models.CASCADE, db_column='id_ipress')
    estado = models.BooleanField()

    def __str__(self):
        return f"{self.id_usuario} - {self.id_ipress}"

    class Meta:
        unique_together = ('id_usuario', 'id_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rd_usuarios_ipress'

class tipoPacientes (models.Model):
    id_tipo_paciente= models.AutoField(primary_key=True)
    tipo_paciente = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_tipo_pacientes'

    def __str__(self):
        return (self.tipo_paciente)

class Periodos (models.Model):
    id_periodo= models.AutoField(primary_key=True)
    periodo = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_periodos'

    def __str__(self):
        return (self.periodo)

class periodoIpress(models.Model):
    id_periodo_ipress = models.AutoField(primary_key=True)
    periodo = models.ForeignKey(Periodos, on_delete=models.CASCADE, db_column='id_periodo')
    ipress = models.ForeignKey(Ipress, on_delete=models.CASCADE, db_column='id_ipress')
    id_estado = models.ForeignKey(estados, on_delete=models.PROTECT, db_column='id_estado')

    # Agrega los campos adicionales que necesites para esta tabla intermedia
    class Meta:
        db_table = 'rd_periodos_ipress'

    def __str__(self):
        return f'{self.id_periodo_ipress}'

class pacientes(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    documento =models.CharField(max_length=100)
    tipo_documento =models.CharField(max_length=100)
    autogenerado =models.CharField(max_length=100)
    paciente =models.CharField(max_length=100)
    fecha_nacimiento =models.CharField(max_length=100)
    genero =models.CharField(max_length=100)
    grado_instruccion =models.CharField(max_length=100)
    id_modalidad=models.ForeignKey(modalidades, on_delete=models.PROTECT, db_column='id_modalidad')
    estado =models.CharField(max_length=100)
    class Meta:
        db_table = 'rd_pacientes' 

    def __str__(self):
        return (self.paciente)

class etiologia(models.Model):
    id_etiologia = models.AutoField(primary_key=True)
    general =models.CharField(max_length=100)
    especifica =models.CharField(max_length=100)
    codigo =models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_etiologias'

    def __str__(self):
        return (self.codigo)

class fecha(models.Model):
    id_fecha = models.AutoField(primary_key=True)
    fecha =models.CharField(max_length=100)
    año =models.CharField(max_length=100)
    mes =models.CharField(max_length=100)
    dia =models.CharField(max_length=100)
    mes_nombre =models.CharField(max_length=100)
    fin_mes =models.CharField(max_length=100)
    periodo =models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_fechas'

    def __str__(self):
        return (self.fecha)

class pacientesDialisis(models.Model):

    id_paciente_dialisis = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    """ id_etiologia =models.ForeignKey(etiologia, on_delete=models.PROTECT, db_column='id_etiologia') """
    modalidad_inicio_trr =models.CharField(max_length=20)
    fecha_inicio_trr=models.CharField(max_length=100)
    subsistema_salud=models.CharField(max_length=100)
    tipo_acceso=models.CharField(max_length=100)
    fecha_creacion_acceso=models.CharField(max_length=100)
    fecha_primer_ingreso=models.CharField(max_length=100)
    """ id_usuario_ipress=models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress') """
    enf_ateroesclerotica_cardiaca=models.CharField(max_length=20, blank=True, null=True)
    enf_insuficiencia_cardiaca_congestiva=models.CharField(max_length=20, blank=True, null=True)
    enf_vascular_periferica=models.CharField(max_length=20, blank=True, null=True)
    enf_cerebro_vascular=models.CharField(max_length=20, blank=True, null=True)
    enf_cancer=models.CharField(max_length=20, blank=True, null=True)
    enf_diabetes=models.CharField(max_length=20, blank=True, null=True)
    enf_hipertension=models.CharField(max_length=20, blank=True, null=True)
    enf_tuberculosis=models.CharField(max_length=20, blank=True, null=True)
    enf_otra=models.CharField(max_length=20, blank=True, null=True)
    id_periodo_ipress = models.CharField(max_length=20, blank=True, null=True)
    fecha_ingreso_hospital=models.CharField(max_length=20, blank=True, null=True)
    localizacion_acceso_inicio=models.CharField(max_length=20, blank=True, null=True)
    hospital_procedencia_trr=models.CharField(max_length=80, blank=True, null=True)
    etiologia=models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.id_paciente}"

    class Meta:
        db_table = 'rf_pacientes_dialisis'

class unidadesActuales(models.Model):

    id_unidad_actual = models.AutoField(primary_key=True)
    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    id_red =models.ForeignKey(red, on_delete=models.PROTECT, db_column='id_red')
    fecha_ingreso =models.CharField(max_length=20, blank=True, null=True)
    VHB=models.CharField(max_length=100, blank=True, null=True)
    VHC=models.CharField(max_length=100, blank=True, null=True)
    VHI=models.CharField(max_length=100, blank=True, null=True)
    AcHBs=models.CharField(max_length=100, blank=True, null=True)
    tipo_acceso_actual=models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion_acceso_actual=models.CharField(max_length=100, blank=True, null=True)
    localizacion_acceso_actual=models.CharField(max_length=100, blank=True, null=True)
    cambio_acceso=models.CharField(max_length=100, blank=True, null=True)
    motivo_cambio=models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion_acceso_nuevo=models.CharField(max_length=100, blank=True, null=True)
    tipo_acceso_nuevo=models.CharField(max_length=100, blank=True, null=True)
    localizacion_acceso_nuevo=models.CharField(max_length=100, blank=True, null=True)
    """ id_usuario_ipress=models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress') """
    """ id_tipo_paciente=models.ForeignKey(tipoPacientes, on_delete=models.PROTECT,db_column='id_tipo_paciente') """

    def __str__(self):
        return f"{self.id_periodo_ipress} - {self.id_paciente}"

    class Meta:
        db_table = 'rf_unidades_actuales'

class eventosAccesosVasculares (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    """ id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress') """
    tipo_acceso_vascular=models.CharField(max_length=100, blank=True, null=True)
    fecha_evento=models.CharField(max_length=100, blank=True, null=True)
    inicio_antmicrobial=models.CharField(max_length=100, blank=True, null=True)
    inicio_vancomicina=models.CharField(max_length=100, blank=True, null=True)
    hemocultivo_positivo=models.CharField(max_length=100, blank=True, null=True)
    estado_acceso_vascular=models.CharField(max_length=100, blank=True, null=True)
    observaciones=models.CharField(max_length=100, blank=True, null=True)
    fe_evento=models.CharField(max_length=100, blank=True, null=True)
    tpInfeccion=models.CharField(max_length=100, blank=True, null=True)
    tratamientoIV=models.BooleanField(default=False)
    vancomicinaIV=models.BooleanField(default=False)
    hemocultivoPositivo=models.BooleanField(default=False)
    tipoGram=models.CharField(max_length=100, blank=True, null=True)
    tipoInfeccionLocal=models.CharField(max_length=100, blank=True, null=True)
    tpGermen=models.CharField(max_length=100, blank=True, null=True)
    bacteria=models.CharField(max_length=100, blank=True, null=True)
    tipoBacteria=models.CharField(max_length=100, blank=True, null=True)
    id_evento_acceso_vascular= models.AutoField(primary_key=True)

    class Meta:
        db_table = 'rf_eventos_accesos_vasculares'

    def __str__(self):
        return (self.observaciones)

        

class morbilidadesHospitalarias (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    """ id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress') """
    diagnostico=models.CharField(max_length=100, blank=True, null=True)
    codigo_diagnostico=models.CharField(max_length=100, blank=True, null=True)
    fecha_hospitalizacion=models.CharField(max_length=100, blank=True, null=True)
    fecha_alta=models.CharField(max_length=100, blank=True, null=True)
    fuente=models.CharField(max_length=100, blank=True, null=True)
    id_morbilidad_hospitalaria= models.AutoField(primary_key=True)
    filtroDescripcion=models.CharField(max_length=100, blank=True, null=True)
    seleccionados=models.CharField(max_length=100, blank=True, null=True)
    fIniHos=models.CharField(max_length=100, blank=True, null=True)
    fAltHos=models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'rf_morbilidades_hospitalarias'

    def __str__(self):
        return (self.diagnostico)


class vacunaciones (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    """ id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress') """
    id_red =models.ForeignKey(red, on_delete=models.PROTECT, db_column='id_red')
    turno=models.CharField(max_length=100)
    frecuencia=models.CharField(max_length=100)
    id_vacunacion= models.AutoField(primary_key=True)


    class Meta:
        db_table = 'rf_vacunaciones'

    def __str__(self):
        return (self.turno)

class resultadosClinicos (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    """ id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress') """
    Hb=models.CharField(max_length=100, blank=True, null=True)
    calcio=models.CharField(max_length=100, blank=True, null=True)
    fosforo=models.CharField(max_length=100, blank=True, null=True)
    PTHi=models.CharField(max_length=100, blank=True, null=True)
    Alb=models.CharField(max_length=100, blank=True, null=True)
    calcio_corregido=models.CharField(max_length=100, blank=True, null=True)
    ktv=models.CharField(max_length=100, blank=True, null=True)
    tiempo_dialisis=models.CharField(max_length=100, blank=True, null=True)
    eritoproyetina=models.BooleanField(default=False)
    hierro=models.CharField(max_length=100, blank=True, null=True)
    hiperparatioidismo=models.BooleanField(default=False)
    id_resultado_clinico= models.AutoField(primary_key=True)

    tmpDialisis=models.CharField(max_length=100, blank=True, null=True)
    eritropoyetina=models.CharField(max_length=100, blank=True, null=True)
    hiperparatiroidismo=models.CharField(max_length=100, blank=True, null=True)
    hb=models.CharField(max_length=100, blank=True, null=True)
    pthi=models.CharField(max_length=100, blank=True, null=True)
    alb=models.CharField(max_length=100, blank=True, null=True)
    calcioCorregido=models.CharField(max_length=100, blank=True, null=True)
    kt=models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'rf_resultados_clinicos'

    def __str__(self):
        return (self.tiempo_dialisis)