import pygame
from lasers import Laser

# la clase que usara para hacer referencia o todo lo que hace la nave

class Nave (pygame.sprite.Sprite):
    def __init__(self, ancho_pantalla, alto_pantalla, offset):
        super().__init__()
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.offset = offset
        #le da el diseño deseado a la nave
        self.image = pygame.image.load('graficos/nave.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        #define el tamaño de la nave en la pantalla de juego y interactuar con el juego
        self.rect = self.image.get_rect(midbottom = ((self.ancho_pantalla + self.offset)/ 2, self.alto_pantalla))
        self.velocidad = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_inicial = True
        self.laser_time = 0
        self.laser_delay = 300
        #musica para los laser
        self.laser_sonido = pygame.mixer.Sound('sonidos/Sounds_laser.ogg')
        self.tiempo_ultimo_disparo = 0
        self.frecuencia_disparo = 400  # milisegundos entre disparos



    def user_input(self):
        keys = pygame.key.get_pressed()

        # Movimiento horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidad
            # Limitar movimiento derecho
            if self.rect.right > self.ancho_pantalla + (self.offset - 35):
                self.rect.right = self.ancho_pantalla + (self.offset - 35)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidad
            # Limitar movimiento izquierdo
            if self.rect.left < 35:
                self.rect.left = 35

        # Disparo
        if keys[pygame.K_SPACE] and self.laser_inicial:
            self.laser_inicial = False
            laser = Laser(self.rect.center, 5, self.alto_pantalla)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sonido.play()

    def update(self):   # se encarga  de actualizar las acciones
        self.user_input()
        self.lasers_group.update()
        self.recargar_laser()

        
    def recargar_laser(self):
        # cuando se necesita recargar
        if not self.laser_inicial:
             # obtiene la hora actual en milesegundos
            hora_actual = pygame.time.get_ticks() 
            # si la hora actual - el ultimo dispaaro es mayor al delay puede volver a disparar
            if hora_actual - self.laser_time >= self.laser_delay:
                self.laser_inicial = True

    #se encarga de poner todo a como estaba al comienzo
    def reinicio(self):
        self.rect = self.image.get_rect(midbottom = ((self.ancho_pantalla + self.offset) / 2, self.alto_pantalla))
        self.lasers_group.empty()

