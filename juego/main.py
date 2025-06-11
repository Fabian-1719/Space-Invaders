# --- Importación de módulos necesarios ---
import pygame  # Librería para crear videojuegos 2D, se usa para gráficos, sonidos, eventos, etc.
import sys  # Sirve para poder salir del juego con sys.exit()
import random  # Se usa para generar números aleatorios (por ejemplo, para el evento de nave misteriosa)

# Importamos la clase Game que contiene la lógica del juego
from game import Game

# Importamos clases para las interfaces de usuario
from interfaz_usuario import InterfazUsuario, MenuPrincipal

# Función para obtener o crear un usuario
from usuario import obtener_o_crear_usuario

# Importamos pantallas adicionales: historial de partidas y top 5 jugadores
from pantallas_extras import PantallaHistorial, PantallaTop5


# --- Inicialización de pygame ---
pygame.init()  # Inicializa todos los módulos de Pygame (gráficos, sonido, etc.)

# --- Configuración de pantalla ---
ANCHO_PANTALLA = 750  # Ancho del área de juego
ALTO_PANTALLA = 730   # Alto del área de juego
OFFSET = 50  # Margen usado para centrar o dar espacio a los elementos


# --- Definición de colores en formato RGB ---
Gris = (29, 29, 27)  # Gris oscuro, usado como fondo
MORADO = (128, 0, 128)  # Color para bordes o separadores
ROJO = (255, 0, 0)  # Usado para Game Over o peligro
AMARILLO = (255, 255, 0)  # Usado para texto y puntajes
VERDE = (0, 255, 0)  # Usado para victoria o elementos positivos


# --- Fuente personalizada para los textos ---
font = pygame.font.Font('Font/monogram.ttf', 40)  
# Carga una fuente tipo pixel desde un archivo externo y la usa en tamaño 40


# --- Caja para mostrar "Game Over" ---
game_over_box = pygame.Surface((400, 200))  # Superficie rectangular de 400x200 píxeles
game_over_box.fill(Gris)  # Rellenamos la caja de gris
pygame.draw.rect(game_over_box, ROJO, game_over_box.get_rect(), 2)  # Dibujamos borde rojo de 2px


# --- Texto "Game Over" ---
game_over_superficie = font.render('GAME OVER', False, ROJO)  # Renderiza el texto en rojo
game_over_rect = game_over_superficie.get_rect(center=(200, 70))  # Centra el texto en la caja (posición relativa)


# --- Texto para reiniciar el juego después de Game Over ---
restart_text = font.render(' ENTER para reiniciar', False, ROJO)
restart_rect = restart_text.get_rect(center=(200, 130))


# --- Texto para continuar entre niveles ---
continuar_text = font.render('Enter para continuar ', False, VERDE)
continuar_rect = continuar_text.get_rect(center=(200, 130))


# --- Caja para mensaje de victoria ---
victory_box = pygame.Surface((400, 200))
victory_box.fill(Gris)
pygame.draw.rect(victory_box, VERDE, victory_box.get_rect(), 2)  # Borde verde


# --- Texto "¡VICTORIA!" ---
victory_superficie = font.render('¡VICTORIA!', False, VERDE)
victory_rect = victory_superficie.get_rect(center=(200, 70))

victory_restart_text = font.render(' ENTER para reiniciar', False, VERDE)
victory_restart_rect = victory_restart_text.get_rect(center=(200, 130))


# --- Caja para transición de nivel (cuando pasas al siguiente) ---
transicion_box = pygame.Surface((400, 200))
transicion_box.fill(Gris)
pygame.draw.rect(transicion_box, VERDE, transicion_box.get_rect(), 2)  # Borde verde


# --- Crear ventana principal del juego ---
screen = pygame.display.set_mode((ANCHO_PANTALLA + OFFSET, ALTO_PANTALLA + 2 * OFFSET))
pygame.display.set_caption('Space Invaders')  # Título de la ventana


# --- Superficies para textos fijos de puntuación ---
puntaje_texto_superficie = font.render('SCORE', False, AMARILLO)
puntaje_alto_texto_superficie = font.render('HIGH-SCORE', False, AMARILLO)


# --- Control del tiempo ---
clock = pygame.time.Clock()  # Objeto para controlar la velocidad del bucle (FPS)

# Crear instancia del juego (pasa el alto, ancho y margen)
game = Game(ALTO_PANTALLA, ANCHO_PANTALLA, OFFSET)


# --- Temporizadores para eventos automáticos ---
disparo_laser = pygame.USEREVENT  # Evento personalizado para disparo de alien
pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())  # Se dispara cada cierto tiempo

nave_misteriosa = pygame.USEREVENT + 1  # Otro evento personalizado para la nave misteriosa
pygame.time.set_timer(nave_misteriosa, random.randint(4000, 8000))  # Se activa aleatoriamente entre 4 y 8 segundos


# --- Control para detectar si cambió el nivel ---
nivel_anterior = game.nivel_actual


# --- Crear interfaz y menú ---
interfaz = InterfazUsuario(screen, font)
menu = MenuPrincipal(screen, font)


usuario_confirmado = False
#while para para que se repita hasta que el usuario ingrese el nombre
while not usuario_confirmado:
    interfaz.mostrar_pantalla_inicio()  # Muestra la pantalla para que el usuario ingrese nombre y nickname

    for event in pygame.event.get():  # Revisa todos los eventos (teclado, cerrar ventana, etc.)
        if event.type == pygame.QUIT:  # Si el usuario cierra la ventana
            pygame.quit()
            sys.exit()
        
        if interfaz.manejar_evento_inicio(event):  # Si el usuario presiona ENTER o confirma los datos
            usuario_confirmado = True  # Sale del bucle y continúa


nombre_usuario, nickname = interfaz.obtener_datos()  # Obtiene los valores que el usuario ingresó
obtener_o_crear_usuario(nombre_usuario, nickname)    # Verifica si el usuario existe o lo crea si no
game.set_usuario(nombre_usuario, nickname)           # Guarda los datos en el objeto game

# while para mostrar el menu principal
while True:
    # Paso 2: Menú principal
    modo = None
    #es paara mostrar el menu hasta que el jugador escoja una opcion
    while modo is None:
        menu.mostrar_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            modo = menu.manejar_evento_menu(event)

    if modo == 0:
        # El usuario seleccionó el modo "Niveles" desde el menú
        game.modo = "niveles"  # Se configura el juego para que funcione en modo por niveles
        game.cargar_puntaje_alto()  # Carga el puntaje más alto registrado para este modo desde archivo
        game.nivel_actual = 1  # Se establece el nivel inicial como el 1
        game.reinicio()  # Reinicia todos los elementos del juego (jugador, aliens, obstáculos, etc.)
        game.corre = True  # Activa el juego para que comience la lógica de actualización y dibujo
        break  # Sale del bucle del menú para continuar con el bucle principal del juego


        # lo mismo para los siguientes condicionales
    elif modo == 1:
        game.modo = "infinito"
        game.cargar_puntaje_alto()
        game.nivel_actual = 1
        game.reinicio()
        game.corre = True
        break  # Salir del menú y entrar al juego

    elif modo == 2:
        # El usuario seleccionó ver su historial de partidas
        historial = PantallaHistorial(screen, font, nombre_usuario)  # Crea la pantalla de historial
        historial.mostrar()  # Muestra el historial (bloquea hasta que el usuario salga)
        continue  # Vuelve al bucle del menú para que el usuario elija otra opción

    elif modo == 3:
        # El usuario seleccionó ver el Top 5 de puntajes
        top = PantallaTop5(screen, font)  # Crea la pantalla que muestra los 5 mejores puntajes
        top.mostrar()  # Muestra esa pantalla hasta que el usuario decida salir
        continue  # Regresa al menú para seguir eligiendo otras opciones

#---bucle pincipal de juego en tiempo real---
while True:
    # 🔁 Bucle principal del juego, corre constantemente mientras el juego está activo

    # 👉 Revisión de todos los eventos del sistema (teclado, mouse, timers, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # El usuario cerró la ventana
            pygame.quit()
            sys.exit()

        if event.type == disparo_laser and game.corre:
            # ⏰ Evento temporizado: un alien debe disparar un láser
            game.laser_alien()

        if event.type == nave_misteriosa:
            # ⏰ Evento temporizado: se crea una nave misteriosa (premio o puntos extra)
            game.crear_nave_misteriosa()
            # Se programa el próximo evento entre 4 y 8 segundos
            pygame.time.set_timer(nave_misteriosa, random.randint(4000, 8000))

        # 🎮 Eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game.corre and not game.transicion_nivel:
                # ⏸ Si el juego está detenido y NO está en transición de nivel
                # presionar SPACE reinicia el nivel actual
                game.reinicio()
                pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
                nivel_anterior = game.nivel_actual

            if event.key == pygame.K_RETURN and not game.corre:
                if game.transicion_nivel:
                    # ⏭️ ENTER se usa para continuar al siguiente nivel
                    game.corre = True
                    game.transicion_nivel = False
                    pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
                    nivel_anterior = game.nivel_actual
                else:
                    # 🔁 ENTER también puede reiniciar el nivel si no es transición
                    game.reinicio()
                    pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
                    nivel_anterior = game.nivel_actual

            if event.key == pygame.K_ESCAPE:
                # 🔙 ESCAPE permite volver al menú principal
                game.reinicio()  # Reinicia el estado del juego
                game.corre = False
                game.transicion_nivel = False

                # ⏮️ Se vuelve al bucle del menú
                while True:
                    modo = None 
                    while modo is None:
                        menu.mostrar_menu()
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            modo = menu.manejar_evento_menu(e)

                    if modo == 0:
                        game.modo = "niveles"
                        game.cargar_puntaje_alto()
                        game.nivel_actual = 1
                        game.reinicio()
                        game.corre = True
                        break

                    elif modo == 1:
                        game.modo = "infinito"
                        game.cargar_puntaje_alto()
                        game.nivel_actual = 1
                        game.reinicio()
                        game.corre = True
                        break

                    elif modo == 2:
                        historial = PantallaHistorial(screen, font, nombre_usuario)
                        historial.mostrar()

                    elif modo == 3:
                        top = PantallaTop5(screen, font)
                        top.mostrar()


    #  Si cambió el nivel, se actualiza la frecuencia de disparos de los aliens
    if game.nivel_actual != nivel_anterior:
        pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
        nivel_anterior = game.nivel_actual


    # Actualizar juego
       #  Actualización de elementos del juego solo si el juego está corriendo
    if game.corre:
        game.nave_grupo.update()  # Mueve y actualiza la nave del jugador
        game.mover_aliens()  # Mueve los aliens
        game.alien_lasers_group.update()  # Actualiza los láseres enemigos
        game.nave_misteriosa_grupo.update()  # Actualiza la nave misteriosa
        game.check_colisiones()  # Detecta colisiones entre objetos (balas, aliens, obstáculos, etc.)


        # Lógica del modo infinito si está activo
    if game.modo == "infinito":
        game.jugar_infinito()


          #  Verifica si un power-up temporal expiró
    if game.power_up_activo in ['disparo_rapido', 'inmune']:
        if pygame.time.get_ticks() > game.power_up_duracion:
            if game.power_up_activo == 'disparo_rapido':
                game.nave_grupo.sprite.laser = 50  # Vuelve al valor normal de disparo

            elif game.power_up_activo == 'inmune':
                game.inmune = False  # Quita la inmunidad

            # 🔚 Elimina el power-up
            game.power_up_activo = None
            game.power_up_duracion = 0
            game.power_up_imagen = None

        

    #-------------Seccion donde se dibuja todo en la pantalla---------------

    screen.fill(Gris)  # Limpia la pantalla con fondo gris
    pygame.draw.rect(screen, MORADO, (10, 10, 782, 810), 2, 0, 60, 60, 60, 60)  # Marco exterior
    pygame.draw.line(screen, MORADO, (25, 750), (775, 750), 3)  # Línea separadora inferior

    
    # Dibujar elementos del juego
    if game.nave_grupo.sprite:
        game.nave_grupo.draw(screen)  # Dibuja la nave del jugador
        game.nave_grupo.sprite.lasers_group.draw(screen)  # Dibuja los láseres del jugador


    # Dibujar puntaje
    screen.blit(puntaje_texto_superficie, (50, 15, 50, 50))  # Texto "PUNTAJE"
    formato_puntaje = str(game.puntaje).zfill(5)  # Puntaje con ceros a la izquierda (ej. 00035)
    puntaje_superficie = font.render(str(formato_puntaje), False, AMARILLO)
    screen.blit(puntaje_superficie, (50, 40, 50, 50))


    # Dibujar puntaje más alto + nickname
    screen.blit(puntaje_alto_texto_superficie, (600, 15, 50, 50))  # Texto "MÁXIMO"
    formato_puntaje_alto = f"{game.nickname_puntaje} - {str(game.puntaje_mas_alto).zfill(5)}"
    puntaje_alto_superficie = font.render(formato_puntaje_alto, False, AMARILLO)
    screen.blit(puntaje_alto_superficie, (600, 40))


    # Mostrar modo infinito si aplica
    if game.modo == "infinito":
        infinito_texto = font.render("MODO INFINITO", False, VERDE)
        screen.blit(infinito_texto, (270, 20))

    # Dibujar vidas
    game.dibujar_vidas(screen)  # Dibuja los íconos de vida restantes del jugador


    
    # Dibujar imagen de power-up activo y tiempo restante
    if game.power_up_imagen:
        screen.blit(game.power_up_imagen, (370, 755))  # Imagen del power-up activo

        if game.power_up_duracion > 0:
            # Muestra cuánto tiempo queda del power-up
            tiempo_restante = max(0, (game.power_up_duracion - pygame.time.get_ticks()) // 1000)
            tiempo_texto = font.render(f'{tiempo_restante}s', False, AMARILLO)
            screen.blit(tiempo_texto, (420, 760))


        
    # Dibujar obstáculos y enemigos
    for obstaculo in game.obstaculos:
        obstaculo.blocke_grupo.draw(screen)  # Dibuja los bloques del obstáculo

    game.aliens_grupo.draw(screen)  # Dibuja a todos los aliens
    game.alien_lasers_group.draw(screen)  # Dibuja los láseres de los aliens
    game.nave_misteriosa_grupo.draw(screen)  # Dibuja la nave misteriosa si está activa


    # Dibujar UI según el estado del juego
    if game.corre:
        # Mostrar nivel actual
        nivel_superficie = font.render(game.get_nivel_texto(), False, AMARILLO)
        screen.blit(nivel_superficie, (590, 765))
        
            
    else:
         # Si el juego está detenido (transición, victoria o game over)
        box_x = (ANCHO_PANTALLA + OFFSET - 400) // 2
        box_y = (ALTO_PANTALLA + 2 * OFFSET - 200) // 2

        if game.transicion_nivel:
            # 🟡 TRANSICIÓN DE NIVEL (cuadro verde)
            screen.blit(transicion_box, (box_x, box_y))
            transicion_text = font.render('NIVEL COMPLETADO', False, VERDE)
            transicion_rect = transicion_text.get_rect(center=(200, 70))
            screen.blit(transicion_text, (box_x + transicion_rect.x, box_y + transicion_rect.y))
            screen.blit(continuar_text, (box_x + continuar_rect.x, box_y + continuar_rect.y))

        elif game.nivel_actual > 3 or (game.aliens_eliminados >= game.aliens_iniciales and game.nivel_actual == 3):
            # 🟢 VICTORIA FINAL (usa la misma caja pero con mensaje diferente)
            screen.blit(game_over_box, (box_x, box_y))
            victoria_text = font.render('¡HAS GANADO!', False, ROJO)
            victoria_rect = victoria_text.get_rect(center=(200, 70))
            screen.blit(victoria_text, (box_x + victoria_rect.x, box_y + victoria_rect.y))
            screen.blit(restart_text, (box_x + restart_rect.x, box_y + restart_rect.y))

        else:
            # 🔴 GAME OVER (muerte o colisión)
            screen.blit(game_over_box, (box_x, box_y))
            screen.blit(game_over_superficie, (box_x + game_over_rect.x, box_y + game_over_rect.y))
            screen.blit(restart_text, (box_x + restart_rect.x, box_y + restart_rect.y))
    
    pygame.display.update()  # Actualiza la pantalla con todo lo que se dibujó
    clock.tick(100)  #Limita el juego a 60 cuadros por segundo (FPS)
