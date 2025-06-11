import pygame  #  Importa la biblioteca de pygame para gráficos, sonido y control de entrada
from lasers import Laser  #  Importa la clase Laser desde el archivo lasers.py

#Clase que representa la nave del jugador
class Nave(pygame.sprite.Sprite):  # Hereda de Sprite para poder usar grupos y colisiones
    def __init__(self, ancho_pantalla, alto_pantalla, offset):
        super().__init__()  # Llama al constructor de la clase Sprite

        #  Guarda el tamaño de la pantalla y un desplazamiento opcional (offset)
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.offset = offset

        #  Carga la imagen de la nave desde los archivos y la escala a 60x60 píxeles
        self.image = pygame.image.load('graficos/nave.png')
        self.image = pygame.transform.scale(self.image, (60, 60))

        #  Define el rectángulo que envuelve la imagen, para posicionarla y detectar colisiones
        # La coloca en la parte inferior y centrada horizontalmente
        self.rect = self.image.get_rect(midbottom=((self.ancho_pantalla + self.offset) / 2, self.alto_pantalla))

        #  Velocidad de movimiento lateral
        self.velocidad = 6

        #  Grupo de todos los láseres disparados por esta nave
        self.lasers_group = pygame.sprite.Group()

        #  Controla si se puede disparar
        self.laser_inicial = True  # Si es True, puede disparar
        self.laser_time = 0        # Hora del último disparo
        self.laser_delay = 300     # Tiempo de espera entre disparos (milisegundos)

        #  Carga el sonido del disparo láser
        self.laser_sonido = pygame.mixer.Sound('sonidos/Sounds_laser.ogg')

        #  Tiempo del último disparo real (usado para manejar frecuencia si se desea)
        self.tiempo_ultimo_disparo = 0
        self.frecuencia_disparo = 400  # No se usa directamente aquí, pero puedes usarlo para limitar disparos

    #  Maneja el input del usuario: mover nave y disparar
    def user_input(self):
        keys = pygame.key.get_pressed()  # Obtiene qué teclas están presionadas

        # ▶ Mover a la derecha
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.velocidad
            # Limita el movimiento derecho para que no salga de pantalla
            if self.rect.right > self.ancho_pantalla + (self.offset - 35):
                self.rect.right = self.ancho_pantalla + (self.offset - 35)
        
        # ◀ Mover a la izquierda
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.velocidad
            # Limita el movimiento izquierdo para que no salga de pantalla
            if self.rect.left < 35:
                self.rect.left = 35

        #  Disparar con ESPACIO si está permitido
        if keys[pygame.K_SPACE] and self.laser_inicial:
            self.laser_inicial = False  # Evita que dispare múltiples veces seguidas
            # Crea un nuevo láser desde el centro de la nave
            laser = Laser(self.rect.center, 5, self.alto_pantalla)
            self.lasers_group.add(laser)  # Añade el láser al grupo
            self.laser_time = pygame.time.get_ticks()  # Guarda el tiempo actual para controlar la recarga
            self.laser_sonido.play()  # Reproduce el sonido del disparo

    #  Actualiza la nave en cada fotograma
    def update(self):
        self.user_input()  # Procesa teclas
        self.lasers_group.update()  # Actualiza todos los láseres en el grupo
        self.recargar_laser()  # Controla si ya puede volver a disparar

    #  Controla el tiempo de recarga para poder volver a disparar
    def recargar_laser(self):
        if not self.laser_inicial:  # Si no puede disparar aún
            hora_actual = pygame.time.get_ticks()  # Hora actual en milisegundos
            # Si ya pasó el tiempo de espera (delay), permite disparar de nuevo
            if hora_actual - self.laser_time >= self.laser_delay:
                self.laser_inicial = True

    #  Reinicia la posición de la nave y borra los láseres
    def reinicio(self):
        # Coloca la nave de nuevo en el centro inferior
        self.rect = self.image.get_rect(midbottom=((self.ancho_pantalla + self.offset) / 2, self.alto_pantalla))
        # Borra todos los láseres del grupo (como si no hubiera disparado)
        self.lasers_group.empty()
