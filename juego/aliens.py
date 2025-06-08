import pygame
import random  # se importa para hacewr que escoja coordebada aleatoria

#hay tres tipos de alien pero se usara la misma clase y despues se cambiara
#la imagen de cada uno
class Alien(pygame.sprite.Sprite):
	def __init__(self, type, x, y):
		super().__init__()
		self.type = type
		path = f"graficos/alien_{type}.png"     #es un marcador de posiciones para llamar despues a type
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(topleft = (x, y))

    # la funcion se encarga de actualizar la posicion de los aliens	
	def update(self, direccion):
		self.rect.x += direccion


class Nave_misteriosa(pygame.sprite.Sprite):
	def __init__(self, ancho_pantalla, offset):
		super().__init__()
		self.image = pygame.image.load('graficos/mystery.png')
		self.ancho_pantalla  = ancho_pantalla
		self.offset = offset

		x = random.choice([self.offset / 2, self.ancho_pantalla + self.offset - self.image.get_width()]) # esto hace que la nave aparesca de manera aletoria entre el borde derecho y izq

		# si aparace en el borde  izqhira en velocidad positiva 
		if x == self.offset / 2:
			self.velocidad = 3
		# si aparece en el borde derecho hira en velocidad negativa 
		else:
			self.velocidad = -3

		'''
		la nave misteriosa puede parecer tanto por la izq que por la derecha asi que
		la cordenada x sera una variable
		'''
		self.rect = self.image.get_rect(topleft = (x, 90))   #la cordenada x es variable

	
	'''
	la funcion hara que la nave se mueva y para eso se necesita
	mover su posicion x en cada cuadro
	'''
	def update(self):
		self.rect.x += self.velocidad
		#validaciones para cuando la nave se salga de la pantalla
		if self.rect.right > self.ancho_pantalla + self.offset / 2:
			self.kill()
		elif self.rect.left < self.offset / 2:
			self.kill()