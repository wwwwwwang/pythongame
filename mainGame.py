# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random
import time

pause = False
clock = pygame.time.Clock()

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ShootGameByWhsh')
# 载入游戏音乐
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
#pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.load('resources/sound/gm1.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


# 载入背景图
#background = pygame.image.load('resources/image/background.png').convert()
#game_over = pygame.image.load('resources/image/gameover.png')
#background = pygame.image.load('resources/image/bg.png').convert()
game_over = pygame.image.load('resources/image/go.jpg')
background1 = pygame.image.load('resources/image/bg1.png').convert()
background2 = pygame.image.load('resources/image/bg2.png').convert()
background3 = pygame.image.load('resources/image/bg3.png').convert()
background4 = pygame.image.load('resources/image/bg.png').convert()


filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename).convert_alpha()


# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

	
def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def quitgame():
	#pygame.quit()
	quit()
	
def unpause():
	global pause
	pause = False
	
def button (msg, x, y, w, h, ic, ac, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(screen, ac, (x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(screen, ic, (x,y,w,h))
	smallText = pygame.font.Font(None, 20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)))
	screen.blit(textSurf, textRect)
	
def game_intro():
	global pasue
	pause = False
	intro = True
	time.sleep(.2)
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		screen.fill(white)
		largeText = pygame.font.Font(None, 100)
		TextSurf, TextRect = text_objects('A shoot game!', largeText)
		TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
		screen.blit(TextSurf, TextRect)
		button("Start", 150, 450, 100, 50, green, bright_green, run)
		button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
		pygame.display.update()
		clock.tick(15)
		
def paused():
	largeText = pygame.font.Font(None, 100)
	TextSurf, TextRect = text_objects('Paused', largeText)
	TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
	screen.blit(TextSurf, TextRect)
 
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					exit()  
				elif event.key == K_p:
					unpause()
##		gameDisplay.fill(white)
		button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
		button("Return", 550, 450, 100, 50, red, bright_red, game_intro)
		pygame.display.update()
		clock.tick(15)

def gameover(score):
	font = pygame.font.Font(None, 48)
	text = font.render('Score: '+ str(score), True, (255, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 200
	screen.blit(game_over, (0, 0))
	screen.blit(text, text_rect)
	#largeText = pygame.font.SysFont('comicsansms',115)
	TextSurf, TextRect = text_objects('Oh, over!', font)
	TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
	screen.blit(TextSurf, TextRect)
	
	over = True
	while over:
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
##		gameDisplay.fill(white)
		button("Play Again", 150, 450, 100, 50, green, bright_green, run)
		button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
		pygame.display.update()
		clock.tick(15)
		
def run():
	global pause
	shoot_frequency = 0
	enemy_frequency = 0
	player_down_index = 16
	score = 0
	running = True
	fire = False
	enemy_speed = 2
	bg_speed = 12
	level = 0
	for_level_up = 150
	bgposition1 = 0
	bgposition2 = 600
	bgposition3 = 1200
	bgposition4 = 1800
	
	# 设置玩家相关参数
	player_rect = []
	player_rect.append(pygame.Rect(0, 99, 102, 126))		# 玩家精灵图片区域
	player_rect.append(pygame.Rect(165, 360, 102, 126))
	player_rect.append(pygame.Rect(165, 234, 102, 126))	 # 玩家爆炸精灵图片区域
	player_rect.append(pygame.Rect(330, 624, 102, 126))
	player_rect.append(pygame.Rect(330, 498, 102, 126))
	player_rect.append(pygame.Rect(432, 624, 102, 126))
	
	player_pos = [350, 470]
	player = Player(plane_img, player_rect, player_pos)
	
	enemies1 = pygame.sprite.Group()
	# 存储被击毁的飞机，用来渲染击毁精灵动画
	enemies_down = pygame.sprite.Group()

	while running:
		# 控制游戏最大帧率为60
		time_passed = clock.tick(60)
		time_passed_seconds = time_passed / 1000.
	
		# 控制发射子弹频率,并发射子弹
		if not player.is_hit:
			if shoot_frequency == 0 and fire == True:
				bullet_sound.play()
				player.shoot(bullet_img)
			shoot_frequency += 1
			if shoot_frequency >= 12:
				shoot_frequency = 0
	
		# 生成敌机
		#print("enemy_speed = ",enemy_speed+level)
		if enemy_frequency % 50 == 0:
			enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
			enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy_speed+level*.5, enemy1_pos)
			enemies1.add(enemy1)
		enemy_frequency += 1*(not pause)
		if enemy_frequency >= 100:
			enemy_frequency = 0
		if score//for_level_up > level:
			level = score//for_level_up
			for_level_up += level*50
	
		# 移动子弹，若超出窗口范围则删除
		for bullet in player.bullets:
			bullet.move(not pause)
			if bullet.rect.bottom < 0:
				player.bullets.remove(bullet)
	
		# 移动敌机，若超出窗口范围则删除
		for enemy in enemies1:
			enemy.move(not pause)
			# 判断玩家是否被击中
			if pygame.sprite.collide_circle(enemy, player):
				enemies_down.add(enemy)
				enemies1.remove(enemy)
				player.is_hit = True
				game_over_sound.play()
				break
			if enemy.rect.top > SCREEN_HEIGHT:
				enemies1.remove(enemy)
	
		# 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
		enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
		for enemy_down in enemies1_down:
			enemies_down.add(enemy_down)
	
		# 绘制背景
		screen.fill(0)
		#screen.blit(background, (0, 0))
		bgposition1 -= bg_speed*time_passed_seconds
		if bgposition1 <= -600:
			bgposition1 = 1800
		bgposition2 -= bg_speed*time_passed_seconds
		if bgposition2 <= -600:
			bgposition2 = 1800
		bgposition3 -= bg_speed*time_passed_seconds
		if bgposition3 <= -600:
			bgposition3 = 1800
		bgposition4 -= bg_speed*time_passed_seconds
		if bgposition4 <= -600:
			bgposition4 = 1800
		screen.blit(background1, (0, bgposition1))
		screen.blit(background2, (0, bgposition2))
		screen.blit(background3, (0, bgposition3))
		screen.blit(background4, (0, bgposition4))
	
		# 绘制玩家飞机
		if not player.is_hit:
			screen.blit(player.image[player.img_index], player.rect)
			# 更换图片索引使飞机有动画效果
			player.img_index = shoot_frequency // 8
		else:
			player.img_index = player_down_index // 8
			screen.blit(player.image[player.img_index], player.rect)
			player_down_index += 1
			if player_down_index > 47:
				running = False
	
		# 绘制击毁动画
		for enemy_down in enemies_down:
			if enemy_down.down_index == 0:
				enemy1_down_sound.play()
			if enemy_down.down_index > 7:
				enemies_down.remove(enemy_down)
				score += 10
				continue
			screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
			enemy_down.down_index += 1
	
		# 绘制子弹和敌机
		player.bullets.draw(screen)
		enemies1.draw(screen)
	
		# 绘制得分
		score_font = pygame.font.Font(None, 36)
		score_text = score_font.render("Score : "+str(score), True, (200, 150, 100))
		level_text = score_font.render("Level : "+str(level), True, (200, 150, 100))
		text_rect = score_text.get_rect()
		level_rect = level_text.get_rect()
		text_rect.topleft = [10, 10]
		level_rect.topleft = [10, 10+text_rect.height]
		screen.blit(score_text, text_rect)
		screen.blit(level_text, level_rect)
	
		# 更新屏幕
		pygame.display.update()
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					exit()  
				elif event.key == K_SPACE and not player.is_hit:
					fire = True
				elif event.key == K_p:
					fire = False
					pause = True
					paused()
					
			elif event.type == KEYUP:
				if event.key == K_SPACE:
					fire = False
				
			pressed_mouse = pygame.mouse.get_pressed()
			if pressed_mouse[0]:
				fire = True
					
				
		# 监听键盘事件
		key_pressed = pygame.key.get_pressed()
		# 若玩家被击中，则无效
		if not player.is_hit:
			if key_pressed[K_w] or key_pressed[K_UP]:
				player.moveUp(not pause)
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				player.moveDown(not pause)
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				player.moveLeft(not pause)
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				player.moveRight(not pause)
	
	gameover(score)

if __name__ == "__main__":
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					exit()
		pygame.display.update()
		game_intro()
		
		