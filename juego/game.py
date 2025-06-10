import pygame
import random
from spaceship import Nave
from obstaculos import Obstaculo
from obstaculos import cuadro
from aliens import Alien
from lasers import Laser
from aliens import Nave_misteriosa
from usuario import guardar_partida, guardar_usuarios


class Game:
    def __init__(self, ancho_pantalla, alto_pantalla, offset):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.offset = offset
        self.nave_grupo = pygame.sprite.GroupSingle()
        self.nave_grupo.add(Nave(self.ancho_pantalla, self.alto_pantalla, self.offset))
        self.obstaculos = self.crear_obstaculos()
        self.aliens_grupo = pygame.sprite.Group()
        
        # Sistema de niveles
        self.nivel_actual = 1
        self.aliens_iniciales = 0
        self.aliens_eliminados = 0
        
        self.crear_aliens()
        self.aliens_direccion = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.nave_misteriosa_grupo = pygame.sprite.GroupSingle()
        
        # Configuración de dificultad por nivel
        self.configurar_nivel()
        
        # UI
        self.image = pygame.image.load('graficos/vidas.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.vida_rect = self.image.get_rect()
        self.vida_offset_x = 50
        self.vida_pos_y = 760
        self.vidas = 3
        self.corre = True
        self.puntaje = 0
        self.puntaje_mas_alto = 0
        self.cargar_puntaje_alto()
        
        # Audio
        pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)
        self.explosion_sonido = pygame.mixer.Sound('sonidos/Sounds_explosion.ogg')

        #para que se pause el juego
        self.transicion_nivel = False

        #powers ups
        self.power_up_activo = None
        self.power_up_duracion = 0
        self.power_up_imagen = None
        self.inmune = False

        self.nombre_usuario = ""
        self.nickname = ""

        self.modo = "niveles"  # Valor por defecto
    
    #funcion que configura los siguientes
    def configurar_nivel(self):
        """Configura la dificultad según el nivel actual"""
        if self.nivel_actual == 1:
            self.alien_velocidad = 1
            self.alien_laser_frecuencia = 300  # milisegundos
            self.alien_descenso = 2
            self.nave_misteriosa_puntos = 500
            self.velocidad_nave_misteriosa = 3
            
        elif self.nivel_actual == 2:
            self.alien_velocidad = 1.5
            self.alien_laser_frecuencia = 250  # Más frecuente
            self.alien_descenso = 3
            self.nave_misteriosa_puntos = 750
            self.velocidad_nave_misteriosa = 4
     
        elif self.nivel_actual == 3:
            self.alien_velocidad = 2
            self.alien_laser_frecuencia = 200  # Muy frecuente
            self.alien_descenso = 4
            self.nave_misteriosa_puntos = 1000
            self.velocidad_nave_misteriosa = 5
            # Agregar aún más aliens y diferentes patrones

    def crear_obstaculos(self):
        """Crea obstáculos con durabilidad variable según el nivel"""
        ancho_obstaculo = len(cuadro[0]) * 3
        brecha = ((self.ancho_pantalla + self.offset) - (4 * ancho_obstaculo)) / 5
        
        obstaculos = []
        for i in range(4):
            desplazamiento_x = (i + 1) * brecha + i * ancho_obstaculo
            obstaculo = Obstaculo(desplazamiento_x, self.alto_pantalla - 110)
            obstaculos.append(obstaculo)
        return obstaculos

    def crear_aliens(self):
        """Crea aliens con configuraciones específicas por nivel"""
        # Limpiar grupo existente
        self.aliens_grupo.empty()
        
        if self.nivel_actual == 1:
            # Configuración original - 5 filas, 11 columnas
            filas = 5
            columnas = 11
            
        elif self.nivel_actual == 2:
            # Más aliens - 6 filas, 11 columnas
            filas = 6
            columnas = 11
            
        elif self.nivel_actual == 3:
            # Configuración máxima - 7 filas, 12 columnas
            filas = 7
            columnas = 12

        for fila in range(filas):
            for columna in range(columnas):
                x = 75 + columna * 55
                y = 110 + fila * 55

                # Determinar tipo de alien según la fila
                if fila == 0:
                    alien_type = 3
                elif fila in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1
                    
                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_grupo.add(alien)
        
        # Contar aliens iniciales para detectar cuando el nivel esté completo
        self.aliens_iniciales = len(self.aliens_grupo.sprites())
        self.aliens_eliminados = 0

    def mover_aliens(self):
        """Mueve aliens con velocidad variable según el nivel"""
        # Velocidad ajustada por nivel
        direccion_actual = self.aliens_direccion * self.alien_velocidad
        self.aliens_grupo.update(direccion_actual)
        
        alien_sprites = self.aliens_grupo.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= 775:
                self.aliens_direccion = -1
                self.mover_aliens_abajo(self.alien_descenso)
                break
            elif alien.rect.left <= 25:
                self.aliens_direccion = 1
                self.mover_aliens_abajo(self.alien_descenso)
                break

    def mover_aliens_abajo(self, distancia):
        """Mueve aliens hacia abajo con distancia variable por nivel"""
        if self.aliens_grupo:
            for alien in self.aliens_grupo.sprites():
                alien.rect.y += distancia

    def laser_alien(self):
        """Disparo de aliens con frecuencia ajustada por nivel"""
        if self.aliens_grupo.sprites():
            # En niveles superiores, puede disparar más de un alien a la vez
            num_disparos = 1
            if self.nivel_actual == 2:
                num_disparos = random.choice([1, 2])
            elif self.nivel_actual == 3:
                num_disparos = random.choice([1, 2, 3])
            
            for _ in range(num_disparos):
                if self.aliens_grupo.sprites():
                    random_alien = random.choice(self.aliens_grupo.sprites())
                    laser_sprite = Laser(random_alien.rect.center, -6, self.alto_pantalla)
                    self.alien_lasers_group.add(laser_sprite)

    def crear_nave_misteriosa(self):
        """Crea nave misteriosa con velocidad ajustada por nivel"""
        nave_misteriosa = Nave_misteriosa(self.ancho_pantalla, self.offset)
        # Ajustar velocidad según el nivel
        if nave_misteriosa.velocidad > 0:
            nave_misteriosa.velocidad = self.velocidad_nave_misteriosa
        else:
            nave_misteriosa.velocidad = -self.velocidad_nave_misteriosa
        self.nave_misteriosa_grupo.add(nave_misteriosa)

    def check_colisiones(self):
        """Verifica colisiones y maneja progresión de niveles"""
        # Nave vs Aliens
        if self.nave_grupo.sprite.lasers_group:
            for laser_sprite in self.nave_grupo.sprite.lasers_group:
                alien_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_grupo, True)
                if alien_hit:
                    self.explosion_sonido.play()
                    for alien in alien_hit:
                        self.revisar_puntacion_alta(self.nickname)
                        puntos_base = alien.type * 100
                        puntos_nivel = puntos_base * self.nivel_actual
                        self.puntaje += puntos_nivel
                        laser_sprite.kill()
                        self.aliens_eliminados += 1

                        # Verificar si se completó el nivel
                        if self.aliens_eliminados >= self.aliens_iniciales:
                            if self.modo == "niveles":
                                self.siguiente_nivel()
            # En modo infinito NO se avanza de nivel aquí — se maneja por jugar_infinito()

                # Nave misteriosa
                if pygame.sprite.spritecollide(laser_sprite, self.nave_misteriosa_grupo, True):
                    self.puntaje += self.nave_misteriosa_puntos
                    self.revisar_puntacion_alta(self.nickname)
                    self.explosion_sonido.play()
                    laser_sprite.kill()

                    self.activar_power_up()


                # Obstáculos
                for obstaculo in self.obstaculos:
                    if pygame.sprite.spritecollide(laser_sprite, obstaculo.blocke_grupo, True):
                        laser_sprite.kill()

        # Laser de aliens vs Nave
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.nave_grupo, False):
                    laser_sprite.kill()
                    if not self.inmune: # para saber si la nave esta con la inmunidad
                        self.vidas -= 1
                        if self.vidas == 0:
                            self.game_over()

                # Obstáculos
                for obstaculo in self.obstaculos:
                    if pygame.sprite.spritecollide(laser_sprite, obstaculo.blocke_grupo, True):
                        laser_sprite.kill()

        # Aliens vs Obstáculos y Nave
        if self.aliens_grupo:
            for alien in self.aliens_grupo:
                for obstaculo in self.obstaculos:
                    pygame.sprite.spritecollide(alien, obstaculo.blocke_grupo, True)

                if pygame.sprite.spritecollide(alien, self.nave_grupo, False):
                    self.game_over()

    def siguiente_nivel(self):
        """Avanza al siguiente nivel o continúa infinito"""
        self.nivel_actual += 1
        self.configurar_nivel()

        if self.modo == "niveles" and self.nivel_actual > 3:
            self.victoria()
            return

        # Reconfigurar
        pygame.mixer.music.stop()
        if self.modo == "niveles":
            pygame.mixer.music.load('sonidos/nivel_2.mp3')
        else:
            pygame.mixer.music.load('sonidos/Sounds_music.ogg')  # misma música en infinito

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)

        self.crear_aliens()
        self.obstaculos = self.crear_obstaculos()

        self.puntaje += 1000 * self.nivel_actual
        self.revisar_puntacion_alta(self.nickname)

        if self.vidas < 2:
            self.vidas += 1

        self.corre = False
        self.transicion_nivel = True


    def victoria(self):
        """Maneja la victoria del juego"""
        self.corre = False
        self.puntaje += 5000  # Bonificación por completar todos los niveles
        self.revisar_puntacion_alta(self.nickname)
        # Aquí podrías agregar música de victoria
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sonidos/victoria.mp3')  # Si tienes este archivo
            pygame.mixer.music.play(-1)
        except pygame.error:
            pygame.mixer.music.stop()
        

    def game_over(self):
        """Finaliza el juego"""
        self.corre = False
        
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sonidos/game_over.mp3')
            pygame.mixer.music.play(-1)
        except pygame.error:
            pygame.mixer.music.stop()
        guardar_partida(self.nombre_usuario, self.puntaje, "infinito")

    def jugar_infinito(self):
        """Loop del nivel infinito: aliens se regeneran automáticamente con más dificultad."""
        if not self.aliens_grupo:
            self.nivel_actual += 1  # Usamos esto para escalar dificultad
            self.configurar_nivel_infinito()
            self.crear_aliens()
            self.obstaculos = self.crear_obstaculos()
            self.puntaje += 250 * self.nivel_actual
            self.revisar_puntacion_alta(self.nickname)

    def configurar_nivel_infinito(self):
        """Escala la dificultad para modo infinito."""
        self.alien_velocidad = min(1 + self.nivel_actual * 0.2, 5)
        self.alien_laser_frecuencia = max(300 - self.nivel_actual * 10, 80)
        self.alien_descenso = min(2 + self.nivel_actual // 2, 6)
        self.nave_misteriosa_puntos = 500 + (self.nivel_actual * 100)
        self.velocidad_nave_misteriosa = min(3 + self.nivel_actual // 2, 8)
    def reinicio(self):
        """Reinicia el juego al nivel 1"""
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)
        
        # Resetear todo al estado inicial
        self.corre = True
        self.vidas = 3
        self.nivel_actual = 1
        if self.modo == "infinito":
            self.configurar_nivel_infinito()
        else:
            self.configurar_nivel()

        
        self.nave_grupo.sprite.reinicio()
        self.aliens_grupo.empty()
        self.alien_lasers_group.empty()
        self.crear_aliens()
        self.nave_misteriosa_grupo.empty()
        self.obstaculos = self.crear_obstaculos()
        self.puntaje = 0
        self.transicion_nivel = False

    def get_alien_laser_frecuencia(self):
        """Retorna la frecuencia de disparo actual para usar en main.py"""
        return self.alien_laser_frecuencia

    def get_nivel_texto(self):
    #Retorna el texto del nivel actual u oleada según el modo
        if self.modo == "infinito":
            return f"OLEADA {self.nivel_actual:02d}"
        else:
            return f"NIVEL {self.nivel_actual:02d}"



    def dibujar_vidas(self, surface):
        """Dibuja los iconos de vidas en la pantalla"""
        for vida in range(self.vidas):
            x = self.vida_offset_x + (vida * self.vida_offset_x)
            self.vida_rect.x = x
            self.vida_rect.y = self.vida_pos_y
            surface.blit(self.image, self.vida_rect)

    def revisar_puntacion_alta(self, nickname):
        if self.puntaje > self.puntaje_mas_alto:
            self.puntaje_mas_alto = self.puntaje
            with open('puntaje_alto.txt', "w") as file:
                file.write(f"{nickname} - {self.puntaje_mas_alto}")

    def cargar_puntaje_alto(self):
        try:
            with open('puntaje_alto.txt', 'r') as file:
                contenido = file.read().strip()
                if ' - ' in contenido:
                    self.nickname_puntaje, valor = contenido.split(" - ")
                    self.puntaje_mas_alto = int(valor)
                else:
                    self.nickname_puntaje = '---'
                    self.puntaje_mas_alto = 0
        except FileNotFoundError:
            self.nickname_puntaje = '---'
            self.puntaje_mas_alto = 0



    def activar_power_up(self):
        self.power_up_activo = random.choice(['vida', 'disparo_rapido', 'inmune'])

        if self.power_up_activo == 'vida':
            self.vidas += 1
            self.power_up_duracion = 0
            self.power_up_imagen = None  # No mostrar imagen

        elif self.power_up_activo == 'disparo_rapido':
            self.power_up_duracion = pygame.time.get_ticks() + 5000
            self.nave_grupo.sprite.frecuencia_disparo = 150  # Mucho más rápido

        elif self.power_up_activo == 'inmune':
            self.power_up_duracion = pygame.time.get_ticks() + 5000
            self.inmune = True

        if self.power_up_activo in ['disparo_rapido', 'inmune']:
            try:
                self.power_up_imagen = pygame.image.load(f'graficos/power_{self.power_up_activo}.png')
                self.power_up_imagen = pygame.transform.scale(self.power_up_imagen, (40, 40))
            except:
                self.power_up_imagen = None

    def set_usuario(self, nombre_usuario, nickname):
        self.nombre_usuario = nombre_usuario
        self.nickname = nickname
