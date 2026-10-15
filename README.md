# Proyecto de Investigacion: Mistral AI / Ministral
Curso: Programacion IV - Sistemas Computacionales Java
Estudiante: Guillermo Arturo Corrales Giammattei

## Descripcion del Proyecto
Este proyecto evalua el rendimiento de modelos de lenguaje locales (Mistral / Ministral) ejecutados a traves de Ollama. Incluye una suite de pruebas funcionales automatizadas, un script de inferencia en Python con medicion de metricas (tiempo de respuesta, tokens por segundo, TTFT) y un entorno contenedorizado con Docker.

## Estructura del Repositorio
├── README.md
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── src/
│   └── inference.py
├── prompts/
│   └── suite.json
├── results/
│   └── corridas.json
└── docs/

## Requisitos Previos
1. Python 3.10 o superior instalado.
2. [Ollama](https://ollama.com/) instalado y ejecutandose localmente con el modelo Ministral descargado (`ollama run ministral`).
3. (Opcional) Docker Desktop para la ejecucion contenedorizada.

## Como Ejecutar la Inferencia Localmente

1. Clonar el repositorio y ubicarse en la carpeta raiz.
2. Instalar las dependencias minimas:
   ```bash
   pip install -r requirements.txt

Ejecutar el script de inferencia indicando el modelo y parametros deseados:
python src/inference.py --model ministral:3b --temperature 0.2 --max_tokens 256

Ejecucion con Docker
Construir la imagen de Docker:
docker build -t evaluador-llm:latest .

Ejecutar el contenedor (asegurandose de tener Ollama corriendo en el host):
docker run --rm --add-host=host.docker.internal:host-gateway -v "${PWD}/results:/app/results" evaluador-llm:latest

