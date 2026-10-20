import argparse
import json
import os
import time
import urllib.request

# Configuracion por defecto
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"

def consultar_ollama(model, prompt, temperature, max_tokens):
    """Envía un prompt a Ollama y mide métricas de rendimiento y tokens."""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": float(temperature),
            "num_predict": int(max_tokens)
        }
    }
    
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        inicio = time.time()
        with urllib.request.urlopen(req) as response:
            fin = time.time()
            respuesta_json = json.loads(response.read().decode("utf-8"))
            
            # Métricas que devuelve Ollama en el JSON de respuesta
            texto_respuesta = respuesta_json.get("response", "").strip()
            eval_count = respuesta_json.get("eval_count", 0)  # Tokens generados
            eval_duration = respuesta_json.get("eval_duration", 0) # Nanosegundos que tardó en generar
            prompt_eval_duration = respuesta_json.get("prompt_eval_duration", 0) # TTFT aproximado (en ns)
            
            # Convertir nanosegundos a segundos
            ttft_segundos = round(prompt_eval_duration / 1e9, 4) if prompt_eval_duration else round(fin - inicio, 4)
            
            # Tokens por segundo
            tokens_por_segundo = 0.0
            if eval_duration > 0:
                tokens_por_segundo = round(eval_count / (eval_duration / 1e9), 2)
            elif (fin - inicio) > 0:
                tokens_por_segundo = round(eval_count / (fin - inicio), 2)

            tiempo_total = round(fin - inicio, 2)
            
            return {
                "respuesta": texto_respuesta,
                "tokens_generados": eval_count,
                "tiempo_total_segundos": tiempo_total,
                "ttft_segundos": ttft_segundos,
                "tokens_por_segundo": tokens_por_segundo,
                "error": None
            }
    except Exception as e:
        return {
            "respuesta": "",
            "tokens_generados": 0,
            "tiempo_total_segundos": 0,
            "ttft_segundos": 0,
            "tokens_por_segundo": 0,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="Script de inferencia local con Ollama para Evaluacion de Modelos")
    parser.add_argument("--model", type=str, default="ministral-3:3b", help="Nombre del modelo en Ollama")
    parser.add_argument("--prompts", type=str, default="prompts/suite.json", help="Ruta al archivo JSON de prompts")
    parser.add_argument("--temperature", type=float, default=0.2, help="Temperatura de generacion")
    parser.add_argument("--max_tokens", type=int, default=256, help="Maximo de tokens a generar")
    args = parser.parse_args()

    if not os.path.exists(args.prompts):
        print(f"Error: No se encontro el archivo de prompts en {args.prompts}")
        return

    print(f"Cargando la suite de prompts desde {args.prompts}...")
    with open(args.prompts, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    resultados = []
    print(f"\nIniciando evaluacion con el modelo '{args.model}' (Temp: {args.temperature}, Max Tokens: {args.max_tokens})...\n" + "="*60)
    
    for item in prompts:
        print(f"\n[ID: {item['id']}] Categoria: {item['categoria'].upper()}")
        print(f"Prompt: {item['prompt']}")
        
        res = consultar_ollama(args.model, item['prompt'], args.temperature, args.max_tokens)
        
        if res["error"]:
            print(f"Error de conexion o servidor: {res['error']}")
        else:
            print(f"Respuesta:\n{res['respuesta']}")
            print(f"[Metricas] Tokens: {res['tokens_generados']} | Tiempo Total: {res['tiempo_total_segundos']}s | TTFT: {res['ttft_segundos']}s | Tokens/s: {res['tokens_por_segundo']}")
        print("-" * 60)
        
        resultados.append({
            "id": item['id'],
            "categoria": item['categoria'],
            "prompt": item['prompt'],
            "respuesta": res["respuesta"],
            "tokens_generados": res["tokens_generados"],
            "tiempo_total_segundos": res["tiempo_total_segundos"],
            "ttft_segundos": res["ttft_segundos"],
            "tokens_por_segundo": res["tokens_por_segundo"],
            "error": res["error"] 
        })

    os.makedirs("results", exist_ok=True)
    ruta_salida = os.path.join("results", "corridas.json")
    
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
        
    print(f"\nEvaluacion finalizada con exito! Resultados guardados en '{ruta_salida}'.")

if __name__ == "__main__":

    
    main()