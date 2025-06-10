import json
import os
from datetime import datetime

ARCHIVO_USUARIOS = "usuarios.json"

def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "w") as f:
            json.dump({}, f)
    with open(ARCHIVO_USUARIOS, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def obtener_o_crear_usuario(nombre_usuario, nickname):
    usuarios = cargar_usuarios()
    if nombre_usuario not in usuarios:
        usuarios[nombre_usuario] = {
            "nickname": nickname,
            "historial": []
        }
        guardar_usuarios(usuarios)
    return usuarios[nombre_usuario]

def guardar_partida(nombre_usuario, puntaje, modo):
    usuarios = cargar_usuarios()
    if nombre_usuario in usuarios:
        usuarios[nombre_usuario]["historial"].insert(0, {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modo": modo,
            "puntaje": puntaje
        })
        guardar_usuarios(usuarios)

def obtener_top5_infinito():
    usuarios = cargar_usuarios()
    top_scores = []
    for usuario, datos in usuarios.items():
        nickname = datos["nickname"]
        for partida in datos["historial"]:
            if partida["modo"] == "infinito":
                top_scores.append((nickname, partida["puntaje"]))
    top_scores.sort(key=lambda x: x[1], reverse=True)
    return top_scores[:5]
