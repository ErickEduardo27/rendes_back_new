FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Lima

# Configura la zona horaria
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

# Instala las dependencias del sistema operativo
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libc-dev \
    libpq-dev \
    tzdata \
    gnupg \
    gdal-bin \
    libgdal-dev \
    && apt-get clean

# Instala las dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install djangorestframework \
    djangorestframework-simplejwt \
    drf-yasg \
    python-dateutil \
    django-cors \
    django-cors-headers \
    pytz \
    python-decouple \
    requests \
    Pillow \
    django-cleanup \
    python-dotenv \
    openpyxl

# Copia tu aplicación al directorio de trabajo
COPY ./ ./

# Define el comando predeterminado para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8050"]