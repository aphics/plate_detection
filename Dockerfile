# Usa una imagen de Python como base
FROM python:3.11.4-alpine3.18

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualizar pip
RUN pip install --upgrade pip

# Copiar archivos al contenedor e instalar dependencias
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que Django correrá
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
