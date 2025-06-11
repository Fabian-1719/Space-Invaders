
import pygame  #  Importa la biblioteca de pygame para gráficos y sprites

#Clase Laser: representa un disparo láser en el juego, tanto para la nave como para los enemigos
class Laser(pygame.sprite.Sprite):  # Hereda de Sprite para poder usar grupos y colisiones fácilmente
    def __init__(self, posicion, velocidad, alto_ventana):
        super().__init__()  # Llama al constructor de Sprite

        #  Crea una superficie pequeña rectangular (4x15 píxeles), que será el láser
        self.image = pygame.Surface((4, 15))

        #  Colorea el láser dependiendo de quién lo dispara:
        # - Si la velocidad es negativa, es un láser de la nave → sube
        # - Si la velocidad es positiva, es un láser de un enemigo → baja
        if velocidad < 0:
            self.image.fill((255, 0, 0))  # Rojo si es disparado por un enemigo (velocidad negativa)
        else:
            self.image.fill((128, 0, 128))  # Morado si es disparado por el jugador

        #  Crea el rectángulo que rodea al láser y lo posiciona en el centro de la nave/enemigo
        self.rect = self.image.get_rect(center=posicion)

        #  Guarda la velocidad vertical del láser (positiva o negativa)
        self.velocidad = velocidad

        #  Guarda la altura total de la ventana del juego, para saber cuándo eliminar el láser
        self.alto_ventana = alto_ventana

    #  Función que se ejecuta en cada fotograma para mover y actualizar el estado del láser
    def update(self):
        #  Mueve el láser verticalmente: si velocidad es positiva baja, si es negativa sube
        self.rect.y -= self.velocidad

        #  Si el láser sale de la pantalla (por arriba o abajo), se elimina automáticamente
        if self.rect.y > self.alto_ventana + 15 or self.rect.y < 0:
            self.kill()  # Elimina el láser del grupo al que pertenece
