import pygame
import random  #  Para generar posiciones aleatorias

#Clase Alien: representa a un enemigo alienígena básico
class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()  # Inicializa el Sprite

        self.type = type  # Tipo de alien (para cambiar el gráfico)
        path = f"graficos/alien_{type}.png"  # Ruta al archivo de imagen del alien
        self.image = pygame.image.load(path)  # Carga el gráfico del alien

        # Posiciona al alien en la pantalla (x, y)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direccion):
        """Mueve el alien horizontalmente según la dirección indicada."""
        self.rect.x += direccion  # Cambia su posición horizontal


#  Clase Nave_misteriosa: nave que aparece de vez en cuando con puntos extra
class Nave_misteriosa(pygame.sprite.Sprite):
    def __init__(self, ancho_pantalla, offset):
        super().__init__()  # Inicializa el Sprite

        # Carga la imagen de la nave misteriosa
        self.image = pygame.image.load('graficos/mystery.png')

        self.ancho_pantalla = ancho_pantalla  # Ancho total de la pantalla
        self.offset = offset  # Margen adicional (puede servir para alineación o UI)

        #  Decide si aparece desde la izquierda o desde la derecha aleatoriamente
        x = random.choice([
            self.offset / 2,  # Aparece desde la izquierda
            self.ancho_pantalla + self.offset - self.image.get_width()  # O desde la derecha
        ])

        # Define la dirección de movimiento según el lado desde el que aparece
        self.velocidad = 3 if x == self.offset / 2 else -3

        # Posición inicial en la parte superior (90 píxeles desde arriba)
        self.rect = self.image.get_rect(topleft=(x, 90))

    def update(self):
        """Mueve la nave misteriosa y la elimina si sale de la pantalla"""
        self.rect.x += self.velocidad  # Mueve horizontalmente

        #  Elimina la nave si se sale completamente de la pantalla por izquierda o derecha
        if self.rect.right > self.ancho_pantalla + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()

    def set_velocidad(self, nueva_velocidad):
        """Permite ajustar la velocidad desde afuera, manteniendo la dirección original"""
        # Si iba a la derecha, sigue yendo a la derecha pero más rápido o más lento
        if self.velocidad > 0:
            self.velocidad = nueva_velocidad
        else:
            self.velocidad = -nueva_velocidad


