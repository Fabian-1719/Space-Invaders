import pygame

#Clase Blocke: representa un pequeño bloque que compone los obstáculos
class blocke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Inicializa como Sprite
        self.image = pygame.Surface((3, 3))  # Crea una superficie de 3x3 píxeles
        self.image.fill((128, 0, 128))       # Le da color morado al bloque
        self.rect = self.image.get_rect(topleft=(x, y))  # Posición en pantalla

#  Matriz (13x23) que define la forma del obstáculo. 
# Cada 1 representa un bloque visible, y cada 0 un espacio vacío.
cuadro = [
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
]

#  Clase Obstaculo: se encarga de agrupar muchos bloques individuales
class Obstaculo:
    def __init__(self, x, y):
        # Grupo que contiene todos los bloques del obstáculo
        self.blocke_grupo = pygame.sprite.Group()

        #  Recorre toda la matriz cuadro (fila por fila, columna por columna)
        for fila in range(len(cuadro)):
            for columna in range(len(cuadro[0])):
                # Si hay un 1, significa que debe colocarse un bloque en esa posición
                if cuadro[fila][columna] == 1:
                    #  Calcula la posición real del bloque en la pantalla
                    # Cada bloque mide 3x3 píxeles, así que se multiplica por 3
                    pos_x = x + columna * 3
                    pos_y = y + fila * 3

                    # Crea el bloque y lo añade al grupo
                    block = blocke(pos_x, pos_y)
                    self.blocke_grupo.add(block)
