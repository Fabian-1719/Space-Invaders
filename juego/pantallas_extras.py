# pantallas_extra.py - Mostrar historial y top 5 con diseño mejorado

import pygame
from usuario import cargar_usuarios, obtener_top5_infinito

#Definición de colores en formato RGB
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_OSCURO = (40, 40, 40)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 100)
ROJO = (255, 60, 60)
AZUL_CLARO = (80, 180, 255)
BORDO = (120, 20, 40)

#Clase para mostrar el historial de partidas de un usuario
class PantallaHistorial:
    def __init__(self, screen, font, nombre_usuario):
        self.screen = screen  # Pantalla del juego donde se dibuja todo
        self.font = font      # Fuente usada para los textos
        self.nombre_usuario = nombre_usuario  # Nombre del usuario actual

    def mostrar(self):
        usuarios = cargar_usuarios()  # Carga todos los usuarios desde el archivo JSON
        historial = usuarios.get(self.nombre_usuario, {}).get("historial", [])  # Obtiene el historial del usuario

        self.screen.fill(GRIS_OSCURO)  # Fondo gris oscuro para la pantalla

        # Dibuja un rectángulo central como "cuadro de historial"
        cuadro = pygame.Rect(70, 80, 610, 500)
        pygame.draw.rect(self.screen, NEGRO, cuadro, border_radius=15)  # Fondo negro con bordes redondeados
        pygame.draw.rect(self.screen, AMARILLO, cuadro, 4, border_radius=15)  # Borde amarillo

        # Muestra el título en pantalla
        titulo = self.font.render("Historial de Partidas", True, AMARILLO)
        self.screen.blit(titulo, (210, 100))

        # Si no hay historial, muestra un mensaje en rojo
        if not historial:
            texto = self.font.render("Sin partidas registradas.", True, ROJO)
            self.screen.blit(texto, (170, 250))
        else:
            # Si hay historial, se muestran las últimas 6 partidas
            for i, partida in enumerate(historial[:6]):
                texto = self.font.render(f"{partida['fecha']}  {partida['modo'].upper()}  {partida['puntaje']}", True, BLANCO)
                self.screen.blit(texto, (100, 160 + i * 50))  # Se posicionan una debajo de la otra

        # Instrucción para volver al menú
        volver = self.font.render("ESC para volver", True, VERDE)
        self.screen.blit(volver, (240, 610))
        pygame.display.update()  # Actualiza la pantalla con todo lo dibujado

        # Espera hasta que el usuario presione ESC para salir de esta pantalla
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cierra el juego si se presiona la X
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Sale de la pantalla con ESC
                        esperando = False


# Clase para mostrar el top 5 global del modo infinito
class PantallaTop5:
    def __init__(self, screen, font):
        self.screen = screen  # Pantalla principal
        self.font = font      # Fuente para el texto

    def mostrar(self):
        top5 = obtener_top5_infinito()  # Obtiene los 5 mejores puntajes del modo infinito

        self.screen.fill(GRIS_OSCURO)  # Fondo de la pantalla

        # Dibuja un rectángulo central como "cuadro del top 5"
        cuadro = pygame.Rect(100, 100, 550, 460)
        pygame.draw.rect(self.screen, NEGRO, cuadro, border_radius=15)  # Fondo negro
        pygame.draw.rect(self.screen, AZUL_CLARO, cuadro, 4, border_radius=15)  # Borde azul claro

        # Título del top 5
        titulo = self.font.render("TOP 5 - Modo Infinito", True, AZUL_CLARO)
        self.screen.blit(titulo, (210, 120))

        # Si no hay datos, se muestra un mensaje
        if not top5:
            texto = self.font.render("Sin datos aún.", True, ROJO)
            self.screen.blit(texto, (220, 250))
        else:
            # Se muestran los mejores 5 puntajes
            for i, (nick, puntaje) in enumerate(top5):
                texto = self.font.render(f"{i+1}. {nick} - {puntaje}", True, BLANCO)
                self.screen.blit(texto, (160, 180 + i * 55))  # Se posicionan en columna

        # Instrucción para volver
        volver = self.font.render("ESC para volver", True, VERDE)
        self.screen.blit(volver, (230, 600))
        pygame.display.update()  # Actualiza la pantalla

        # Espera hasta que el usuario presione ESC
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cierra el juego si se presiona la X
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Sale de esta pantalla
                        esperando = False
