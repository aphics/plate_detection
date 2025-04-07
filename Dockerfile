# Dockerfile - Python 3.11 Slim + matplotlib + gmpy2
FROM python:3.11-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
	build-essential \
	python3-dev \
	libffi-dev \
	libfreetype6-dev \
	libpng-dev \
	libopenblas-dev \
	libgmp-dev \
	libmpfr-dev \
	libmpc-dev \
	libgl1 \
	libglib2.0-0 \
	gfortran \
	git \
	&& rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Clona el repositorio en el contenedor
RUN git clone https://github.com/aphics/plate_detection.git /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto de Django
EXPOSE 8000

# Comando por defecto para ejecutar el servidor
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
