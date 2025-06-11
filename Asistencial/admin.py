""" from django.contrib import admin
from Asistencial.models import incidenciaEnfermeriaDetalle,procedimientoEnfermeria, incidenciaEnfermeriaCabecera,programacionTurno,unidadAtencion,correos,solicitud,movimientoPaciente,pacienteLocalizacion,pacienteGeoTem,ubigeo,asisPacDiarioAdicional,examenLaboratorio,dpDiario,loginAppHisar,serologiaPaciente,baseDatosProduccion,asisPacDiario,asigCuposPac,parameCentroPuesto,parameCentro,docuContratados, parNuticion, maestroMatSap,cas,usuario, paciente, examen, archivo, presAnemia, admiAnemia, exclusionAnemia, movimientoAnemia, bienAmbiente, bienPersonal, bienpat,dependencia,ambiente,personal, bienImag, proveedor, provMaq, maestro, incidenciaDsi, bienHadware, bienSoftware, bienDetalleMonitor, nutricion, personalVpn, personalCertificado, valGlobalSub, delegacionBienesEstra, listaEspera

# Pacientes geolocalizados Temporalmente
class pacienteGeoTemAdmin(admin.ModelAdmin):
    list_display = ('dni','nombre','hospital','direccion','distrito','latitud','longitud','telefono','frecuencia','turno','serologia','cordePac')
    search_fields = ('dni',)

# Tablas Generales
class ubigeoAdmin(admin.ModelAdmin):
    list_display = ('ubigeo_reniec','ubigeo_inei','codDepartamento_inei','departamento','codProvincia_inei','provincia','distrito')
    search_fields = ('ubigeo_reniec',)

# Ubicacion usuario
class casAdmin(admin.ModelAdmin):
    list_display = ('codCas','descripCas','tipoCas','distrito','estado')
    search_fields = ('tipoCas',)

# Seguridad
class usuarioAdmin(admin.ModelAdmin):
    list_display = ('num_doc','nombre','cas','usuario','clave','perfil_id')
    search_fields = ('usuario',)

class perfilAdmin(admin.ModelAdmin):
    list_display = ('perfil','ruta','imagen')
    search_fields = ('perfil',)

# Register your models here.
class maestroAdmin(admin.ModelAdmin):
    list_display = ('codMaestro','descripMaestro','detalleMaestro')
    search_fields = ('codMaestro',)

class pacienteAdmin(admin.ModelAdmin):
    list_display = ('tipo_doc','num_doc','ape_pat','ape_mat','nombres','fecha_nac','sexo','cas','estado','direccion','distrito')
    ordering = ['ape_pat',]
    search_fields = ('ape_pat','num_doc')

class serologiaPacienteAdmin(admin.ModelAdmin):
    list_display = ('paciente','tipoSerologia','serologia')
    autocomplete_fields = ('paciente',)
    search_fields = ('paciente__num_doc',)

class examenAdmin(admin.ModelAdmin):
    list_display = ('paciente','tipo_exam','archivo_exam','estado_lectura','estado','fecha_reg','user_reg','fecha_mod','user_mod','fecha_eli','user_eli')
    search_fields = ('paciente__nombres', 'paciente__ape_pat', 'paciente__ape_mat',)

class archivoAdmin(admin.ModelAdmin):
    list_display = ('paciente','numHisCli','numBalda','estado','user_reg')
    search_fields = ('numHisCli',)

class imagenInline(admin.TabularInline):
    model = bienImag

#Anemia clinicas

class presAnemiaAdmin(admin.ModelAdmin):
    list_display = ('paciente','fechaPres','nomNefro','medPres','dosisPres','medHiePres','dosisHiePres','viaAdmPres','viaAdmHiePres','usuario')
    search_fields = ('nomNefro',)

class admiAnemiaAdmin(admin.ModelAdmin):
    list_display = ('presAnemia','fechaAdmi','nomEnfer','medAdmi','dosisAdmi','medHieAdmi','dosisHieAdmi','viaAdm','viaAdmHierro','usuario')
    search_fields = ('nomEnfer',)

class exclusionAnemiaAdmin(admin.ModelAdmin):
    list_display = ('paciente','fechaExclu','razonExclu','ObservaExclu','usuario')
    search_fields = ('razonExclu',)

class movimientoAnemiaAdmin(admin.ModelAdmin):
    list_display = ('paciente','fechaMotivo','razonMotivo','obserMotivo')
    search_fields = ('razonMotivo',)

class nutricionAdmin(admin.ModelAdmin):
    list_display = ('paciente','turno','frecuencia','tipoPaciente','fechaIngreso','fechaEvaluacion','peso','talla','imc','circuBra','porcentajeCMB','medCali','porcentajeEPT','albSerica','ValGlobalSub','ingestaCalorica','ingestaProteica','ingestaCaloricaT','ingestaProteicaT','diagNutricional','interveNutricional','obsNutricion','usuario','fechaReg','pacNuevo')
    search_fields = ('frecuencia',)

#Datos de Hospitales VGS

class valGlobalSubAdmin(admin.ModelAdmin):
    list_display = ('paciente','fechaEval','ganPerPeso','camPesoCorp','duraDieta','resultDieta','tipoDieta','sintoGastro','disfuncion','cambioCapFun','grasaSubcu','atrofiaMusc','EdemaTobi','edemaSacro','ascitis','resultadoVGS','fechaReg','userReg')
    search_fields = ('resultadoVGS',)

#Datos de inventario

class bienpatAdmin(admin.ModelAdmin):
    list_display = ('codEti','propBien','desBien','serBien','modBien','marBien','situBien','valBien','estBien')
    search_fields = ('codEti',)
    inlines = [imagenInline]
    list_filter = ('propBien','desBien','serBien','modBien','marBien','situBien')
+
class dependenciaAdmin(admin.ModelAdmin):
    list_display = ('codDep','descDep')
    search_fields = ('codDep',)

class ambienteAdmin(admin.ModelAdmin):
    list_display = ('codAmb','descAmb','dependencia')
    search_fields = ('codAmb',)

class personalAdmin(admin.ModelAdmin):
    list_display = ('dniPer','apePatPer','apeMatPer','nomPer','sexo','fecNacPer','codPlaPer','regPer','cargoPer','nivelPer','telefoPer','correoPer','direcPer','estPer','dependencia')
    search_fields = ('dniPer',)
    ordering = ['apePatPer',]

class bienPersonalAdmin(admin.ModelAdmin):
    list_display = ('personal','bienpat')
    autocomplete_fields = ('personal','bienpat')
    search_fields = ('bienpat__codEti','personal__dniPer','personal__apePatPer')

class bienAmbienteAdmin(admin.ModelAdmin):
    list_display = ('ambiente','bienpat','personal')
    autocomplete_fields = ('ambiente','bienpat')

class bienHadwareAdmin(admin.ModelAdmin):
    list_display = ('bienpat','procesador','numeroIp','numeroIpMv','numeroMac','memoriaRam','capAlmacenamiento','uso','condicion')
    autocomplete_fields = ('bienpat',)

class bienSoftwareAdmin(admin.ModelAdmin):
    list_display = ('bienpat','sistemaOperativo','ofimatica','antivirus')
    autocomplete_fields = ('bienpat',)

class bienDetalleMonitorAdmin(admin.ModelAdmin):
    list_display = ('bienpat','pulgadas')
    autocomplete_fields = ('bienpat',)

class proveedorAdmin(admin.ModelAdmin):
    list_display = ('rucProveedor','nombreProveedor','telefProveedor','direcProveedor','estadoProveedor')
    search_fields = ('rucProveedor',)

class provMaqAdmin(admin.ModelAdmin):
    list_display = ('usobien','bienpat')
    search_fields = ('usobien',)

class incidenciaDsiAdmin(admin.ModelAdmin):
    list_display = ('personal','problema','clasiSolu','solucion','userReg','fecha_reg','numTicket','estado')
    search_fields = ('estado__codMaestro',)
    list_filter = ('estado','clasiSolu')

class personalVpnAdmin(admin.ModelAdmin):
    list_display = ('personal','ip','usuario','clave','personalAutoriza','fechaHabilita','fechaInstalacion','observacion','fecha_reg')
    autocomplete_fields = ('personal',)
    search_fields = ('usuario',)

class personalCertificadoAdmin(admin.ModelAdmin):
    list_display = ('personal','fechaSolicita','tipoCertificado','fechaInstalacion','perosnalInstala','observacion','fecha_reg')
    autocomplete_fields = ('personal',)
    search_fields = ('tipoCertificado',)

class delegacionBienesEstraAdmin(admin.ModelAdmin):
    list_display = ('solPed','codigoSap','producto','unidadMedida','cantidad','fechaDelegacion','pediodoDelegacion','fechaDerivacion','fechaRequerimiento','periodoSolicitado','fechaLogistica','numOrdenCompra','monto','fechaIngresoAlmacen','fechaPago','anulacionPedido','fecha_reg','userOpc','userUsuario','userLogistica','userFinanzas','estado','posiFinaciera','tipoBienEstra','valorTotal','fechaEmiOrden','observaLogistica','tipoDoc','numDoc','cantiRequeridaUsu','obsUsu')
    search_fields = ('solPed',)

class maestroMatSapAdmin(admin.ModelAdmin):
    list_display = ('codSap','tipoBienes','desProducto')
    search_fields = ('codSap',)

class parNuticionAdmin(admin.ModelAdmin):
    list_display = ('edad','pt','cb','cmb','sexo')
    search_fields = ('sexo',)

class listaEsperaAdmin(admin.ModelAdmin):
    list_display = ('paciente','fechaSoli','telefono','telefonoDos','casOrigen','casDestino','distrito','turno','referencia','observaciones','estado','fecha_reg','user_reg','fecha_mod')
    search_fields = ('paciente__num_doc',)

class docuContratadosAdmin(admin.ModelAdmin):
    list_display = ('cas','formato','archivo','estado','fecha_reg','usuario_reg','fecha_edit')
    search_fields = ('formato',)

class parameCentroAdmin(admin.ModelAdmin):
    list_display = ('cas','turno','frecuencia','capacidad','estado','fecha_reg','usuario_reg')
    search_fields = ('turno',)

class parameCentroPuestoAdmin(admin.ModelAdmin):
    list_display = ('cas','turno','frecuencia','tipoPuesto','numeroPuesto','estado','fecha_reg','usuario_reg')
    search_fields = ('turno',)

class asigCuposPacAdmin(admin.ModelAdmin):
    list_display = ('parameCentroPuesto','paciente','fechaAsigCupo','fecha_reg','usuario_reg','fechaTerminoCupo','usuario_reg_termino','estado')
    autocomplete_fields = ('paciente',)
    search_fields = ('usuario_reg',)
    

class asisPacDiarioAdmin(admin.ModelAdmin):
    list_display = ('asigCuposPac','estadoAsistencia','observaFalta','usuario_reg','fecha_reg','validacionAsistencia','casAsd','vigSeguro','estadoAcredi')
    search_fields = ('validacionAsistencia',)

class asisPacDiarioAdicionalAdmin(admin.ModelAdmin):
    list_display = ('paciente','cas','sala','turno','frecuencia','estadoAsistencia','usuario_reg','fecha_reg','validacionAsistencia','motivo','casAsd','vigSeguro')
    search_fields = ('validacionAsistencia',)

#HISAR CUADRO DE MANDO INTEGRAL

class baseDatosProduccionAdmin(admin.ModelAdmin):
    list_display = ('periodo','serie','servicio','actividad','subactividad','cantidad','meta')
    search_fields = ('serie',)

#BACK PARA APLICATIVOS MOVILs

class loginAppHisarAdmin(admin.ModelAdmin):
    list_display = ('paciente','contra','estado','tipoTrataPac')
    autocomplete_fields = ('paciente',)
    search_fields = ('contra',)

class dpDiarioAdmin(admin.ModelAdmin):
    list_display = ('paciente','ultrafil','presArtSis','ultrafil','presArtDias','peso','userReg','fechaReg','imagenOriSalida')
    autocomplete_fields = ('paciente',)
    search_fields = ('ultrafil',)

class examenLaboratorioAdmin(admin.ModelAdmin):
    list_display = ('centro','periodo','area','servicio','actividad','subactividad','acto_medico','fecha_atencion','fecha_solicitud','fecha_cita','fecha_resultado','num_solicitud','dni_solicita','prof_solicita','tipexamen','arealab','sede','examen','descexamen','dni_profesional','profesional','dni_paciente','h_c','paciente','telefonos','annos','meses','dias','sexo','tipo_paciente','cas_adscripcion','diagnostico','des_diagn','tip_diagn','resultado','categoria_resul','fecha_registro','usuario_registro','informe_resultado','orden_plantilla','desc_plantilla','valor_resultado','unidadvalor','observresultado','usario_modifica','fecha_modifica','centro_origen_solicitud','codresul_covid','resultado_covid','hora_registro','autogenerado','desc_topico')
    search_fields = ('area',)

class pacienteLocalizacionAdmin(admin.ModelAdmin):
    list_display = ('cas','paciente','ubigeo','direccion','referencia','telefono','telefonoAlterno','latitud','longitud','cordePac','userReg','fechaReg')
    search_fields = ('direccion',)

class movimientoPacienteAdmin(admin.ModelAdmin):
    list_display = ('cas','paciente','numSolicitud','fechaSolicitud','tipoSolicitud','estado','userReg','fechaReg')
    search_fields = ('numSolicitud',)

class solicitudAdmin(admin.ModelAdmin):
    list_display = ('cas','paciente','respuesta','fechaSolicitud','fechaRespuesta','nuevoTurno','fechaReg','userReg','fechaEdit','userEdit','motivo')
    search_fields = ('respuesta',)

class correosAdmin(admin.ModelAdmin):
    list_display = ('cas','usuario','correo')
    search_fields = ('correo',)

class unidadAtencionAdmin(admin.ModelAdmin):
    list_display = ('codUnidadAtencion','UnidadAtencion')
    search_fields = ('codUnidadAtencion',)

admin.site.register(unidadAtencion, unidadAtencionAdmin)

class programacionTurnoAdmin(admin.ModelAdmin):
    list_display = ('codProgramacionTurno','programacionTurno','dias','horario','horarioFin')
    search_fields = ('codProgramacionTurno',)

admin.site.register(programacionTurno, programacionTurnoAdmin)

class incidenciaEnfermeriaCabeceraAdmin(admin.ModelAdmin):
    list_display = ('fechaReg','horaReg','usuarioReg','fechaEdit','usuarioEdit','sala','descripcionIncidencia')
    search_fields = ('usuarioReg',)

admin.site.register(incidenciaEnfermeriaCabecera, incidenciaEnfermeriaCabeceraAdmin)

class procedimientoEnfermeriaAdmin(admin.ModelAdmin):
    list_display = ('codProcedimientoEnfermeria','procedimientoEnfermeria','tipoProcedimientoEnfermeria')
    search_fields = ('codProcedimientoEnfermeria',)

admin.site.register(procedimientoEnfermeria, procedimientoEnfermeriaAdmin)

class incidenciaEnfermeriaDetalleAdmin(admin.ModelAdmin):
    list_display = ('paciente','personal','unidadAtencion','programacionTurno','procedimientoEnfermeria','incidenciaEnfermeriaCabecera')
    search_fields = ('paciente',)

admin.site.register(incidenciaEnfermeriaDetalle, incidenciaEnfermeriaDetalleAdmin)

admin.site.register(ubigeo, ubigeoAdmin)
admin.site.register(cas, casAdmin)

admin.site.register(usuario, usuarioAdmin)

admin.site.register(maestro, maestroAdmin)

admin.site.register(paciente, pacienteAdmin)
admin.site.register(serologiaPaciente, serologiaPacienteAdmin)
admin.site.register(examen, examenAdmin)
admin.site.register(archivo, archivoAdmin)

admin.site.register(presAnemia, presAnemiaAdmin)
admin.site.register(admiAnemia, admiAnemiaAdmin)
admin.site.register(exclusionAnemia, exclusionAnemiaAdmin)
admin.site.register(movimientoAnemia, movimientoAnemiaAdmin)
admin.site.register(nutricion, nutricionAdmin)
admin.site.register(valGlobalSub, valGlobalSubAdmin)

admin.site.register(personal, personalAdmin)
admin.site.register(bienpat, bienpatAdmin)
admin.site.register(dependencia, dependenciaAdmin)
admin.site.register(ambiente, ambienteAdmin)
admin.site.register(bienPersonal, bienPersonalAdmin)
admin.site.register(bienAmbiente, bienAmbienteAdmin)
admin.site.register(bienHadware, bienHadwareAdmin)
admin.site.register(bienSoftware, bienSoftwareAdmin)
admin.site.register(bienDetalleMonitor, bienDetalleMonitorAdmin)

admin.site.register(proveedor, proveedorAdmin)
admin.site.register(provMaq, provMaqAdmin)


admin.site.register(incidenciaDsi, incidenciaDsiAdmin)
admin.site.register(personalVpn, personalVpnAdmin)
admin.site.register(personalCertificado, personalCertificadoAdmin)

admin.site.register(delegacionBienesEstra, delegacionBienesEstraAdmin)
admin.site.register(maestroMatSap, maestroMatSapAdmin)

admin.site.register(parNuticion, parNuticionAdmin)

admin.site.register(listaEspera, listaEsperaAdmin)

admin.site.register(docuContratados, docuContratadosAdmin)

admin.site.register(parameCentro, parameCentroAdmin)
admin.site.register(parameCentroPuesto, parameCentroPuestoAdmin)
admin.site.register(asigCuposPac, asigCuposPacAdmin)
admin.site.register(asisPacDiario, asisPacDiarioAdmin)
admin.site.register(asisPacDiarioAdicional, asisPacDiarioAdicionalAdmin)

admin.site.register(baseDatosProduccion, baseDatosProduccionAdmin)

admin.site.register(loginAppHisar, loginAppHisarAdmin)
admin.site.register(dpDiario, dpDiarioAdmin)
admin.site.register(examenLaboratorio, examenLaboratorioAdmin)

admin.site.register(pacienteLocalizacion, pacienteLocalizacionAdmin)

admin.site.register(movimientoPaciente, movimientoPacienteAdmin)

admin.site.register(solicitud, solicitudAdmin)

admin.site.register(correos, correosAdmin) """