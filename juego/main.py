# main.py - Versión actualizada con sistema de niveles

import pygame, sys
from game import Game
import random
from interfaz_usuario import InterfazUsuario, MenuPrincipal
from usuario import obtener_o_crear_usuario
from pantallas_extras import PantallaHistorial, PantallaTop5


pygame.init()

ANCHO_PANTALLA = 750
ALTO_PANTALLA = 730
OFFSET = 50

Gris = (29, 29, 27)
MORADO = (128, 0, 128)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)

# Fuente para textos
font = pygame.font.Font('Font/monogram.ttf', 40)

# Mensaje de game over
game_over_box = pygame.Surface((400, 200))
game_over_box.fill(Gris)
pygame.draw.rect(game_over_box, ROJO, game_over_box.get_rect(), 2)

#texto de game over
game_over_superficie = font.render('GAME OVER', False, ROJO)
game_over_rect = game_over_superficie.get_rect(center=(200, 70))

#texto de reiniciar
restart_text = font.render(' ENTER para reiniciar', False, ROJO)
restart_rect = restart_text.get_rect(center=(200, 130))

#texto de continuar
continuar_text = font.render('Enter para continuar ', False, VERDE)
continuar_rect = continuar_text.get_rect(center=(200, 130))

# Mensaje de victoria
victory_box = pygame.Surface((400, 200))
victory_box.fill(Gris)
pygame.draw.rect(victory_box, VERDE, victory_box.get_rect(), 2)

victory_superficie = font.render('¡VICTORIA!', False, VERDE)
victory_rect = victory_superficie.get_rect(center=(200, 70))

victory_restart_text = font.render(' ENTER para reiniciar', False, VERDE)
victory_restart_rect = victory_restart_text.get_rect(center=(200, 130))

# Cuadro de transición entre niveles
transicion_box = pygame.Surface((400, 200))
transicion_box.fill(Gris)
pygame.draw.rect(transicion_box, VERDE, transicion_box.get_rect(), 2)

screen = pygame.display.set_mode((ANCHO_PANTALLA + OFFSET, ALTO_PANTALLA + 2 * OFFSET))
pygame.display.set_caption('Space Invaders')

# Superficies de texto
puntaje_texto_superficie = font.render('SCORE', False, AMARILLO)
puntaje_alto_texto_superficie = font.render('HIGH-SCORE', False, AMARILLO)

clock = pygame.time.Clock()
game = Game(ALTO_PANTALLA, ANCHO_PANTALLA, OFFSET)

# Temporizadores
disparo_laser = pygame.USEREVENT
# Inicializar con la frecuencia del nivel 1
pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())

nave_misteriosa = pygame.USEREVENT + 1
pygame.time.set_timer(nave_misteriosa, random.randint(4000, 8000))

# Variable para rastrear cambios de nivel
nivel_anterior = game.nivel_actual

interfaz = InterfazUsuario(screen, font)
menu = MenuPrincipal(screen, font)

# Paso 1: Pantalla de inicio (usuario + nickname)
usuario_confirmado = False
while not usuario_confirmado:
    interfaz.mostrar_pantalla_inicio()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if interfaz.manejar_evento_inicio(event):
            usuario_confirmado = True

nombre_usuario, nickname = interfaz.obtener_datos()
obtener_o_crear_usuario(nombre_usuario, nickname)
game.set_usuario(nombre_usuario, nickname)

while True:
    # Paso 2: Menú principal
    modo = None
    while modo is None:
        menu.mostrar_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            modo = menu.manejar_evento_menu(event)

    # Paso 3: Actuar según la opción elegida
    if modo == 0:
        game.modo = "niveles"
        game.nivel_actual = 1
        game.reinicio()
        game.corre = True
        break  # Salir del menú y entrar al juego

    elif modo == 1:
        game.modo = "infinito"
        game.nivel_actual = 1
        game.reinicio()
        game.corre = True
        break  # Salir del menú y entrar al juego

    elif modo == 2:
        historial = PantallaHistorial(screen, font, nombre_usuario)
        historial.mostrar()
        # Volver al menú (no continuar el juego)
        continue

    elif modo == 3:
        top = PantallaTop5(screen, font)
        top.mostrar()
        # Volver al menú
        continue


while True:
    # Revisar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == disparo_laser and game.corre:
            game.laser_alien()
            
        if event.type == nave_misteriosa:
            game.crear_nave_misteriosa()
            pygame.time.set_timer(nave_misteriosa, random.randint(4000, 8000))

        # Manejo de teclas
        if event.type == pygame.KEYDOWN:
            # ✅ SPACE solo reinicia si el juego está detenido y NO está en transición de nivel
            if event.key == pygame.K_SPACE and not game.corre and not game.transicion_nivel:
                game.reinicio()
                pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
                nivel_anterior = game.nivel_actual

            # ✅ ENTER controla tanto transición como reinicio según el caso
            if event.key == pygame.K_RETURN and not game.corre:
                if game.transicion_nivel:
                    game.corre = True
                    game.transicion_nivel = False
                    pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
                    nivel_anterior = game.nivel_actual
                else:
                    game.reinicio()
                    pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
                    nivel_anterior = game.nivel_actual



    # Actualizar frecuencia de disparo si cambió el nivel
    if game.nivel_actual != nivel_anterior:
        pygame.time.set_timer(disparo_laser, game.get_alien_laser_frecuencia())
        nivel_anterior = game.nivel_actual

    # Actualizar juego
    if game.corre:
        game.nave_grupo.update()
        game.mover_aliens()
        game.alien_lasers_group.update()
        game.nave_misteriosa_grupo.update()
        game.check_colisiones()

    if game.modo == "infinito":
        game.jugar_infinito()

        # Desactivar power-ups temporales si expiraron
    if game.power_up_activo in ['disparo_rapido', 'inmune']:
        if pygame.time.get_ticks() > game.power_up_duracion:
            if game.power_up_activo == 'disparo_rapido':
                game.nave_grupo.sprite.laser= 50   # Valor normal

            elif game.power_up_activo == 'inmune':
                game.inmune = False

            game.power_up_activo = None
            game.power_up_duracion = 0
            game.power_up_imagen = None
        

    # Dibujar
    screen.fill(Gris)
    pygame.draw.rect(screen, MORADO, (10, 10, 782, 810), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, MORADO, (25, 750), (775, 750), 3)
    
    # Dibujar elementos del juego
    game.nave_grupo.draw(screen)
    game.nave_grupo.sprite.lasers_group.draw(screen)

    # Dibujar puntaje
    screen.blit(puntaje_texto_superficie, (50, 15, 50, 50))
    formato_puntaje = str(game.puntaje).zfill(5)
    puntaje_superficie = font.render(str(formato_puntaje), False, AMARILLO)
    screen.blit(puntaje_superficie, (50, 40, 50, 50))

    # Dibujar puntaje más alto
    screen.blit(puntaje_alto_texto_superficie, (600, 15, 50, 50))
    formato_puntaje_alto = f"{game.nickname_puntaje} - {str(game.puntaje_mas_alto).zfill(5)}"
    puntaje_alto_superficie = font.render(formato_puntaje_alto, False, AMARILLO)
    screen.blit(puntaje_alto_superficie, (645, 40))

    # Mostrar modo infinito si aplica
    if game.modo == "infinito":
        infinito_texto = font.render("MODO INFINITO", False, VERDE)
        screen.blit(infinito_texto, (270, 20))

    # Dibujar vidas
    game.dibujar_vidas(screen)

    # Dibujar imagen de power-up activo
    # Dibujar imagen de power-up activo y tiempo restante
    if game.power_up_imagen:
        screen.blit(game.power_up_imagen, (370, 755))
        
        # Mostrar tiempo restante si aplica
        if game.power_up_duracion > 0:
            tiempo_restante = max(0, (game.power_up_duracion - pygame.time.get_ticks()) // 1000)
            tiempo_texto = font.render(f'{tiempo_restante}s', False, AMARILLO)
            screen.blit(tiempo_texto, (420, 760))

        
    # Dibujar obstáculos y enemigos
    for obstaculo in game.obstaculos:
        obstaculo.blocke_grupo.draw(screen)
    game.aliens_grupo.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.nave_misteriosa_grupo.draw(screen)

    # Dibujar UI según el estado del juego
    if game.corre:
        # Mostrar nivel actual
        nivel_superficie = font.render(game.get_nivel_texto(), False, AMARILLO)
        screen.blit(nivel_superficie, (590, 765))
        
        # Mostrar indicador de progreso de nivel
        aliens_restantes = len(game.aliens_grupo.sprites())
        if aliens_restantes <= 5:  # Mostrar cuando quedan pocos aliens
            restantes_text = font.render(f'ALIENS: {aliens_restantes}', False, ROJO)
            screen.blit(restantes_text, (300, 765))
            
    else:
        # 🖼️ Mostrar mensaje central cuando el juego está detenido (Game Over, Victoria o Transición)
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

    pygame.display.update()
    clock.tick(60)