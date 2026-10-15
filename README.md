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

## 📋 Requisitos Previos
* Python 3.10 o superior instalado.
* [Ollama](https://ollama.com/) instalado en tu equipo.
* Docker Desktop (opcional, para la ejecución en contenedor).

---

## 🚀 Guía de Reproducción (Paso a Paso)

### 1. Clonar el Repositorio
Clona este repositorio en tu máquina local y accede a la carpeta del proyecto:
```bash
git clone [https://github.com/tu-usuario/nombre-del-repo.git](https://github.com/tu-usuario/nombre-del-repo.git)
cd nombre-del-repo

Asegúrate de tener el servicio de Ollama corriendo y descarga el modelo Ministral utilizado en las pruebas:

Bash
ollama serve
# En otra terminal, descarga el modelo:
ollama run ministral

Instala las dependencias necesarias de Python:

Bash
pip install -r requirements.txt
Ejecuta el script de inferencia para correr la suite de pruebas y generar el archivo de resultados:

Bash
python src/inference.py

Ejecución con Docker
Si prefieres ejecutar el entorno de forma contenerizada:

Construye la imagen de Docker:

Bash
docker build -t ministral-inference .
Ejecuta el contenedor asegurándote de mapear el volumen de resultados:

Bash
docker run --rm -v $(pwd)/results:/app/results ministral-inference
