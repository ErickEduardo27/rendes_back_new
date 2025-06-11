from django.db import models
from django.contrib.gis.db import models as gis_models
import openpyxl
from django.http import JsonResponse


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

class usuario(models.Model):
    id_usuario=models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(perfil, on_delete=models.CASCADE, db_column='id_perfil')
    documento =models.CharField(max_length=15)
    nombre =models.CharField(max_length=50)
    usuario =models.CharField(max_length=15)
    clave =models.CharField(max_length=15)
    estado =models.CharField(max_length=15)
    class Meta:
        db_table = 'rd_usuarios'

    def __str__(self):
        return (self.usuario) 


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
        
class ipress(models.Model):
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
    id_ipress = models.ForeignKey(ipress, on_delete=models.CASCADE, db_column='id_ipress')
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

class periodos (models.Model):

    id_periodo= models.AutoField(primary_key=True)
    periodo = models.CharField(max_length=100)

    class Meta:
        db_table = 'rd_periodos'

    def __str__(self):
        return (self.periodo)


class periodoIpress(models.Model):
    id_periodo_ipress = models.AutoField(primary_key=True)
    id_periodo = models.ForeignKey(periodos, on_delete=models.CASCADE, db_column='id_periodo')
    id_ipress = models.ForeignKey(ipress, on_delete=models.CASCADE, db_column='id_ipress')
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
    id_etiologia =models.ForeignKey(etiologia, on_delete=models.PROTECT, db_column='id_etiologia')
    modalidad_inicio_trr =models.CharField(max_length=20)
    fecha_inicio_trr=models.CharField(max_length=100)
    subsistema_salud=models.CharField(max_length=100)
    tipo_acceso=models.CharField(max_length=100)
    fecha_creacion_acceso=models.CharField(max_length=100)
    fecha_primer_ingreso=models.CharField(max_length=100)
    id_usuario_ipress=models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    enf_ateroesclerotica_cardiaca=models.CharField(max_length=20, blank=True, null=True)
    enf_insuficiencia_cardiaca_congestiva=models.CharField(max_length=20, blank=True, null=True)
    enf_vascular_periferica=models.CharField(max_length=20, blank=True, null=True)
    enf_cerebro_vascular=models.CharField(max_length=20, blank=True, null=True)
    enf_cancer=models.CharField(max_length=20, blank=True, null=True)
    enf_diabetes=models.CharField(max_length=20, blank=True, null=True)
    enf_hipertension=models.CharField(max_length=20, blank=True, null=True)
    enf_tuberculosis=models.CharField(max_length=20, blank=True, null=True)
    enf_otra=models.CharField(max_length=20, blank=True, null=True)
    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')

    def __str__(self):
        return f"{self.id_periodo_ipress} - {self.id_paciente}"

    class Meta:
        unique_together = ('id_periodo_ipress', 'id_paciente','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_pacientes_dialisis'
        
class unidadesActuales(models.Model):

    id_unidad_actual = models.AutoField(primary_key=True)
    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    id_red =models.ForeignKey(red, on_delete=models.PROTECT, db_column='id_red')
    fecha_ingreso =models.CharField(max_length=20)
    VHB=models.CharField(max_length=100)
    VHC=models.CharField(max_length=100)
    VHI=models.CharField(max_length=100)
    AcHBs=models.CharField(max_length=100)
    tipo_acceso=models.CharField(max_length=100)
    motivo_cambio_acceso=models.CharField(max_length=100)
    fecha_creacion_acceso=models.CharField(max_length=100)
    id_usuario_ipress=models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    id_tipo_paciente=models.ForeignKey(tipoPacientes, on_delete=models.PROTECT,db_column='id_tipo_paciente')

    def __str__(self):
        return f"{self.id_periodo_ipress} - {self.id_paciente}"

    class Meta:
        unique_together = ( 'id_paciente','id_periodo_ipress','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_unidades_actuales'

class unidadesActualesDetalles(models.Model):

    id_unidad_actual_detalle = models.AutoField(primary_key=True)
    id_unidad_actual = models.ForeignKey(unidadesActuales, on_delete=models.PROTECT, db_column='id_unidad_actual')
    fecha_egreso =models.DateField()
    tipo_egreso=models.CharField(max_length=100)
    fecha_reingreso=models.DateField()
    
    class Meta:
        db_table = 'rf_unidades_actuales_detalles'

    def __str__(self):
        return (self.tipo_egreso)

class eventosAccesosVasculares (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    tipo_acceso_vascular=models.CharField(max_length=100)
    fecha_evento=models.CharField(max_length=100)
    inicio_antmicrobial=models.CharField(max_length=100)
    inicio_vancomicina=models.CharField(max_length=100)
    hemocultivo_positivo=models.CharField(max_length=100)
    estado_acceso_vascular=models.CharField(max_length=100)
    observaciones=models.CharField(max_length=100, blank=True, null=True)
    id_evento_acceso_vascular= models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('id_periodo_ipress', 'id_paciente','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_eventos_accesos_vasculares'

    def __str__(self):
        return (self.observaciones)

class morbilidadesHospitalarias (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    diagnostico=models.CharField(max_length=100)
    codigo_diagnostico=models.CharField(max_length=100)
    fecha_hospitalizacion=models.CharField(max_length=100)
    fecha_alta=models.CharField(max_length=100)
    fuente=models.CharField(max_length=100)
    id_morbilidad_hospitalaria= models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('id_periodo_ipress', 'id_paciente','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_morbilidades_hospitalarias'

    def __str__(self):
        return (self.diagnostico)

class resultadosClinicos (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    Hb=models.CharField(max_length=100)
    calcio=models.CharField(max_length=100)
    fosforo=models.CharField(max_length=100)
    PTHi=models.CharField(max_length=100)
    Alb=models.CharField(max_length=100)
    calcio_corregido=models.CharField(max_length=100)
    ktv=models.CharField(max_length=100)
    tiempo_dialisis=models.CharField(max_length=100)
    eritoproyetina=models.BooleanField()
    hierro=models.BooleanField()
    hiperparatioidismo=models.BooleanField()
    id_resultado_clinico= models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('id_periodo_ipress', 'id_paciente','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_resultados_clinicos'

    def __str__(self):
        return (self.tiempo_dialisis)
    
class calidadMicrobiologicas (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    control=models.BooleanField()
    salida_osmosis_ufc=models.CharField(max_length=100)
    anillo_circulacion_ufc=models.CharField(max_length=100)
    salida_osmosis_ue=models.CharField(max_length=100)
    anillo_circulacion_ue=models.CharField(max_length=100)
    maquina_1_ufc=models.CharField(max_length=100)
    maquina_2_ufc=models.CharField(max_length=100)
    maquina_1_ue=models.CharField(max_length=100)
    maquina_2_ue=models.CharField(max_length=100)
    id_calidad_microbiologica= models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('id_periodo_ipress','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_calidad_microbiologicas'

    def __str__(self):
        return (self.control)

class vacunaciones (models.Model):

    id_periodo_ipress = models.ForeignKey(periodoIpress, on_delete=models.PROTECT, db_column='id_periodo_ipress')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.PROTECT, db_column='id_paciente')
    id_usuario_ipress =models.ForeignKey(usuarioIpress, on_delete=models.PROTECT, db_column='id_usuario_ipress')
    id_red =models.ForeignKey(red, on_delete=models.PROTECT, db_column='id_red')
    turno=models.CharField(max_length=100)
    frecuencia=models.CharField(max_length=100)
    id_vacunacion= models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('id_periodo_ipress','id_paciente','id_usuario_ipress')  # Garantiza unicidad de la combinación de campos
        db_table = 'rf_vacunaciones'

    def __str__(self):
        return (self.turno)

class vacunacionesDetalles (models.Model):

    id_vacunacion_detalle= models.AutoField(primary_key=True)
    id_vacunacion = models.ForeignKey(vacunaciones, on_delete=models.PROTECT, db_column='id_vacunacion')
    tipo_vacuna=models.CharField(max_length=100)
    nro_dosis=models.CharField(max_length=100)
    fecha_dosis=models.CharField(max_length=100)
    motivo_no_vacunacion=models.CharField(max_length=100)

    class Meta:
        db_table = 'rf_vacunacionesDetalles'

    def __str__(self):
        return (self.nro_dosis)



