import requests

url = 'http://10.0.54.88:8060/enviar-correo/'  # Reemplaza con la URL de tu vista de envío de correo
datos = {
    'asunto': 'Asunto del correo',
    'mensaje': 'Cuerpo del correo',
    'destinatario': 'kevinariassistemas@gmail.com'
}

response = requests.post(url, data=datos)

if response.status_code == 200:
    resultado = response.json()
    print(resultado)
else:
    print('Error al enviar el correo:', response.status_code)