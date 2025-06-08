import pygame, sys
from game import Game
import random



pygame.init()

ANCHO_PANTALLA = 750
ALTO_PANTALLA = 730
OFFSET = 50


Gris = (29, 29, 27)
MORADO = (128, 0, 128)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# superficie que muentra el mensaje de el nivel en que te encuentras 
font = pygame.font.Font('Font/monogram.ttf', 40)  # crea una funte para el mensaje de texto
nivel_superficie =font.render('NIVEL 01', False, AMARILLO ) # el False es para no usar el argumento anti-alias por que se esta usando pixelart

#mensaje de game over
# Crear superficie para el cuadro de Game Over
game_over_box = pygame.Surface((400, 200))
game_over_box.fill(Gris)
pygame.draw.rect(game_over_box, ROJO, game_over_box.get_rect(), 2)

# Centrar el texto "GAME OVER" en el cuadro
game_over_superficie = font.render('GAME OVER', False, ROJO)
game_over_rect = game_over_superficie.get_rect(center=(200, 70))

# Agregar texto de instrucción
restart_text = font.render(' ENTER para reiniciar', False, ROJO)
restart_rect = restart_text.get_rect(center=(200, 130))

screen = pygame.display.set_mode((ANCHO_PANTALLA + OFFSET, ALTO_PANTALLA + 2 * OFFSET))
pygame.display.set_caption('Space Invaders')

#muestra el puntaje del jugador actual
puntaje_texto_superficie = font.render('SCORE', False, AMARILLO)

#muestra la puntuacion mas alta
puntaje_alto_texto_superficie = font.render('HIGH-SCORE',  False, AMARILLO)

clock = pygame.time.Clock()

game = Game(ALTO_PANTALLA, ANCHO_PANTALLA, OFFSET)

#un temporizador para que los lasers no se disparen a lo loco
disparo_laser =  pygame.USEREVENT  #userevent es para crear eventos perspnalizados
pygame.time.set_timer(disparo_laser, 300) #con esto se consigue que disparen  cada 300 milisegundos

# se creara un temporizador que sera el encargado de ecir cada cuanto aparece la nave misteriosa
nave_misteriosa = pygame.USEREVENT + 1
pygame.time.set_timer(nave_misteriosa,random.randint(4000, 8000))

while True:
    # revisa los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == disparo_laser and game.corre:
            game.laser_alien()         

        if event.type == nave_misteriosa:
            game.crear_nave_misteriosa()
            pygame.time.set_timer(nave_misteriosa,random.randint(4000, 8000))

        #esto hara que si se presione la tecla de espacio se reinicie el juego si ya se perdieron todas las vidas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.corre == False:
            game.reinicio()

    #actualizando constantementea
    if game.corre:
        game.nave_grupo.update()
        game.mover_aliens()
        game.alien_lasers_group.update()
        game.nave_misteriosa_grupo.update()
        game.check_colisiones()

    

    # dibuja 
    screen.fill(Gris)
    #dibuja un rectangulo en la pantalla. tamaño . grosor. radios de las esquinas       
    pygame.draw.rect(screen, MORADO, (10, 10, 782, 810 ), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, MORADO, (25, 750), (775, 750), 3)
    game.nave_grupo.draw(screen)
    game.nave_grupo.sprite.lasers_group.draw(screen)   #dibuja los lasers

    #dibuja el puntaje
    screen.blit(puntaje_texto_superficie, (50, 15, 50, 50))
    formato_puntaje = str(game.puntaje).zfill(5)   # convierte la puntuacion en una cadena llena de 5 ceros
    puntaje_superficie = font.render(str(formato_puntaje), False, AMARILLO)
    screen.blit(puntaje_superficie, (50, 40, 50, 50))

    #dibuja el puntaje mas alto
    screen.blit(puntaje_alto_texto_superficie, (600, 15, 50, 50))
    formato_puntaje_alto = str(game.puntaje_mas_alto).zfill(5)
    puntaje_alto_superficie = font.render(formato_puntaje_alto, False, AMARILLO)
    screen.blit(puntaje_alto_superficie, (645, 40))

    #dibuja las vidas
    game.dibujar_vidas(screen)
    
    for obstaculo in game.obstaculos:
        obstaculo.blocke_grupo.draw(screen)
    game.aliens_grupo.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.nave_misteriosa_grupo.draw(screen)
  
    #se usara el metodo blit que es para transeferir de imagen en bloque la mayor parte del tiempo
    if game.corre:
        screen.blit(nivel_superficie, (590, 765))
    else:
        # Calcular posición central de la pantalla
        box_x = (ANCHO_PANTALLA + OFFSET - 400) // 2
        box_y = (ALTO_PANTALLA + 2 * OFFSET - 200) // 2
        
        # Dibuja el cuadro y los textos que trabaj en el game over
        if game.corre:
            screen.blit(nivel_superficie, (590, 765))
        else:
            box_x = (ANCHO_PANTALLA + OFFSET - 400) // 2
            box_y = (ALTO_PANTALLA + 2 * OFFSET - 200) // 2
            screen.blit(game_over_box, (box_x, box_y))
            screen.blit(game_over_superficie, (box_x + game_over_rect.x, box_y + game_over_rect.y))
            screen.blit(restart_text, (box_x + restart_rect.x, box_y + restart_rect.y))

        
        # Verificar si se presiona ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # RETURN es la tecla Enter
            game.reinicio()

    pygame.display.update()
    clock.tick(60)                     # la cantidad de fotogramas