# pantallas_extra.py - Mostrar historial y top 5 con diseño mejorado
import pygame
from usuario import cargar_usuarios, obtener_top5_infinito

BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_OSCURO = (40, 40, 40)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 100)
ROJO = (255, 60, 60)
AZUL_CLARO = (80, 180, 255)
BORDO = (120, 20, 40)

class PantallaHistorial:
    def __init__(self, screen, font, nombre_usuario):
        self.screen = screen
        self.font = font
        self.nombre_usuario = nombre_usuario

    def mostrar(self):
        usuarios = cargar_usuarios()
        historial = usuarios.get(self.nombre_usuario, {}).get("historial", [])

        self.screen.fill(GRIS_OSCURO)
        cuadro = pygame.Rect(70, 80, 610, 500)
        pygame.draw.rect(self.screen, NEGRO, cuadro, border_radius=15)
        pygame.draw.rect(self.screen, AMARILLO, cuadro, 4, border_radius=15)

        titulo = self.font.render("Historial de Partidas", True, AMARILLO)
        self.screen.blit(titulo, (170, 100))

        if not historial:
            texto = self.font.render("Sin partidas registradas.", True, ROJO)
            self.screen.blit(texto, (170, 250))
        else:
            for i, partida in enumerate(historial[:6]):
                texto = self.font.render(f"{partida['fecha']}  {partida['modo'].upper()}  {partida['puntaje']}", True, BLANCO)
                self.screen.blit(texto, (100, 160 + i * 50))

        volver = self.font.render("ESC para volver", True, VERDE)
        self.screen.blit(volver, (240, 610))
        pygame.display.update()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esperando = False

class PantallaTop5:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def mostrar(self):
        top5 = obtener_top5_infinito()

        self.screen.fill(GRIS_OSCURO)
        cuadro = pygame.Rect(100, 100, 550, 460)
        pygame.draw.rect(self.screen, NEGRO, cuadro, border_radius=15)
        pygame.draw.rect(self.screen, AZUL_CLARO, cuadro, 4, border_radius=15)

        titulo = self.font.render("TOP 5 - Modo Infinito", True, AZUL_CLARO)
        self.screen.blit(titulo, (170, 120))

        if not top5:
            texto = self.font.render("Sin datos aún.", True, ROJO)
            self.screen.blit(texto, (220, 250))
        else:
            for i, (nick, puntaje) in enumerate(top5):
                texto = self.font.render(f"{i+1}. {nick} - {puntaje}", True, BLANCO)
                self.screen.blit(texto, (160, 180 + i * 55))

        volver = self.font.render("ESC para volver", True, VERDE)
        self.screen.blit(volver, (230, 600))
        pygame.display.update()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esperando = False

