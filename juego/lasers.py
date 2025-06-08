from typing import Any
import pygame


# esta clase servira tanto para las naves como para los enemigos
class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad, alto_ventana):
        super().__init__()
        #crea un pequeño rectangulo que simula ser el laser
        self.image = pygame.Surface((4,15))
        # Si velocidad es positiva, es láser de alien (va hacia abajo)
        # Si velocidad es negativa, es láser de nave (va hacia arriba)
        if velocidad < 0:
            self.image.fill((255, 0, 0))  # Amarillo para aliens
        else:
            self.image.fill((128, 0, 128))  # Morado para la nave
            
        self.rect = self.image.get_rect(center = posicion)  # rectangulo para el laser
        self.velocidad = velocidad
        self.alto_ventana = alto_ventana

    def update(self):
        self.rect.y -= self.velocidad
        
        if self.rect.y > self.alto_ventana + 15 or self.rect.y < 0:
            self.kill()