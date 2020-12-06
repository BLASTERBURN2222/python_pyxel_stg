from random import random

import requests
from bs4 import BeautifulSoup

import pyxel
import json
import math

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

ENERGY_INIT = 1

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2

BG_WIDTH = 64
BG_HEIGHT = 16
BG_SPEED = 4

BG_COUNT = 11

BAR_WIDTH = 80
BAR_HEIGHT = 8


ENEBALL_WIDTH = 8
ENEBALL_HEIGHT = 8

BULLET_WIDTH = 8
BULLET_HEIGHT = 8
BULLET_SPEED = 6


bar_list = []
baku_list = []
bullet_list = []
eneball_list = []
muteki = 0
player_x = 0.0
player_y = 0.0
game_distance = 0

def update_list(list):
	for elem in list:
		elem.update()


def draw_list(list):
	for elem in list:
		elem.draw()


def cleanup_list(list):
	i = 0
	while i < len(list):
		elem = list[i]
		if not elem.alive:
			list.pop(i)
		else:
			i += 1

class Bullet:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = BULLET_WIDTH
		self.h = BULLET_HEIGHT
		self.alive = True

		bullet_list.append(self)

	def update(self):
		self.y -= BULLET_SPEED

		if self.y + self.h - 1 < 0:
			self.alive = False

	def draw(self):
		pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 0)

class Baku:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vy = -1
		self.anime = 0
		self.anime_cnt = 0
		self.alive = True

		baku_list.append(self)

	def update(self):
		self.y += self.vy
		self.anime_cnt += 1
		if self.anime_cnt > 2:
			self.anime_cnt = 0
			self.anime += 1

		if self.anime >= 4:
			self.alive = False

	def draw(self):
		plus = self.anime;
		pyxel.blt(self.x, self.y, 0, 40+(8*plus), 8, 8, 8, 0)


class EneBall:
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.w = ENEBALL_WIDTH
		self.h = ENEBALL_HEIGHT
		self.vx = vx
		self.vy = vy
		self.alive = True

		eneball_list.append(self)

	def update(self):
		self.x += self.vx
		self.y += self.vy
		if self.y >= pyxel.height:
			self.alive = False


	def draw(self):
		pyxel.blt(self.x, self.y, 0, 8, 8, ENEBALL_WIDTH, ENEBALL_HEIGHT, 0)




class Bar:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = BAR_WIDTH
		self.h = BAR_HEIGHT
		self.alive = True

		bar_list.append(self)

	def update(self):
		self.y += BG_SPEED
		if self.y >= pyxel.height:
			self.alive = False


	def draw(self):
		pyxel.blt(self.x, self.y, 0, 24, 0, BAR_WIDTH, BAR_HEIGHT, 0)







class Background:
	def __init__(self):
		self.star_list = []
		for i in range(BG_COUNT):
			self.star_list.append(
				(0, BG_HEIGHT*i)
			)

	def update(self):
		for i, (x, y) in enumerate(self.star_list):
			y += BG_SPEED
			if y >= pyxel.height:
				y -= (pyxel.height+BG_HEIGHT)
			self.star_list[i] = (x, y)

	def draw(self):
		for (x, y) in self.star_list:
			pyxel.blt(x, y, 0, 0, 16, 128,16, 0)


class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = PLAYER_WIDTH
		self.h = PLAYER_HEIGHT
		self.alive = True
		self.shot_cnt = 0

	def update(self):
		global player_x
		global player_y
		if pyxel.btn(pyxel.KEY_LEFT):
			self.x -= PLAYER_SPEED

		if pyxel.btn(pyxel.KEY_RIGHT):
			self.x += PLAYER_SPEED

		if pyxel.btn(pyxel.KEY_UP):
			self.y -= PLAYER_SPEED

		if pyxel.btn(pyxel.KEY_DOWN):
			self.y += PLAYER_SPEED


		self.x = max(self.x, 0)
		self.x = min(self.x, pyxel.width - self.w)

		self.y = max(self.y, 0)
		self.y = min(self.y, pyxel.height - self.h)


		if pyxel.btnp(pyxel.KEY_SPACE):
			self.shot_cnt = 1
		else:
			if pyxel.btn(pyxel.KEY_SPACE):
				self.shot_cnt += 1
				self.shot_cnt = self.shot_cnt & 7
			else:
				self.shot_cnt = 0

		if self.shot_cnt == 1:
			Bullet(
				self.x , self.y
			)

		player_x = self.x
		player_y = self.y


	def draw(self):
		global muteki
		if muteki <= 0:
			pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h, 0)
		else:
			if pyxel.frame_count % 3 < 2:
				pyxel.blt(self.x, self.y, 0, 72,8, self.w, self.h, 0)



# リソース akgres.pyxres



class App:
	def __init__(self):
		load_url = "http://www5f.biglobe.ne.jp/~akagiken/index.html"
		html = requests.get(load_url)
		soup = BeautifulSoup(html.content,"html.parser")
		
		self.str_title = soup.find("title").text

#keyをセットして、514行を有効にするとタイトル画面で東京の気温が表示されます
#		url = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric"
#		url = url.format(city="Tokyo,Jp",key=" ")
#		jsondata = requests.get(url).json()
#		self.str_kion = str(jsondata["main"]["temp"]) #気温


		self.anime = 0
		pyxel.init(128, 160, caption=self.str_title)
		pyxel.load("assets/akgres.pyxres")
		self.x = 0
		

		self.scene = SCENE_TITLE
		muteki = 0

		self.score = 0
		self.hiscore = 0
		self.keywait = 10
		self.energy = ENERGY_INIT
		self.background = Background()
		self.player = Player(pyxel.width / 2, pyxel.height - 20)
		self.push_cnt = 0


		pyxel.run(self.update, self.draw)

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		self.background.update()
		if self.scene == SCENE_TITLE:
			self.update_title_scene()
		elif self.scene == SCENE_PLAY:
			self.update_play_scene()
		elif self.scene == SCENE_GAMEOVER:
			self.update_gameover_scene()


	def update_title_scene(self):
		global muteki
		global game_distance
		
		if self.keywait > 0:
			self.keywait -= 1
		else:
			self.push_cnt = self.push_cnt + 1
			self.push_cnt = self.push_cnt & 31
			if pyxel.btnp(pyxel.KEY_SPACE):
				self.energy = ENERGY_INIT
				self.scene = SCENE_PLAY
				game_distance = 0
				muteki = 0


	def update_play_scene(self):
		global muteki
		global player_x
		global player_y
		global game_distance

		game_distance += 1
		bar_cnt = 120
		ball_cnt = 20
		if game_distance < 500:
			bar_cnt = 120
			ball_cnt = 20
		elif game_distance < 1000:
			bar_cnt = 100
			ball_cnt = 15
		elif game_distance < 1500:
			bar_cnt = 60
			ball_cnt = 10
		elif game_distance < 2000:
			bar_cnt = 90
			ball_cnt = 5
		else:
			bar_cnt = 50
			ball_cnt = 3

		if pyxel.frame_count % bar_cnt == 0:
			Bar(random() * (pyxel.width), 0-BAR_HEIGHT)

		if pyxel.frame_count % ball_cnt == 0:
			start_x = random() * (pyxel.width)
			start_y = -20.0
			dx = player_x - start_x
			dy = player_y - start_y;
			kakudo = math.atan2(dy, dx)
			sin_d = math.sin(kakudo)
			cos_d = math.cos(kakudo)

			sin_d *= 4.0
			cos_d *= 4.0

			EneBall(start_x, start_y ,cos_d,sin_d)




		if muteki > 0:
			muteki -= 1


		for ene in bar_list:
			for shot in bullet_list:
				if (
					ene.x + ene.w > shot.x
					and shot.x + shot.w > ene.x
					and ene.y + ene.h > shot.y
					and shot.y + shot.h > ene.y
				):
					shot.alive = False

					baku_list.append(
						Baku(shot.x + (shot.w/2), shot.y + (shot.h/2))
					)

					self.score += 10


		for ene in eneball_list:
			for shot in bullet_list:
				if (
					ene.x + ene.w > shot.x
					and shot.x + shot.w > ene.x
					and ene.y + ene.h > shot.y
					and shot.y + shot.h > ene.y
				):
					ene.alive = False
					shot.alive = False

					baku_list.append(
						Baku(shot.x + (shot.w/2), shot.y + (shot.h/2))
					)
					baku_list.append(
						Baku(ene.x + (ene.w/2), ene.y + (ene.h/2))
					)

					self.score += 100



		if muteki <= 0:

			for ene in bar_list:
				if (
					self.player.x + self.player.w > ene.x
					and ene.x + ene.w > self.player.x
					and self.player.y + self.player.h > ene.y
					and ene.y + ene.h > self.player.y
				):

					baku_list.append(
						Baku(self.player.x + PLAYER_WIDTH / 2, self.player.y + PLAYER_HEIGHT / 2)
					)
					if self.score > self.hiscore:
						self.hiscore = self.score
					self.keywait = 30
					self.push_cnt = 0
					self.scene = SCENE_GAMEOVER
					


			for ene in eneball_list:
				if (
					self.player.x + self.player.w > ene.x
					and ene.x + ene.w > self.player.x
					and self.player.y + self.player.h > ene.y
					and ene.y + ene.h > self.player.y
				):

					baku_list.append(
						Baku(ene.x + ene.w / 2, ene.y + ene.h / 2)
					)

					ene.alive = False

					baku_list.append(
						Baku(self.player.x + PLAYER_WIDTH / 2, self.player.y + PLAYER_HEIGHT / 2)
					)

					self.energy -= 1
					if self.energy <= 0:
						if self.score > self.hiscore:
							self.hiscore = self.score
						self.keywait = 30
						self.push_cnt = 0
						self.scene = SCENE_GAMEOVER
					else:
						muteki = 60




		update_list(bar_list)
		update_list(eneball_list)
		update_list(bullet_list)
		update_list(baku_list)

		cleanup_list(bar_list)
		cleanup_list(eneball_list)
		cleanup_list(bullet_list)
		cleanup_list(baku_list)


		self.player.update()

	def update_gameover_scene(self):
		update_list(bullet_list)
		update_list(bar_list)
		update_list(eneball_list)
		update_list(baku_list)

		cleanup_list(bar_list)
		cleanup_list(eneball_list)
		cleanup_list(bullet_list)
		cleanup_list(baku_list)

		if self.keywait > 0:
			self.keywait -= 1
		else:
			self.push_cnt = self.push_cnt + 1
			self.push_cnt = self.push_cnt & 31


			if pyxel.btnp(pyxel.KEY_SPACE):
				self.keywait = 20
				self.scene = SCENE_TITLE
				self.player.x = pyxel.width / 2
				self.player.y = pyxel.height - 20
				self.score = 0

				bar_list.clear()
				eneball_list.clear()
				bullet_list.clear()
				baku_list.clear()



	def draw(self):
		pyxel.cls(0)
		
		self.background.draw()

		if self.scene == SCENE_TITLE:
			self.draw_title_scene()
		elif self.scene == SCENE_PLAY:
			self.draw_play_scene()
		elif self.scene == SCENE_GAMEOVER:
			self.draw_gameover_scene()

	def draw_title_scene(self):
		pyxel.text(39, 4, "HI-SCORE {:5}".format(self.hiscore), 7)
		pyxel.text(35, 50, self.str_title , pyxel.frame_count % 16)

		if self.keywait == 0:
			if self.push_cnt < 16:
				pyxel.text(25, 90, "- PRESS SPACE BAR -", 1)

#		pyxel.text(10, 80, self.str_kion, 13)

		pyxel.text(20, 130, "RAINBOW SHOOTING MMXX", pyxel.frame_count % 16)


	def draw_play_scene(self):
		global game_distance

		draw_list(bar_list)
		draw_list(eneball_list)
		draw_list(bullet_list)
		draw_list(baku_list)

		self.player.draw()
		pyxel.text(39, 4, "HI-SCORE {:5}".format(self.hiscore), 7)
		if self.score > self.hiscore:
			pyxel.text(39, 14, "SCORE {:5}".format(self.score), pyxel.frame_count % 16)
		else:
			pyxel.text(39, 14, "SCORE {:5}".format(self.score), 7)

		pyxel.text(5, 150, "DISTANCE {:6}".format(game_distance), 13)

	def draw_gameover_scene(self):
		global game_distance

		draw_list(bullet_list)
		draw_list(bar_list)
		draw_list(eneball_list)
		draw_list(baku_list)

		pyxel.text(39, 4, "HI-SCORE {:5}".format(self.hiscore), 7)
		pyxel.text(39, 14, "SCORE {:5}".format(self.score), 7)

		pyxel.text(43, 66, "GAME OVER", 8)
		if self.keywait == 0:
			if self.push_cnt < 16:
				pyxel.text(25, 110, "- PRESS SPACE BAR -", 1)

		pyxel.text(5, 150, "DISTANCE {:6}".format(game_distance), 13)


App()
