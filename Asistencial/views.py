from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from Asistencial.models import perfil,usuario,ipress,pacientes,usuarioIpress,etiologia,pacientesDialisis,fecha,unidadesActuales,unidadesActualesDetalles,red,eventosAccesosVasculares,morbilidadesHospitalarias,resultadosClinicos,calidadMicrobiologicas,vacunaciones,vacunacionesDetalles,modalidades,periodos,estados,periodoIpress,tipoPacientes,ubigeo
from rest_framework import permissions, viewsets, filters ,status
from rest_framework.pagination import PageNumberPagination
#servicios externos
from django.http import HttpResponse,JsonResponse
import requests
import json
from decouple import config
# Create your views here.
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import IsAuthenticated
from Asistencial.serializers import perfilSerializer,ipressSerializer,pacienteSerializer,usuarioSerializer,usuarioIpressSerializer,etiologiaSerializer,pacientesDialisisSerializer,fechaSerializer,unidadesActualesSerializer,unidadesActualesDetallesSerializer,redSerializer,eventosAccesosVascularesSerializer,morbilidadesHospitalariasSerializer,resultadosClinicosSerializer,calidadMicrobiologicasSerializer,vacunacionesSerializer,vacunacionesDetallesSerializer,modalidadesSerializer,periodosSerializer,estadosSerializer,periodoIpressSerializer,tipoPacientesSerializer,ubigeoSerializer
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date
from django.db import connection
from decimal import Decimal
import json
import csv
from django.views.generic import ListView
import openpyxl
from django.http import JsonResponse
import datetime

##########SERVICIO DE ACCESO ESSI - BACKLOCK
@api_view(['POST'])
@permission_required([IsAuthenticated])
def LoginViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.post(config('URLL001'),auth = (result.get('Username'), result.get('Password')))
    login = response.json()
    #print(type(result))
    #print(result.get("codOpcion"))

    return JsonResponse(login)
##########

@api_view(['POST'])
@permission_required([IsAuthenticated])
def UsersViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.post(config('URL'),auth = (config('USER'), config('PASSWORD')) ,  json = {
                        "codOpcion": result.get("codOpcion"),
                        "codTipDoc": result.get("codTipDoc"),
                        "numDoc": result.get("numDoc"),
                        "fecNacimiento":result.get("fecNacimiento")
                      })
    users = response.json()
    #print(type(result))
    #print(result.get("codOpcion"))

    return JsonResponse(users)
##########

@api_view(['POST'])
@permission_required([IsAuthenticated])
def scritpFecha(request):
    # Importar las clases necesarias
    cursor = connection.cursor()
    # Definir la consulta SQL
    sql = 'select * from rendes_registrar_fecha()'

    # Ejecutar la consulta SQL
    cursor.execute(sql)
    # Obtener todos los resultados
    resultados = cursor.fetchall()
    
    # Convertir los resultados a formato JSON
    datos = []
    # Debes poblar `datos` con los datos de `resultados` aqui
    # Devolver la respuesta JSON
    return JsonResponse(datos, safe=False)

def resumen_registros(request, id_periodo_ipress):
    cursor = connection.cursor()

    # Llamar a la función SQL con el parámetro
    sql = "SELECT * FROM rendes_resumen_registros(%s)"
    cursor.execute(sql, [id_periodo_ipress])

    # Cada fila es una tupla (resultado_json,), así que extraemos solo el JSON
    filas = cursor.fetchall()
    datos = [fila[0] for fila in filas]  # fila[0] contiene el JSON ya construido en PostgreSQL

    return JsonResponse(datos, safe=False)

def carga_masiva(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            workbook = openpyxl.load_workbook(file, read_only=True, data_only=True)
            sheet = workbook.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                documento, tipo_documento, autogenerado, nombre_paciente, fecha_nacimiento, genero, grado_instruccion,id_modalidad,id_tipo_paciente = row
                
                paciente_existente = pacientes.objects.filter(documento=documento).first()
                
                if paciente_existente:
                    paciente_existente.tipo_documento = tipo_documento
                    paciente_existente.autogenerado = autogenerado
                    paciente_existente.paciente = nombre_paciente
                    paciente_existente.fecha_nacimiento = fecha_nacimiento
                    paciente_existente.genero = genero
                    paciente_existente.grado_instruccion = grado_instruccion
                    paciente_existente.id_modalidad = modalidades.objects.get(id_modalidad=id_modalidad)
                    paciente_existente.id_tipo_paciente = tipoPacientes.objects.get(id_tipo_paciente=id_tipo_paciente)
                    paciente_existente.save()
                else:
                    paciente_nuevo = pacientes(
                        documento=documento,
                        tipo_documento=tipo_documento,
                        autogenerado=autogenerado,
                        paciente=nombre_paciente,
                        fecha_nacimiento=fecha_nacimiento,
                        genero=genero,
                        grado_instruccion=grado_instruccion,
                        id_modalidad=modalidades.objects.get(id_modalidad=id_modalidad),
                        id_tipo_paciente=tipoPacientes.objects.get(id_tipo_paciente=id_tipo_paciente)
                    )
                    paciente_nuevo.save()
            return JsonResponse({'message': 'Datos guardados exitosamente.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Debes enviar un archivo.'}, status=400)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def calcular_avance_por_paciente(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            paciente = objeto_python.get("paciente")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_calcular_avance_por_paciente(%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_periodo_ipress,id_usuario_ipress,paciente])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            print(resultados)
            # Convertir los resultados a formato JSON
            columnas = [col[0] for col in cursor.description]

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                fila_dict = {}
                for key, value in zip(columnas, fila):
                    # Convertir Decimal a str para evitar problemas de serialización
                    if isinstance(value, Decimal):
                        fila_dict[key] = str(value)
                    else:
                        fila_dict[key] = value
                datos.append(fila_dict)

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)

            # Convertir de nuevo a diccionario de Python para JsonResponse
            cadena_sin_escape = json.loads(json_data)

            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_periodo_activo(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_modalidad = objeto_python.get("id_modalidad")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_periodo_activo(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_modalidad])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id','periodo'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_periodo_inactivo(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_ipress = objeto_python.get("id_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_periodo_inactivo(%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id','periodo'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_ipress(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_ipress()'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id_ipress','ipress'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)


@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_periodo_actualizacion(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_modalidad = objeto_python.get("id_modalidad")
            estado = objeto_python.get("estado")

            # Importar las clases necesarias
            cursor = connection.cursor()
            print(id_usuario_ipress)
            print(id_modalidad)
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_periodo_actualizacion(%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_modalidad,id_usuario_ipress,estado])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            print(resultados)
            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id_periodo','periodo'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def pre_carga(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_pre_carga(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id','periodo'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)



@api_view(['POST'])
@permission_required([IsAuthenticated])
def cantidad_registros_abiertos(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_modalidad = objeto_python.get("id_modalidad")
            id_periodo = objeto_python.get("id_periodo")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_cantidad_registros_abiertos(%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_modalidad,id_usuario_ipress,id_periodo])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('numero','formulario','cantidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)



@api_view(['POST'])
@permission_required([IsAuthenticated])
def cantidad_registros_cerrados(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_modalidad = objeto_python.get("id_modalidad")
            id_periodo = objeto_python.get("id_periodo")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_cantidad_registros_cerrados(%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_modalidad,id_usuario_ipress,id_periodo])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('numero','formulario','cantidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)


@api_view(['POST'])
@permission_required([IsAuthenticated])
def cerrar_mes(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_modalidad = objeto_python.get("id_modalidad")
            id_periodo = objeto_python.get("id_periodo")
            id_formulario = objeto_python.get("id_formulario")
            estado = objeto_python.get("estado")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_cerrar_mes(%s,%s,%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_modalidad,id_usuario_ipress,id_periodo,id_formulario,estado])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('formulario','cantidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_home(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_modalidad = objeto_python.get("id_modalidad")
            id_periodo = objeto_python.get("id_periodo")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_home(%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_modalidad,id_usuario_ipress,id_periodo])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('formulario','estado','cantidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_inicio(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_inicio(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('documento','paciente','tipo_paciente','modalidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_periodo(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Importar las clases necesarias
            cursor = connection.cursor()
            id_ipress = objeto_python.get("id_ipress")
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_periodo(%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id_periodo','periodo','estado'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)


@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_periodo_ipress(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            id_ipress = objeto_python.get("id_ipress")
            id_periodo = objeto_python.get("id_periodo")
            id_estado = objeto_python.get("id_estado")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_periodo_ipress(%s,%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_ipress,id_periodo,id_estado])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id_periodo_ipress'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_precarga(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            id_ipress = objeto_python.get("id_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_precarga(%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id_periodo_ipress'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def registrar_periodo_ipress(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_ipress = objeto_python.get("id_ipress")
            id_periodo = objeto_python.get("id_periodo")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_registrar_periodo_ipress(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_periodo,id_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('id_ipress','ipress'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def cantidad_registros(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_cantidad_registros(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('numero','nombre_form','cantidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def consulta_periodo_estado(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_consulta_periodo_estado(%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('numero','nombre_form','cantidad'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def crear_periodo_ipress(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_ipress = objeto_python.get("id_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_crear_periodo_ipress(%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('numero'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_pacientes_dialisis(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_pacientes_dialisis(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','general','especifica','modalidad_inicio_trr','fecha_inicio_trr','subsistema_salud','tipo_acceso','fecha_creacion_acceso','fecha_primer_ingreso','enf_ateroesclerotica_cardiaca','enf_insuficiencia_cardiaca_congestiva','enf_vascular_periferica','enf_cerebro_vascular','enf_cancer','enf_diabetes','enf_hipertension','enf_tuberculosis','enf_otra'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_unidades_actuales(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_unidades_actuales(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','red','fecha_ingreso','VHB','VHC','VHI','AcHBs','tipo_acceso','motivo_cambio_acceso','fecha_creacion_acceso'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_eventos_accesos_vasculares(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_eventos_accesos_vasculares(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','tipo_acceso_vascular','fecha_evento','inicio_antmicrobial','inicio_vancomicina','hemocultivo_positivo','estado_acceso_vascular','observaciones'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_morbilidades_hospitalarias(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_morbilidades_hospitalarias(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','diagnostico','codigo_diagnostico','fecha_hospitalizacion','fecha_alta','fuente','observaciones'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_resultados_clinicos(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_resultados_clinicos(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','Hb','calcio','fosforo','PTHi','PTHi','Alb','calcio_corregido','ktv','tiempo_dialisis','eritoproyetina','hierro','hiperparatioidismo'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_resultados_clinicos(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_resultados_clinicos(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','Hb','calcio','fosforo','PTHi','PTHi','Alb','calcio_corregido','ktv','tiempo_dialisis','eritoproyetina','hierro','hiperparatioidismo'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_calidad_microbiologicas(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_calidad_microbiologicas(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('control','salida_osmosis_ufc','anillo_circulacion_ufc','salida_osmosis_ue','anillo_circulacion_ue','maquina_1_ufc','maquina_2_ufc','maquina_1_ue','maquina_2_ue'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_calidad_microbiologicas(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_calidad_microbiologicas(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('control','salida_osmosis_ufc','anillo_circulacion_ufc','salida_osmosis_ue','anillo_circulacion_ue','maquina_1_ufc','maquina_2_ufc','maquina_1_ue','maquina_2_ue'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)


@api_view(['POST'])
@permission_required([IsAuthenticated])
def reporte_vacunaciones(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)

            # Verificar si los valores son None o no están presentes
            id_usuario_ipress = objeto_python.get("id_usuario_ipress")
            id_periodo_ipress = objeto_python.get("id_periodo_ipress")

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from rendes_reporte_vacunaciones(%s,%s)'

            # Ejecutar la consulta SQL
            cursor.execute(sql, [id_usuario_ipress,id_periodo_ipress])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','red','turno','frecuencia'), fila)))
            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

class usuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['=usuario']

class perfilViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = perfil.objects.all()
    serializer_class = perfilSerializer 
    #Asignar valores
    permission_classes = [permissions.IsAuthenticated]    
    # filter_backends = [filters.SearchFilter]
    search_fields = ['']

class ipressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ipress.objects.all()
    serializer_class = ipressSerializer  # Asigna la clase serializadora correspondient
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['estado']

class indexIpressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = ipressSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
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
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = usuarioIpress.objects.all()
    serializer_class = usuarioIpressSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id_usuario__usuario']


class periodoIpressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = periodoIpress.objects.all()
    serializer_class = periodoIpressSerializer  
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
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
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = pacientes.objects.all()
    serializer_class = pacienteSerializer
    
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
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
    """
    Punto final de la API que permite ver o editar grupos.
    """
    serializer_class = usuarioIpressSerializer 
    search_fields = ['=id_usuario']

    def get_queryset(self):
        queryset = usuarioIpress.objects.all()
        id_usuario = self.request.query_params.get('id_usuario', None)
        if id_usuario is not None:
            queryset = queryset.filter(id_usuario=id_usuario)
        return queryset

class etiologiaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = etiologia.objects.all()
    serializer_class = etiologiaSerializer 
    search_fields = ['=codigo']

class pacientesDialisisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
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

class fechaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = fecha.objects.all()
    serializer_class = fechaSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['=fecha']

class unidadesActualesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = unidadesActuales.objects.all()
    serializer_class = unidadesActualesSerializer 
    search_fields = ['=fecha_ingreso']
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

class unidadesActualesDetallesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = unidadesActualesDetalles.objects.all()
    serializer_class = unidadesActualesDetallesSerializer 
    search_fields = ['=fecha_egreso']

class eventosAccesosVascularesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = eventosAccesosVasculares.objects.all()
    serializer_class = eventosAccesosVascularesSerializer
    search_fields = ['=fecha_evento']
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


class ubigeoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ubigeo.objects.all()
    serializer_class = ubigeoSerializer 
    search_fields = ['=ubigeo']


class redViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = red.objects.all()
    serializer_class = redSerializer 
    search_fields = ['=red']

class morbilidadesHospitalariasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = morbilidadesHospitalarias.objects.all()
    serializer_class = morbilidadesHospitalariasSerializer
    search_fields = ['=fecha_hospitalizacion']
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

class resultadosClinicosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = resultadosClinicos.objects.all()
    serializer_class = resultadosClinicosSerializer
    search_fields = ['=tiempo_dialisis']
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

class calidadMicrobiologicasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = calidadMicrobiologicas.objects.all()
    serializer_class = calidadMicrobiologicasSerializer
    search_fields = ['=control']
    def get_queryset(self):
        queryset = super().get_queryset()
        id_usuario_ipress = self.request.query_params.get('id_usuario_ipress')
        id_periodo_ipress = self.request.query_params.get('id_periodo_ipress')
        id_paciente = self.request.query_params.get('id_paciente')

        if id_usuario_ipress:
            queryset = queryset.filter(id_usuario_ipress=id_usuario_ipress)
        if id_periodo_ipress:
            queryset = queryset.filter(id_periodo_ipress=id_periodo_ipress)
        return queryset

class vacunacionesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = vacunaciones.objects.all()
    serializer_class = vacunacionesSerializer
    search_fields = ['=control']
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

class vacunacionesDetallesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = vacunacionesDetalles.objects.all()
    serializer_class = vacunacionesDetallesSerializer
    search_fields = ['=control']

class modalidadesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = modalidades.objects.all()
    serializer_class = modalidadesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=modalidades','=id']

class tipoPacientesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = tipoPacientes.objects.all()
    serializer_class = tipoPacientesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=tipo_paciente']

class periodosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = periodos.objects.all()
    serializer_class = periodosSerializer
    search_fields = ['=periodo']

class estadosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = estados.objects.all()
    serializer_class = estadosSerializer
    search_fields = ['=estado']