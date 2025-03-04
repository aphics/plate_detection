FROM python:3.11.4-alpine3.18

# Instala dependencias necesarias
RUN apk add --no-cache git

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Clona el repositorio en el contenedor
RUN git clone https://github.com/aphics/plate_detection.git /app

# Instala las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Django
EXPOSE 8000

# Comando por defecto para ejecutar el servidor
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
