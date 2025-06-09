import pygame
import random
from spaceship import Nave
from obstaculos import Obstaculo
from obstaculos import cuadro
from aliens import Alien
from lasers import Laser
from aliens import Nave_misteriosa

'''
La clase Game servira como contenedor para  los elementos del juego , como la nave, 
los enemigos, los obstaculos, y el estado del juego . tambien contendra metodos para 
la logica del juego como actualizar las posiciones de los objetos , comprobar colisiones
y actualizar puntuaciones.
La mayor parte esta centralizado en esta clase para  que sea mas facil de entender el 
codigo y ampliar si es necesario
'''

class Game :
    def __init__(self, ancho_pantalla, alto_pantalla, offset):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.offset = offset
        self.nave_grupo = pygame.sprite.GroupSingle()
        self.nave_grupo.add(Nave(self.ancho_pantalla , self.alto_pantalla, self.offset))
        self.obstaculos = self.crear_obstaculos()
        self.aliens_grupo = pygame.sprite.Group()
        self.crear_aliens()
        self.aliens_direccion = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.nave_misteriosa_grupo = pygame.sprite.GroupSingle()
        self.image = pygame.image.load('graficos/vidas.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajustar tamaño
        self.vida_rect = self.image.get_rect()
        self.vida_offset_x = 50  # Espacio entre cada icono de vida
        self.vida_pos_y = 760    # Posición Y fija para los iconos de vida
        self.vidas = 3     # la cantidad de vidas
        self.corre = True  # esto hara saber si el juego sigue corriendo 
        self.puntaje = 0
        self.puntaje_mas_alto = 0
        self.cargar_puntaje_alto()
        
        #trae la musica deseada para el level 1
        pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)
        
        
        #sonido de explosion 
        self.explosion_sonido = pygame.mixer.Sound('sonidos/Sounds_explosion.ogg')

    #funcion que se encargara de crear los obtaculos
    def crear_obstaculos(self):
        #primero encuentra el ancho
        ancho_obstaculo = len(cuadro[0]) *3
        #ahora se restara el ancho de los 4 y se dividira el resultado entre 5 por que tenemos 5 espacios en total
        brecha = ((self.ancho_pantalla + self.offset) - (4 * ancho_obstaculo))/ 5
        
        #lista para guardar los obstaculos
        obstaculos = []

        #secrean los 4 obstaculos con el blucle for
        for i in range(4):
            '''
            calcula la posicion horizontal de cada obstaculo añadiedo espacio iguales 
            entre ambos , asegurando que esten bien alineados
            '''
            desplazamiento_x = (i + 1) * brecha + i * ancho_obstaculo
            # posiciona verticalmente a 100 pixeles de la parte inferior de la pantalla
            obstaculo = Obstaculo(desplazamiento_x, self.alto_pantalla - 110)
            obstaculos.append(obstaculo)
        return obstaculos
    
    '''
    como en el juego hay 5 filas y 11columnas de aliens se usara una matriz
    para manejarlos
    '''
    def crear_aliens(self):
        for fila in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + fila * 55

                if fila == 0:
                    alien_type = 3

                elif fila in (1,2):
                    alien_type = 2
                    
                else:
                    alien_type = 1
                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_grupo.add(alien)

    #la funcion se encarga  de hacer que los aliens se muevan 7
    def mover_aliens(self): 
        '''
        ahora se arreglara el problema de que los aliens se 
        salgan de la pantalla y hay que restringir el movimiento
        de los aliens
        -primero se tiene que obtener todos los sprites alienigenas en
        en la lista 
        -luego se comprueba cada alienigena en la lista para saber si se movio
        fuera de la ventana de juego , se comprueba con un for
        '''
       
        # Actualiza la posición de todos los aliens según la dirección actual
        self.aliens_grupo.update(self.aliens_direccion)
        
        # Obtiene una lista de todos los aliens activos
        alien_sprites = self.aliens_grupo.sprites()

        # Revisa cada alien para ver si toca los bordes
        for alien in alien_sprites:
            # Si algún alien toca el borde derecho (coincide con línea morada en x=775)
            if alien.rect.right >= 775:
                self.aliens_direccion = -1
                self.mover_aliens_abajo(2)
                break
            
            # Si algún alien toca el borde izquierdo (coincide con línea morada en x=25)
            elif alien.rect.left <= 25:
                self.aliens_direccion = 1
                self.mover_aliens_abajo(2)
                break    # los brakes son para que no se acumulen datos

    '''
    tomara la distancia para mover a los alienigenas  hacia abajo 
    '''
    def mover_aliens_abajo(self, distancia):
        if self.aliens_grupo:
            for alien in self.aliens_grupo.sprites():
                alien.rect.y += distancia      

    #se encarga de hacer que los aliens disparen de manera aleatoriO
    def laser_alien(self):
        if self.aliens_grupo.sprites():
            #se selecciona un alienigena aleatorio de todos los aliens visibles
            random_alien = random.choice(self.aliens_grupo.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.alto_pantalla)
            self.alien_lasers_group.add(laser_sprite)


    def crear_nave_misteriosa(self):
        self.nave_misteriosa_grupo.add(Nave_misteriosa(self.ancho_pantalla, self.offset))

    '''
    La siguiente funcion  se encargara de la colsiones con un metodo que ofrece 
    pygame llamado spritecollide , este metodo  verifica si  un sprite especifico
    colisiona con alguno de los sprites de un grupo tambien permite destruir automaticamente 
    el sprite con el que choca 
    '''
    def check_colisiones(self):
        #primero verificar si alaguno de los laseres de la nave coliono con los aliens
        #Nave
        if self.nave_grupo.sprite.lasers_group:
            for laser_sprite in self.nave_grupo.sprite.lasers_group:
                                         #por cada laser, que colisione con los aliens, destruye
                alien_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_grupo, True)
                if alien_hit:
                    self.explosion_sonido.play()
                    for alien in alien_hit:
                        self.revisar_puntacion_alta()
                        self.puntaje += alien.type * 100
                        laser_sprite.kill()   
                        
                #↑ 
                # nota
                #esto devuelve una lista vacia que contiene los sprites de u grupo
                 #que se intersectan con otro sprite asi que se puede usar esa informacion 
                 #tal que :
                    #si retorna una lista que no esta vacia significa que si hubo una colision 
                    #por lo tanto se debe destruir el laser_sprite

                #-nave misteriosa-
                if pygame.sprite.spritecollide(laser_sprite, self.nave_misteriosa_grupo, True):
                    self.puntaje += 500
                    self.revisar_puntacion_alta()
                    self.explosion_sonido.play()
                    laser_sprite.kill()
                    

                #-Los 4 obstaculos-
                for obstaculo in self.obstaculos:
                    if pygame.sprite.spritecollide(laser_sprite, obstaculo.blocke_grupo, True):
                        laser_sprite.kill()
                        


                
        #laser de los aliens
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.nave_grupo, False):  #por que queremos que la nave tenga 3 vidas
                    laser_sprite.kill()
                    self.vidas -= 1
                    if self.vidas == 0:
                        self.game_over()
                               
                #obstaculos golpeados por los aliens
                for obstaculo in self.obstaculos:
                    if pygame.sprite.spritecollide(laser_sprite, obstaculo.blocke_grupo, True):
                        laser_sprite.kill()

        #ahora  las colisiones de los aliens con los obtaculos y la nave del jugador
        if self.alien_lasers_group:
            for alien in self.aliens_grupo:  
                for obstaculo in self.obstaculos:
                    pygame.sprite.spritecollide(alien, obstaculo.blocke_grupo, True)

                if pygame.sprite.spritecollide(alien, self.nave_grupo, False):
                    self.game_over()


    '''
    esta funcion se encargara de finalizar  el juego dependiendo de lo sucedido en el mismo
    '''
    def game_over(self):
        self.corre = False
        try:
            # Intentar cargar y reproducir la música de game over
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sonidos/game_over.mp3')
            pygame.mixer.music.play(-1)
        except pygame.error:
            # Si hay error, solo detener la música actual
            pygame.mixer.music.stop()
        self.corre = False

    #esta funcion se encarga de reiniciar al estado inicial el juego
    def reinicio(self):
         # Detener música de game over y volver a la música del nivel 1
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)
        #todo el juego desde cero
        self.corre = True
        self.vidas = 3
        self.nave_grupo.sprite.reinicio()
        self.aliens_grupo.empty()  #elimina los que estan en la pantalla
        self.alien_lasers_group.empty()
        self.crear_aliens()
        self.nave_misteriosa_grupo.empty()
        self.obstaculos = self.crear_obstaculos()
        self.puntaje = 0
        
    #la funcion de las vidas
    def dibujar_vidas(self, surface):
        """Dibuja los iconos de vidas en la pantalla"""
        for vida in range(self.vidas):
            x = self.vida_offset_x + (vida * self.vida_offset_x)
            self.vida_rect.x = x
            self.vida_rect.y = self.vida_pos_y
            surface.blit(self.image, self.vida_rect)

    def revisar_puntacion_alta(self):
        if self.puntaje > self.puntaje_mas_alto:
            self.puntaje_mas_alto = self.puntaje

            with open('puntaje_alto.txt', "w") as file:
                file.write(str(self.puntaje_mas_alto))

    def cargar_puntaje_alto(self):
        try:

                with open('puntaje_alto.txt', 'r') as file:
                    self.puntaje_mas_alto = int(file.read())
        except FileNotFoundError:
            self.puntaje_mas_alto = 0


