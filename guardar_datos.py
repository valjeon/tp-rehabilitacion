import json
import os
import time
import paciente

def guardar_resultado(nombre_actividad, datos):

    base_path = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base_path, "datos")
    os.makedirs(carpeta, exist_ok=True)

    paciente_id = paciente.datos_paciente["id"]
    archivo = os.path.join(carpeta, f"paciente_{paciente_id}.json")

    # cargar archivo si existe
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            data = json.load(f)
    else:
        data = {
            "paciente": paciente.datos_paciente,
            "resultados": []
        }

    # agregar resultado
    resultado = {
        "actividad": nombre_actividad,
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        **datos
    }

    data["resultados"].append(resultado)

    # guardar
    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)