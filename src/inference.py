import json
import os
import time
import urllib.request

# Configuracion de Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"
MODEL_NAME = os.getenv("MODEL_NAME", "ministral")

def consultar_ollama(prompt):
    """Envia un prompt a Ollama y devuelve la respuesta del modelo."""
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        inicio = time.time()
        with urllib.request.urlopen(req) as response:
            respuesta_json = json.loads(response.read().decode("utf-8"))
            fin = time.time()
            
            return {
                "respuesta": respuesta_json.get("response", "").strip(),
                "tiempo_segundos": round(fin - inicio, 2)
            }
    except Exception as e:
        return {
            "respuesta": f"Error de conexion con Ollama ({OLLAMA_URL}): {str(e)}",
            "tiempo_segundos": 0
        }

def main():
    ruta_suite = os.path.join("prompts", "suite.json")
    
    if not os.path.exists(ruta_suite):
        print(f"Error: No se encontro el archivo en {ruta_suite}")
        return

    print(f"Cargando la suite de prompts desde {ruta_suite}...")
    with open(ruta_suite, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    resultados = []
    print(f"\nIniciando evaluacion con el modelo local '{MODEL_NAME}'...\n" + "="*50)
    
    for item in prompts:
        print(f"\n[ID: {item['id']}] Categoria: {item['categoria'].upper()}")
        print(f"Prompt: {item['prompt']}")
        
        resultado_modelo = consultar_ollama(item['prompt'])
        
        print(f"Respuesta:\n{resultado_modelo['respuesta']}")
        print(f"Tiempo de respuesta: {resultado_modelo['tiempo_segundos']} s")
        print("-" * 50)
        
        resultados.append({
            "id": item['id'],
            "categoria": item['categoria'],
            "prompt": item['prompt'],
            "respuesta": resultado_modelo['respuesta'],
            "tiempo_segundos": resultado_modelo['tiempo_segundos']
        })

    # Asegurar que exista la carpeta results
    os.makedirs("results", exist_ok=True)
    ruta_salida = os.path.join("results", "corridas.json")
    
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
        
    print(f"\nEvaluacion finalizada! Resultados guardados exitosamente en '{ruta_salida}'.")

if __name__ == "__main__":
    main()