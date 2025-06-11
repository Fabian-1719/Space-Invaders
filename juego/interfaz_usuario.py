
import pygame
from usuario import obtener_o_crear_usuario  # Función externa para manejar usuarios

# Colores predefinidos
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_OSCURO = (30, 30, 30)
BORDO = (128, 0, 64)
ROJO = (255, 0, 0)

#  Clase que gestiona la pantalla de ingreso de usuario y nickname
class InterfazUsuario:
    def __init__(self, pantalla, font):
        self.pantalla = pantalla  # Pantalla principal del juego
        self.font = font  # Fuente para textos
        self.nombre_usuario = ""  # Texto que el usuario escribe como nombre
        self.nickname = ""  # Nickname de 3 letras
        self.input_activo = "usuario"  # Controla qué campo está activo ("usuario" o "nickname")
        self.finalizado = False  # Si ya se completaron los datos
        self.cuadro_input = pygame.Surface((500, 300))  # Cuadro donde se muestran los inputs
        self.cuadro_input.fill(GRIS_OSCURO)  # Color de fondo del cuadro
        pygame.draw.rect(self.cuadro_input, BORDO, self.cuadro_input.get_rect(), 4, border_radius=12)  # Borde decorativo
        self.mensaje_error = ""  # Mensaje de error si hay problemas con el input

    #  Muestra la pantalla para ingresar nombre y nickname
    def mostrar_pantalla_inicio(self):
        self.pantalla.fill(NEGRO)  # Fondo negro

        # Título del juego
        titulo = self.font.render("SPACE INVADERS", True, AMARILLO)
        self.pantalla.blit(titulo, (220, 80))

        # Instrucciones para el usuario
        instrucciones = self.font.render("Ingrese su nombre y nickname (3 letras)", True, BLANCO)
        self.pantalla.blit(instrucciones, (90, 140))

        # Muestra el cuadro para escribir
        self.pantalla.blit(self.cuadro_input, (125, 200))

        # Muestra el texto del nombre y el nickname, el activo se ve en amarillo
        texto_usuario = self.font.render(f"Usuario: {self.nombre_usuario}", True, AMARILLO if self.input_activo == "usuario" else BLANCO)
        texto_nick = self.font.render(f"Nickname: {self.nickname}", True, AMARILLO if self.input_activo == "nickname" else BLANCO)

        self.pantalla.blit(texto_usuario, (150, 250))
        self.pantalla.blit(texto_nick, (150, 300))

        # Si los datos fueron completados correctamente, se indica cómo continuar
        if self.finalizado:
            continuar = self.font.render("ENTER para continuar", True, BLANCO)
            self.pantalla.blit(continuar, (180, 360))

        # Si hay un error, se muestra en pantalla
        if self.mensaje_error:
            error_texto = self.font.render(self.mensaje_error, True, ROJO)
            self.pantalla.blit(error_texto, (150, 420))

        pygame.display.update()  # Se actualiza la pantalla

    # 🎮 Maneja los eventos de teclado en la pantalla de inicio
    def manejar_evento_inicio(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                # Si se presiona ENTER, cambia entre campos o finaliza
                if self.input_activo == "usuario":
                    # Valida que el nombre no esté vacío
                    if self.nombre_usuario.strip() != "":
                        self.mensaje_error = ""
                        self.input_activo = "nickname"  # Pasa al campo de nickname
                    else:
                        self.mensaje_error = "El nombre no puede estar vacío"
                elif self.input_activo == "nickname":
                    # Valida que el nickname tenga 3 letras
                    if len(self.nickname) == 3:
                        self.mensaje_error = ""
                        self.finalizado = True  # Datos listos
                        return True  # Indica que se puede avanzar
                    else:
                        self.mensaje_error = "El nickname debe tener 3 letras"

            elif evento.key == pygame.K_BACKSPACE:
                # Borra el último carácter ingresado
                if self.input_activo == "usuario":
                    self.nombre_usuario = self.nombre_usuario[:-1]
                else:
                    self.nickname = self.nickname[:-1]

            # Captura los caracteres alfanuméricos
            else:
                char = evento.unicode.upper()  # Se convierte a mayúscula
                if self.input_activo == "usuario" and len(self.nombre_usuario) < 12 and char.isalnum():
                    self.nombre_usuario += char  # Agrega al nombre
                elif self.input_activo == "nickname" and len(self.nickname) < 3 and char.isalpha():
                    self.nickname += char  # Agrega al nickname (solo letras)

        return False  # Aún no se han completado los datos

    #  Devuelve los datos del usuario ingresado
    def obtener_datos(self):
        return self.nombre_usuario, self.nickname

#  Clase que muestra el menú principal del juego
class MenuPrincipal:
    def __init__(self, pantalla, font):
        self.pantalla = pantalla  # Pantalla principal
        self.font = font  # Fuente de texto
        self.opciones = ["Modo Niveles", "Modo Infinito", "Ver Historial", "Top 5 Infinito"]  # Opciones del menú
        self.opcion_actual = 0  # Índice de la opción seleccionada
        self.marco_menu = pygame.Surface((500, 350))  # Marco decorativo
        self.marco_menu.fill(GRIS_OSCURO)
        pygame.draw.rect(self.marco_menu, BORDO, self.marco_menu.get_rect(), 4, border_radius=12)

    # Dibuja el menú principal
    def mostrar_menu(self):
        self.pantalla.fill(NEGRO)  # Fondo negro

        # Título del menú
        titulo = self.font.render("MENU PRINCIPAL", True, AMARILLO)
        self.pantalla.blit(titulo, (275, 100))

        # Dibuja el recuadro del menú
        self.pantalla.blit(self.marco_menu, (125, 180))

        # Dibuja cada opción del menú
        for i, opcion in enumerate(self.opciones):
            color = AMARILLO if i == self.opcion_actual else BLANCO  # La opción actual se resalta
            texto = self.font.render(opcion, True, color)
            self.pantalla.blit(texto, (170, 200 + i * 60))  # Posición vertical según índice

        pygame.display.update()  # Se actualiza la pantalla

    #  Maneja los eventos del teclado dentro del menú
    def manejar_evento_menu(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                # Mueve la selección hacia arriba (cíclico)
                self.opcion_actual = (self.opcion_actual - 1) % len(self.opciones)
            elif evento.key == pygame.K_s:
                # Mueve la selección hacia abajo (cíclico)
                self.opcion_actual = (self.opcion_actual + 1) % len(self.opciones)
            elif evento.key == pygame.K_RETURN:
                # Se selecciona la opción actual
                return self.opcion_actual

        return None  # No se eligió aún
