# aliens.py - Versión mejorada con soporte para niveles

import pygame
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"graficos/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direccion):
        """Actualiza la posición del alien con velocidad variable"""
        self.rect.x += direccion


class Nave_misteriosa(pygame.sprite.Sprite):
    def __init__(self, ancho_pantalla, offset):
        super().__init__()
        self.image = pygame.image.load('graficos/mystery.png')
        self.ancho_pantalla = ancho_pantalla
        self.offset = offset

        # Posición inicial aleatoria
        x = random.choice([self.offset / 2, self.ancho_pantalla + self.offset - self.image.get_width()])

        # Velocidad base (será modificada por la clase Game según el nivel)
        if x == self.offset / 2:
            self.velocidad = 3
        else:
            self.velocidad = -3

        self.rect = self.image.get_rect(topleft=(x, 90))

    def update(self):
        """Actualiza la posición de la nave misteriosa"""
        self.rect.x += self.velocidad
        
        # Eliminar cuando sale de la pantalla
        if self.rect.right > self.ancho_pantalla + self.offset / 2:
            self.kill()
        elif self.rect.left < self.offset / 2:
            self.kill()

    def set_velocidad(self, nueva_velocidad):
        """Permite cambiar la velocidad desde fuera de la clase"""
        if self.velocidad > 0:
            self.velocidad = nueva_velocidad
        else:
            self.velocidad = -nueva_velocidad


# Clase adicional para aliens especiales en niveles superiores
class AlienEspecial(Alien):
    """Alien especial que aparece en niveles superiores con comportamiento diferente"""
    def __init__(self, type, x, y, patron_movimiento="normal"):
        super().__init__(type, x, y)
        self.patron_movimiento = patron_movimiento
        self.contador_movimiento = 0
        self.velocidad_vertical = 0

    def update(self, direccion):
        """Movimiento especial para aliens de niveles superiores"""
        if self.patron_movimiento == "zigzag":
            # Movimiento en zigzag
            self.rect.x += direccion
            self.contador_movimiento += 1
            if self.contador_movimiento % 30 == 0:  # Cada 30 frames
                self.velocidad_vertical = -self.velocidad_vertical if self.velocidad_vertical != 0 else 2
            self.rect.y += self.velocidad_vertical
            
        elif self.patron_movimiento == "rapido":
            # Movimiento más rápido
            self.rect.x += direccion * 1.5
            
        else:
            # Movimiento normal
            self.rect.x += direccion