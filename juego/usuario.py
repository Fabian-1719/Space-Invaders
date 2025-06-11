import json  #  Módulo para trabajar con archivos en formato JSON
import os  #  Módulo para manejar rutas y archivos del sistema
from datetime import datetime  #  Módulo para obtener fecha y hora actual

#Nombre del archivo donde se guardan todos los usuarios
ARCHIVO_USUARIOS = "usuarios.json"

# Cargar todos los usuarios desde el archivo JSON
def cargar_usuarios():
    # Si el archivo no existe, se crea con un diccionario vacío {}
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "w") as f:
            json.dump({}, f)  # Crea un archivo con un objeto JSON vacío

    # Abre el archivo y carga el contenido como un diccionario de Python
    with open(ARCHIVO_USUARIOS, "r") as f:
        return json.load(f)  # Devuelve los datos como un diccionario Python

#  Guarda todos los usuarios (y sus datos) en el archivo JSON
def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w") as f:
        # Convierte el diccionario `usuarios` a texto JSON y lo escribe en el archivo
        json.dump(usuarios, f, indent=4)  # `indent=4` es para que quede bien formateado (más fácil de leer)

#  Obtiene un usuario ya registrado, o lo crea si no existe
def obtener_o_crear_usuario(nombre_usuario, nickname):
    usuarios = cargar_usuarios()  # Carga los usuarios existentes

    # Si el usuario no existe aún en el archivo...
    if nombre_usuario not in usuarios:
        # Crea una nueva entrada con su nickname y un historial vacío
        usuarios[nombre_usuario] = {
            "nickname": nickname,  #  Nombre corto de 3 letras
            "historial": []  #  Lista vacía para guardar partidas futuras
        }
        guardar_usuarios(usuarios)  # Guarda el nuevo usuario en el archivo

    # Devuelve los datos del usuario (ya sea nuevo o existente)
    return usuarios[nombre_usuario]

#  Guarda una nueva partida en el historial del usuario
def guardar_partida(nombre_usuario, puntaje, modo):
    usuarios = cargar_usuarios()  # Carga los datos de todos los usuarios

    if nombre_usuario in usuarios:
        # Crea un nuevo registro de partida con fecha, modo y puntaje
        nueva_partida = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 🗓 Fecha y hora actual formateada
            "modo": modo,  # Puede ser "niveles" o "infinito"
            "puntaje": puntaje  # Puntaje obtenido en esa partida
        }

        # Inserta la nueva partida al principio del historial
        usuarios[nombre_usuario]["historial"].insert(0, nueva_partida)

        # Guarda todos los cambios nuevamente en el archivo JSON
        guardar_usuarios(usuarios)

#  Devuelve el Top 5 de mayores puntajes en modo "infinito"
def obtener_top5_infinito():
    usuarios = cargar_usuarios()  # Carga todos los usuarios

    top_scores = []  # Lista vacía para almacenar puntajes altos

    # Recorre cada usuario y sus partidas
    for usuario, datos in usuarios.items():
        nickname = datos["nickname"]  # Se usa el nickname en el ranking

        for partida in datos["historial"]:
            # Solo se consideran las partidas jugadas en modo "infinito"
            if partida["modo"] == "infinito":
                # Agrega una tupla (nickname, puntaje) a la lista de top_scores
                top_scores.append((nickname, partida["puntaje"]))

    # Ordena la lista de puntajes de mayor a menor
    top_scores.sort(key=lambda x: x[1], reverse=True)

    # Devuelve solo los 5 mejores puntajes
    return top_scores[:5]

