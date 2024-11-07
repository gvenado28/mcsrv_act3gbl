# Usar una imagen base de Python
FROM python:latest

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto en el que Flask se ejecutará
EXPOSE 5000

# Definir el comando para ejecutar la aplicación
CMD ["python", "mcsrv_flask.py"]
