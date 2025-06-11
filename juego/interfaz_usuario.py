## interfaz.py - Manejo de pantallas para login y menú principal
import pygame
from usuario import obtener_o_crear_usuario

AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_OSCURO = (30, 30, 30)
BORDO = (128, 0, 64)
ROJO = (255, 0, 0)

class InterfazUsuario:
    def __init__(self, pantalla, font):
        self.pantalla = pantalla
        self.font = font
        self.nombre_usuario = ""
        self.nickname = ""
        self.input_activo = "usuario"  # Puede ser "usuario" o "nickname"
        self.finalizado = False
        self.cuadro_input = pygame.Surface((500, 300))
        self.cuadro_input.fill(GRIS_OSCURO)
        pygame.draw.rect(self.cuadro_input, BORDO, self.cuadro_input.get_rect(), 4, border_radius=12)
        self.mensaje_error = ""


    def mostrar_pantalla_inicio(self):
        self.pantalla.fill(NEGRO)

        titulo = self.font.render("SPACE INVADERS", True, AMARILLO)
        self.pantalla.blit(titulo, (220, 80))

        instrucciones = self.font.render("Ingrese su nombre y nickname (3 letras)", True, BLANCO)
        self.pantalla.blit(instrucciones, (90, 140))

        self.pantalla.blit(self.cuadro_input, (125, 200))

        texto_usuario = self.font.render(f"Usuario: {self.nombre_usuario}", True, AMARILLO if self.input_activo == "usuario" else BLANCO)
        texto_nick = self.font.render(f"Nickname: {self.nickname}", True, AMARILLO if self.input_activo == "nickname" else BLANCO)

        self.pantalla.blit(texto_usuario, (150, 250))
        self.pantalla.blit(texto_nick, (150, 300))

        if self.finalizado:
            continuar = self.font.render("ENTER para continuar", True, BLANCO)
            self.pantalla.blit(continuar, (180, 360))

        if self.mensaje_error:
            error_texto = self.font.render(self.mensaje_error, True, ROJO)
            self.pantalla.blit(error_texto, (150, 420))

        pygame.display.update()

    def manejar_evento_inicio(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if self.input_activo == "usuario":
                    if self.nombre_usuario.strip() != "":
                        self.mensaje_error = ""
                        self.input_activo = "nickname"
                    else:
                        self.mensaje_error = "El nombre no puede estar vacío"
                elif self.input_activo == "nickname":
                    if len(self.nickname) == 3:
                        self.mensaje_error = ""
                        self.finalizado = True
                        return True
                    else:
                        self.mensaje_error = "El nickname debe tener 3 letras"



            elif evento.key == pygame.K_BACKSPACE:
                if self.input_activo == "usuario":
                    self.nombre_usuario = self.nombre_usuario[:-1]
                else:
                    self.nickname = self.nickname[:-1]

            elif evento.key == pygame.K_RETURN:
                if self.nombre_usuario.strip() != "" and len(self.nickname) == 3:
                    self.finalizado = True
                    return True

            else:
                char = evento.unicode.upper()
                if self.input_activo == "usuario" and len(self.nombre_usuario) < 12 and char.isalnum():
                    self.nombre_usuario += char
                elif self.input_activo == "nickname" and len(self.nickname) < 3 and char.isalpha():
                    self.nickname += char

        return False

    def obtener_datos(self):
        return self.nombre_usuario, self.nickname

class MenuPrincipal:
    def __init__(self, pantalla, font):
        self.pantalla = pantalla
        self.font = font
        self.opciones = ["Modo Niveles", "Modo Infinito", "Ver Historial", "Top 5 Infinito"]
        self.opcion_actual = 0
        self.marco_menu = pygame.Surface((500, 350))
        self.marco_menu.fill(GRIS_OSCURO)
        pygame.draw.rect(self.marco_menu, BORDO, self.marco_menu.get_rect(), 4, border_radius=12)

    def mostrar_menu(self):
        self.pantalla.fill(NEGRO)
        titulo = self.font.render("MENU PRINCIPAL", True, AMARILLO)
        self.pantalla.blit(titulo, (275, 100))

        self.pantalla.blit(self.marco_menu, (125, 180))

        for i, opcion in enumerate(self.opciones):
            color = AMARILLO if i == self.opcion_actual else BLANCO
            texto = self.font.render(opcion, True, color)
            self.pantalla.blit(texto, (170, 200 + i * 60))

        pygame.display.update()

    def manejar_evento_menu(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                self.opcion_actual = (self.opcion_actual - 1) % len(self.opciones)
            elif evento.key == pygame.K_s:
                self.opcion_actual = (self.opcion_actual + 1) % len(self.opciones)
            elif evento.key == pygame.K_RETURN:
                return self.opcion_actual
        return None
