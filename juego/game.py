import pygame                                    # Importa pygame para gráficos, sonido y manejo de sprites
import random                                    # Para generar valores aleatorios (ejemplo: disparos y power-ups)

from spaceship import Nave                       # Importa la clase Nave, que representa al jugador
from obstaculos import Obstaculo
from obstaculos import cuadro                    # Importa la matriz para formar los obstáculos defensivos
from aliens import Alien
from lasers import Laser
from aliens import Nave_misteriosa             # Nave especial que aparece ocasionalmente
from usuario import guardar_partida, guardar_usuarios

# clase que maneja toda la logica del juego
class Game:
    def __init__(self, ancho_pantalla, alto_pantalla, offset):
        # Guarda las dimensiones y margen de la ventana
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.offset = offset

        # Crea un grupo con la nave del jugador
        self.nave_grupo = pygame.sprite.GroupSingle()
        self.nave_grupo.add(Nave(self.ancho_pantalla, self.alto_pantalla, self.offset))

        # Genera los obstáculos protectores
        self.obstaculos = self.crear_obstaculos()

        # Grupo de aliens enemigos
        self.aliens_grupo = pygame.sprite.Group()
        
        # Inicializa contador del sistema de niveles
        self.nivel_actual = 1
        self.aliens_iniciales = 0
        self.aliens_eliminados = 0
        
        # Crea la formación inicial de aliens
        self.crear_aliens()
        # Dirección de movimiento inicial (+1 = derecha, -1 = izquierda)
        self.aliens_direccion = 1

        # Grupo para los disparos de los aliens
        self.alien_lasers_group = pygame.sprite.Group()

        # Nave misteriosa (grupo de uno solo)
        self.nave_misteriosa_grupo = pygame.sprite.GroupSingle()
        
        # Configura dificultad según nivel
        self.configurar_nivel()
        
        # Carga el gráfico para las vidas
        self.image = pygame.image.load('graficos/vidas.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.vida_rect = self.image.get_rect()

        # Variables para dibujar las vidas en pantalla
        self.vida_offset_x = 50
        self.vida_pos_y = 760
        self.vidas = 3

        # Estado general del juego
        self.corre = True                   # True = juego en curso
        self.puntaje = 0                    # Puntaje actual
        self.puntaje_mas_alto = 0          # Mejor puntaje registrado
        self.modo = "niveles"              # "niveles" o "infinito"
        self.cargar_puntaje_alto()         # Lee puntaje acumulado del archivo

        # Carga la música de fondo y el sonido de explosión
        pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)
        self.explosion_sonido = pygame.mixer.Sound('sonidos/Sounds_explosion.ogg')

        # Control de transición entre niveles
        self.transicion_nivel = False

        # Power-ups (inmunidad, disparo rápido, vida extra)
        self.power_up_activo = None
        self.power_up_duracion = 0
        self.power_up_imagen = None
        self.inmune = False

        # Datos del jugador
        self.nombre_usuario = ""
        self.nickname = ""

    #funcion con la logica para el nivel infinito
    # Función con la lógica para ajustar la dificultad en el modo infinito
    def configurar_nivel_infinito(self):
        """Aumenta la dificultad automáticamente en modo infinito según el nivel actual."""

        # Aumenta la velocidad de movimiento horizontal de los aliens.
        # Comienza en 1 y aumenta 0.2 por cada nivel, hasta un máximo de 5.
        self.alien_velocidad = min(1 + self.nivel_actual * 0.2, 5)

        # Disminuye el intervalo entre disparos de los aliens (es decir, disparan más seguido).
        # Parte de 300 fotogramas y se reduce 10 por cada nivel, con un mínimo de 80.
        self.alien_laser_frecuencia = max(300 - self.nivel_actual * 10, 80)

        # Aumenta la cantidad de píxeles que los aliens descienden al tocar los bordes.
        # Comienza en 2 y sube 1 cada 2 niveles, hasta un máximo de 6.
        self.alien_descenso = min(2 + self.nivel_actual // 2, 6)

        # Incrementa la cantidad de puntos que otorga la nave misteriosa.
        # Comienza en 500 y suma 100 por cada nivel.
        self.nave_misteriosa_puntos = 500 + (self.nivel_actual * 100)

        # Aumenta la velocidad de la nave misteriosa.
        # Comienza en 3 y sube 1 cada 2 niveles, con un tope de 8.
        self.velocidad_nave_misteriosa = min(3 + self.nivel_actual // 2, 8)


    #funcion con la logica para los diferentes niveles
    def configurar_nivel(self):
        """Ajusta parámetros de dificultad por cada nivel (1, 2 o 3)."""
        #para nivel 1
        if self.nivel_actual == 1:
            self.alien_velocidad = 1
            self.alien_laser_frecuencia = 300  # tiempo entre disparos
            self.alien_descenso = 2
            self.nave_misteriosa_puntos = 500
            self.velocidad_nave_misteriosa = 3

        #para nivel 2
        elif self.nivel_actual == 2:
            self.alien_velocidad = 1.5
            self.alien_laser_frecuencia = 250
            self.alien_descenso = 3
            self.nave_misteriosa_puntos = 750
            self.velocidad_nave_misteriosa = 4

        #para nivel 3
        elif self.nivel_actual == 3:
            self.alien_velocidad = 2
            self.alien_laser_frecuencia = 200
            self.alien_descenso = 4
            self.nave_misteriosa_puntos = 1000
            self.velocidad_nave_misteriosa = 5

    #funcion que crea los obstaculos
    def crear_obstaculos(self):
        """Construye 4 escudos defensivos bajo la nave protegiéndola."""
        ancho_obstaculo = len(cuadro[0]) * 3   # ancho en píxeles de la matriz
        brecha = ((self.ancho_pantalla + self.offset) - (4 * ancho_obstaculo)) / 5

        obstaculos = []
        for i in range(4):
            # Determina posición de cada obstáculo
            desplazamiento_x = (i + 1) * brecha + i * ancho_obstaculo
            obst = Obstaculo(desplazamiento_x, self.alto_pantalla - 110)
            obstaculos.append(obst)
        return obstaculos

    #funcion que crea los aliens
    def crear_aliens(self):
        """Forma la flota de aliens según niveles (más filas y columnas en niveles altos)."""
        self.aliens_grupo.empty()

        if self.nivel_actual == 1:
            filas, columnas = 5, 11
        elif self.nivel_actual == 2:
            filas, columnas = 6, 11
        else:
            filas, columnas = 7, 12

        for fila in range(filas):
            for columna in range(columnas):
                x = 75 + columna * 55
                y = 110 + fila * 55
                # Determina tipo de alien basado en la fila (filas superiores dan más puntaje)
                if fila == 0:
                    alien_type = 3
                elif fila in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1
                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_grupo.add(alien)

        self.aliens_iniciales = len(self.aliens_grupo.sprites())  # Cantidad total inicial
        self.aliens_eliminados = 0  # Recuento de eliminados reseteado
    
    #funcion encargada del movimiento de los aliens
    def mover_aliens(self):
        """Mueve los aliens horizontalmente y los hace descender al rebotar en los bordes."""
        direccion_actual = self.aliens_direccion * self.alien_velocidad
        self.aliens_grupo.update(direccion_actual)

        for alien in self.aliens_grupo.sprites():
            if alien.rect.right >= 775:
                self.aliens_direccion = -1   # Cambia dirección a izquierda
                self.mover_aliens_abajo(self.alien_descenso)
                break
            elif alien.rect.left <= 25:
                self.aliens_direccion = 1    # Cambia dirección a derecha
                self.mover_aliens_abajo(self.alien_descenso)
                break
                
    #funcion encargada de mover los aliens hacia abajo
    def mover_aliens_abajo(self, distancia):
        """Hace que todos los aliens bajen verticalmente una cantidad dada."""
        for alien in self.aliens_grupo.sprites():
            alien.rect.y += distancia

    #funcion de los laseres de los aliens
    def laser_alien(self):
        """Genera disparos de aliens aleatorios según nivel (1, 2 o 3 disparos)."""
        if self.aliens_grupo.sprites():
            num_disparos = 1
            if self.nivel_actual == 2:
                num_disparos = random.choice([1, 2])
            elif self.nivel_actual == 3:
                num_disparos = random.choice([1, 2, 3])

            for _ in range(num_disparos):
                random_alien = random.choice(self.aliens_grupo.sprites())
                laser = Laser(random_alien.rect.center, -6, self.alto_pantalla)
                self.alien_lasers_group.add(laser)

    #funcion que crea la nave misteriosa
    def crear_nave_misteriosa(self):
        """Crea una nave misteriosa que cruza la pantalla y da puntos extra si se destruye."""
        nm = Nave_misteriosa(self.ancho_pantalla, self.offset)
        # Ajusta su velocidad basándose en el nivel actual
        nm.velocidad = self.velocidad_nave_misteriosa if nm.velocidad > 0 else -self.velocidad_nave_misteriosa
        self.nave_misteriosa_grupo.add(nm)

    #funcion encargada de la logica de las ccolisiones
    def check_colisiones(self):
        """Comprueba todas las colisiones y aplica la lógica del juego (puntos, vidas, power-ups, etc.)."""
        if self.nave_grupo.sprite.lasers_group:
            for laser in self.nave_grupo.sprite.lasers_group:
                # Colisión láser de jugador vs aliens
                alien_hit = pygame.sprite.spritecollide(laser, self.aliens_grupo, True)
                if alien_hit:
                    self.explosion_sonido.play()
                    for alien in alien_hit:
                        # Guarda puntaje alto si lo supera
                        self.revisar_puntacion_alta(self.nickname)
                        puntos = alien.type * 100 * self.nivel_actual
                        self.puntaje += puntos
                        laser.kill()
                        self.aliens_eliminados += 1

                        if self.aliens_eliminados >= self.aliens_iniciales and self.modo == "niveles":
                            self.siguiente_nivel()

                # Colisión láser de jugador vs nave misteriosa
                if pygame.sprite.spritecollide(laser, self.nave_misteriosa_grupo, True):
                    self.puntaje += self.nave_misteriosa_puntos
                    self.revisar_puntacion_alta(self.nickname)
                    self.explosion_sonido.play()
                    laser.kill()
                    self.activar_power_up()

                # Colisión láser de jugador vs obstáculos
                for obstaculo in self.obstaculos:
                    if pygame.sprite.spritecollide(laser, obstaculo.blocke_grupo, True):
                        laser.kill()

        # Colisión láser de aliens vs nave del jugador
        for laser in self.alien_lasers_group:
            if pygame.sprite.spritecollide(laser, self.nave_grupo, False):
                laser.kill()
                if not self.inmune:
                    self.vidas -= 1
                    if self.vidas == 0:
                        self.game_over()
            # Colisión láser de aliens vs obstáculos
            for obstaculo in self.obstaculos:
                if pygame.sprite.spritecollide(laser, obstaculo.blocke_grupo, True):
                    laser.kill()

        # Colisión aliens vs obstáculos y jugador
        for alien in self.aliens_grupo:
            for obstaculo in self.obstaculos:
                pygame.sprite.spritecollide(alien, obstaculo.blocke_grupo, True)
            if pygame.sprite.spritecollide(alien, self.nave_grupo, False):
                self.game_over()

    #funcion que se encarga de la logica para pasar de nivel
    def siguiente_nivel(self):
        """Pasa al siguiente nivel o lanza la pantalla de victoria al terminar."""
        self.nivel_actual += 1
        self.configurar_nivel()
        if self.modo == "niveles" and self.nivel_actual > 3:
            self.victoria()
            return

        # Cambia música según nivel
        pygame.mixer.music.stop()
        if self.nivel_actual == 2:
            pygame.mixer.music.load('sonidos/nivel_2.mp3')
        elif self.nivel_actual == 3:
            pygame.mixer.music.load('sonidos/nivel_3.mp3')
        else:
            pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)

        # Reinicia aliens y obstáculos para nuevo nivel
        self.crear_aliens()
        self.obstaculos = self.crear_obstaculos()

        # Bonificación de nivel
        self.puntaje += 1000 * self.nivel_actual
        self.revisar_puntacion_alta(self.nickname)

        # Vida extra opcional
        if self.vidas < 2:
            self.vidas += 1

        # Pausa para transición entre niveles
        self.corre = False
        self.transicion_nivel = True

    #funcion de victoria para cuando se acabe el juego
    def victoria(self):
        """Gestiona la condición de victoria al completar todos los niveles."""
        self.corre = False
        self.puntaje += 5000  # Bonus de victoria
        self.revisar_puntacion_alta(self.nickname)
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sonidos/victoria.mp3')
            pygame.mixer.music.play(-1)
        except pygame.error:
            pygame.mixer.music.stop()
    
    #funcion de game over
    def game_over(self):
        """Lógica al perder: pausa el juego, guarda puntaje y quita la nave."""
        self.corre = False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sonidos/game_over.mp3')
            pygame.mixer.music.play(-1)
        except pygame.error:
            pygame.mixer.music.stop()
        guardar_partida(self.nombre_usuario, self.puntaje, self.modo)
        self.nave_grupo.empty()

    #funcion para el modo infinito
    def jugar_infinito(self):
        """Genera nuevas oleadas infinitamente con dificultad creciente."""
        if not self.aliens_grupo:
            self.nivel_actual += 1
            self.configurar_nivel_infinito()
            self.crear_aliens()
            self.obstaculos = self.crear_obstaculos()
            self.puntaje += 250 * self.nivel_actual
            self.revisar_puntacion_alta(self.nickname)

    #funcion para reiniciar el juego
    def reinicio(self):
        """Reinicia el juego para empezar de nuevo desde nivel 1."""
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sonidos/Sounds_music.ogg')
        pygame.mixer.music.play(-1)

        self.corre = True
        self.vidas = 3
        self.nivel_actual = 1
        if self.modo == "infinito":
            self.configurar_nivel_infinito()
        else:
            self.configurar_nivel()

        # Reinicia todos los elementos principales del juego
        self.nave_grupo.empty()
        self.nave_grupo.add(Nave(self.ancho_pantalla, self.alto_pantalla, self.offset))
        self.aliens_grupo.empty()
        self.alien_lasers_group.empty()
        self.crear_aliens()
        self.nave_misteriosa_grupo.empty()
        self.obstaculos = self.crear_obstaculos()
        self.puntaje = 0
        self.transicion_nivel = False

#funcion para la frecuencia de disparo de los aliens
    def get_alien_laser_frecuencia(self):
        """Devuelve el tiempo en ms entre disparos de aliens (para temporizadores)."""
        return self.alien_laser_frecuencia

    def get_nivel_texto(self):
        """Devuelve el texto mostrado en pantalla: nivel u oleada según el modo."""
        if self.modo == "infinito":
            return f"OLEADA {self.nivel_actual:02d}"
        return f"NIVEL {self.nivel_actual:02d}"

    
    def dibujar_vidas(self, surface):
        """Dibuja íconos de vida en la interfaz según cantidad."""
        for vida in range(self.vidas):
            x = self.vida_offset_x + vida * self.vida_offset_x
            self.vida_rect.x = x
            self.vida_rect.y = self.vida_pos_y
            surface.blit(self.image, self.vida_rect)

    #funcion que se encarga de revisar la puntuacion 
    def revisar_puntacion_alta(self, nickname):
        """
        Si el puntaje actual supera el mayor registrado, lo guarda en archivo,
        dependiendo del modo de juego (niveles o infinito).
        """
        archivo = 'puntaje_alto_niveles.txt' if self.modo == 'niveles' else 'puntaje_alto_infinito.txt'
        if self.puntaje > self.puntaje_mas_alto:
            self.puntaje_mas_alto = self.puntaje
            with open(archivo, "w") as file:
                file.write(f"{nickname} - {self.puntaje_mas_alto}")

    #Funcion encargada de cargar el puntaje mas alto
    def cargar_puntaje_alto(self):
        """Carga el puntaje más alto del archivo correspondiente en memoria."""
        archivo = 'puntaje_alto_niveles.txt' if self.modo == 'niveles' else 'puntaje_alto_infinito.txt'
        try:
            with open(archivo, 'r') as file:
                contenido = file.read().strip()
                if ' - ' in contenido:
                    self.nickname_puntaje, valor = contenido.split(" - ")
                    self.puntaje_mas_alto = int(valor)
                else:
                    self.nickname_puntaje, self.puntaje_mas_alto = '---', 0
        except FileNotFoundError:
            self.nickname_puntaje, self.puntaje_mas_alto = '---', 0

 #funcion que maneja la activacion de los powewr-ups
    def activar_power_up(self):
        """Activa un power-up aleatorio: vida extra, disparo rápido o inmunidad."""
        self.power_up_activo = random.choice(['vida', 'disparo_rapido', 'inmune'])
        if self.power_up_activo == 'vida':
            self.vidas += 1
            self.power_up_duracion = 0
            self.power_up_imagen = None
        elif self.power_up_activo == 'disparo_rapido':
            self.power_up_duracion = pygame.time.get_ticks() + 5000
            self.nave_grupo.sprite.frecuencia_disparo = 150
        elif self.power_up_activo == 'inmune':
            self.power_up_duracion = pygame.time.get_ticks() + 5000
            self.inmune = True

        if self.power_up_activo in ['disparo_rapido', 'inmune']:
            try:
                ruta = f'graficos/power_{self.power_up_activo}.png'
                img = pygame.image.load(ruta)
                self.power_up_imagen = pygame.transform.scale(img, (40, 40))
            except:
                self.power_up_imagen = None

    def set_usuario(self, nombre_usuario, nickname):
         #Guarda los datos del usuario actual para registrar puntajes.
        self.nombre_usuario = nombre_usuario
        self.nickname = nickname
