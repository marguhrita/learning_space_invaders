import pygame
from pygame import mixer
from pygame.locals import *
import random

#region Task 7
#<===============================TASK 7==========================================>
#<===============================CODE STARTS HERE==========================================>
def validate_input():
	modes = ["easy", "medium", "hard"]
	# Show the user the possible modes, and ask them which one they would like to choose
	print("Please enter a difficulty:")
	for counter in range(0,len(modes)):
		print(modes[counter])
	
	
	#loop until a valid answer is given!
	valid = False
	while not valid:
		answer = input()
		#check if any of the modes are the same as the answer - return true if it is
		for counter in range(0,len(modes)):
			if modes[counter] == answer.lower():
				valid = True
		
		if not valid:
			print(answer + " is not a valid difficulty - please try again")
	
	#return the given answer once a valid one is given
	return answer.lower()

difficulty = validate_input()

#<===============================CODE ENDS HERE==========================================>
#endregion

#region initialisation
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


#define fps
clock = pygame.time.Clock()
fps = 60


screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))

#define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#load sounds
explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)


#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

#load image
bg = pygame.image.load("img/bg.png")

def draw_bg():
	screen.blit(bg, (0, 0))


#define function for creating text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))




#endregion init

#region sprite classes


#create spaceship class
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/spaceship.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()


	def update(self, ship_move, ship_shoot):
		game_over = 0

		key = pygame.key.get_pressed()
		self.rect.x = ship_move(self.rect, key)
		ship_shoot(self.rect, key)

		#update mask
		self.mask = pygame.mask.from_surface(self.image)

		#draw health bar
		pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
		elif self.health_remaining <= 0:
			explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
			explosion_group.add(explosion)
			self.kill()
			game_over = -1
		return game_over



#create Bullets class
class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()
		if pygame.sprite.spritecollide(self, alien_group, True):
			self.kill()
			explosion_fx.play()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
			explosion_group.add(explosion)




#create Aliens class
class Aliens(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.move_counter = 0
		self.move_direction = 1
		self.x = self.rect.centerx
		self.y = self.rect.centery

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		self.x = self.rect.centerx
		self.y = self.rect.centery
		if abs(self.move_counter) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction



#create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/alien_bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y += 2
		if self.rect.top > screen_height:
			self.kill()
		if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
			self.kill()
			explosion2_fx.play()
			#reduce spaceship health
			spaceship.health_remaining -= 1
			explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
			explosion_group.add(explosion)




#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"img/exp{num}.png")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			#add the image to the list
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, delete explosion
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

#create player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

#endregion

#define game variables
alien_cooldown = 1000 #bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()
last_count = pygame.time.get_ticks()
last_shot = pygame.time.get_ticks()
countdown = 3
game_over = 0 #0 is no game over, 1 means player has won, -1 means player has lost

#region Task 8
#<=====================================TASK 1==========================================>
#<==================================START CODE HERE==========================================>
if difficulty == "easy":
	alien_cooldown = 1000 #bullet cooldown in milliseconds
elif difficulty == "medium":
	alien_cooldown = 700 #bullet cooldown in milliseconds
else:
	alien_cooldown = 200 #bullet cooldown in milliseconds

#<==================================END CODE HERE==========================================>
#endregion

#region Task 1
#<=====================================TASK 1==========================================>
#Make them create aliens first in a row, then in columns, then together
def create_aliens():
#<==============================START CODE HERE=============================>
	rows = 5
	cols = 5
	#generate aliens
	for row in range(rows):
		for item in range(cols):
			alien = Aliens(100 + item * 100, 100 + row * 70)
			alien_group.add(alien)

#<==============================END CODE HERE=============================>

create_aliens()
#endregion

#region Task 2
#<==================================TASK 2==========================================>
def spaceship_move(ship, key):
#<==============================START CODE HERE=============================>
	#set movement speed
	speed = 8
	#get key press
	if key[pygame.K_LEFT] and ship.left > 0:
		ship.x -= speed
	if key[pygame.K_RIGHT] and ship.right < screen_width:
		ship.x += speed

	return ship.x

#<==============================END CODE HERE=============================>

#endregion

#region Task 3
#<==================================TASK 3==========================================>
def spaceship_shoot(ship, key):
	#Get time of last shot as a global variable
	global last_shot
#<==============================START CODE HERE=============================>
	#record current time
	time_now = pygame.time.get_ticks()
	#set a cooldown variable
	cooldown = 500 #milliseconds
	#shoot
	if key[pygame.K_SPACE] and time_now - last_shot > cooldown:
		laser_fx.play()
		bullet = Bullets(ship.centerx, ship.top)
		bullet_group.add(bullet)
		last_shot = time_now
#<==============================END CODE HERE=============================>
#endregion

#region Helper Functions
#Helper function to update sprites
def update_sprites():
	#update spaceship
	game_over = spaceship.update(spaceship_move, spaceship_shoot)
	#update sprite groups
	bullet_group.update()
	alien_group.update()
	alien_bullet_group.update()
	return game_over

def shoot_alien_bullet(x,y):
	global last_alien_shot
	alien_bullet = Alien_Bullets(x, y)
	alien_bullet_group.add(alien_bullet)
	last_alien_shot = time_now
#endregion

#region main game loop
pygame.display.set_caption('Space Invaders')
run = True
while run:
	clock.tick(fps)
	#draw background
	draw_bg()

	#region Task 4
	#<==================================TASK 4==========================================>
	#<==============================START CODE HERE=====================================>
	if countdown == 0:
		#create random alien bullets
		#record current time
		time_now = pygame.time.get_ticks()
		#shoot
		if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 40 and len(alien_group) > 0:
			attacking_alien = random.choice(alien_group.sprites())
			shoot_alien_bullet(attacking_alien.x, attacking_alien.y)
	
	#<==============================END CODE HERE=====================================>
	
	#endregion

	#region Task 5
	#Set game over to -1 if the spaceship is out of health!
	if spaceship.health_remaining <= 0:
		game_over = -1

	#<==================================TASK 5========================================>
	#<==============================START CODE HERE===================================>
	if len(alien_group) == 0:
		game_over = 1

	#<==============================END CODE HERE=====================================>

	#endregion

	#region Task 6
	#<==================================TASK 6========================================>
	#<==============================START CODE HERE===================================>
	if game_over == 0:
		update_sprites()
	else:
		if game_over == -1:
			draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
		if game_over == 1:
			draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

	#<==============================END CODE HERE=====================================>

	#endregion

	#region Pygame
	if countdown > 0:
		draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
		draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
		count_timer = pygame.time.get_ticks()
		if count_timer - last_count > 1000:
			countdown -= 1
			last_count = count_timer


	#update explosion group	
	explosion_group.update()

	#draw sprite groups
	spaceship_group.draw(screen)
	bullet_group.draw(screen)
	alien_group.draw(screen)
	alien_bullet_group.draw(screen)
	explosion_group.draw(screen)


	#event handlers
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	pygame.display.update()
	#endregion

pygame.quit()
	

#endregion