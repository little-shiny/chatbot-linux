# Imagen base con Python 3.11
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para Tkinter y la pantalla virtual
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY app.py .
COPY base_datos.json .

# Variable de entorno para la pantalla (X11)
ENV DISPLAY=:0

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]