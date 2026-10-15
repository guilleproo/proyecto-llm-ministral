# 1. Imagen base ligera con version fija
FROM python:3.10-slim

# 2. Crear un usuario no root por seguridad (Buena practica exigida)
RUN useradd --create-home appuser

# 3. Establecer directorio de trabajo
WORKDIR /app

# 4. Copiar requerimientos e instalar dependencias (Aprovechamiento de capas/cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el codigo y los prompts manteniendo la estructura
COPY src/ ./src/
COPY prompts/ ./prompts/

# 6. Crear la carpeta results con permisos para el usuario no root
RUN mkdir -p results && chown -R appuser:appuser /app

# 7. Cambiar al usuario no root
USER appuser

# 8. Variables de entorno por defecto
ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV MODEL_NAME=ministral

# 9. Comando por defecto ejecutando el script con argumentos
CMD ["python", "src/inference.py"]