import pygame


class blocke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image =pygame.Surface((3,3))    #crea una superficie para hacer bloques para los obstaculos
        self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect(topleft = (x, y))

#matriz que se usara para la forma del obstaculo
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
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]]

#esta clase sirve para contener multiples blockes
class Obstaculo:
    def __init__(self, x, y):
        self.blocke_grupo = pygame.sprite.Group()  # para almacenar varios
        '''
        el bucle iterara atravez de toda la matriz y creara un nuevo blocke
        #cuando encurntre un 1 si no ,no crera un bloque
        '''
        for fila in range(len(cuadro)):
            for columna in range(len(cuadro[0])):
                if cuadro[fila][columna] == 1:
                    '''
                    Las siguientes variables calculan las cordenadas x, y del blocke segun la 
                    la cantidad de columnas y filas en la matriz , como cada bloque tiene 3 pixeles
                    de ancho y de largo se multiplican el numero de columnass y filas por 3 y sumandole
                    el eje respectivo para determinar las cordenadas x , y y posicionarlo donde se necesite
                    '''
                    pos_x = x + columna * 3    
                    pos_y = y + fila * 3     
                    block = blocke(pos_x, pos_y)
                    self.blocke_grupo.add(block)   # agrega el blocke a su grupo para almacenarlo