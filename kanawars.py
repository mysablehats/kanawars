# -*- coding: utf-8 -*-
#! /usr/bin/env python
# it's my hiragana game :-)
# author: Frederico B. Klein
# date: 30th of May 2015
# ver: 0.06


import pygame, sys, logging, os, time, platform
import pygame._view
from pygame.locals import *
import random

logging.basicConfig(level=logging.INFO)
pygame.init()  
pygame.mixer.music.load('An_8_Bit_Story.ogg')
screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption("カナ　W・A・R・S")
clock = pygame.time.Clock()        # create pygame clock object
global KPM
KPM = 20			   # Kanas per minute to generate
FPS = 60                           # desired max. framerate in frames per second.

OS = platform.system()
if OS=='Linux':
	keystr = [[49,50,51,52,53,54,55,56,57,48,45,61],[113,119,101,114,116,121,117,105,111,112,314,91],[97,115,100,102,103,104,106,107,108,231,314,93],[92,122,120,99,118,98,110,109,44,46,59,47]] 
elif OS=='Windows':
	keystr = [[49,50,51,52,53,54,55,56,57,48,45,61],[113,119,101,114,116,121,117,105,111,112,91,93],[97,115,100,102,103,104,106,107,108,59,39,92],[60,122,120,99,118,98,110,109,44,46,47,47]] 
else:
	logging.warning("Your platform " + OS + " is not supported. Keys will likely be wrong")
	logging.warning("Edit code yourself to fix it. It's not that hard.")
	keystr = [[49,50,51,52,53,54,55,56,57,48,45,61],[113,119,101,114,116,121,117,105,111,112,314,91],[97,115,100,102,103,104,106,107,108,231,314,93],[92,122,120,99,118,98,110,109,44,46,59,47]] 
	#logging.basicConfig(level=logging.DEBUG) #uncomment this to see keypresses
	# use debuglevel info so the program will list the codes of the keypresses. you will just need to adjust to create an elif condition for your system and adjust the keystr variable. if this is running inside a webmachine or java platform it might be trickier, but we trust you.

pygame.font.init()
f = pygame.font.Font("Cyberbit.ttf",27)
placarf = pygame.font.Font("fonts-japanese-gothic.ttf",22)
bg_color = (220,220,220) #background color

pygame.display.flip()



#creating the boxes
class Boxes(pygame.sprite.Sprite):
    def __init__(self,kana,level):
	#pygame.sprite.Sprite.__init__(self, self.groups)
	y=kana/12
	x=kana%12
	#print kana,x,y
	#kana contem o ponteiro para a kana
	#vou tentar colocar o offset certo
	if y == 0:
		offset = -12
	elif y == 2:
		offset = 10
	elif y == 3:
		offset = -10
	else:
		offset = 0
	unistr = [u"ぬふあうえおやゆよわほへ", u"たていすかんなにらせ゛゜", u"ちとしはきくまのりれけむ", u"ろつさそひこみもねるめろ"]	
	self.kana=unistr[y][x]
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((30,30))
        self.image.fill((self.randcolors(level)))        
	self.image.blit(f.render(self.kana,True,(0,0,0)),(0,-5))
        self.rect=self.image.get_rect()
        self.rect.center=(40*x+20+100+offset,40*y+20+100)
  	self.x = x 
	self.y = y
	self.timerz = 0
    def update(self, level):
	global DEATH
	DEATH = False
	if self.timerz == 0 and self.alive() == True: 
		self.timerz = time.time()
	elif self.alive == False:
		self.timerz = 0
	# you can change where it is also,,, so why dont you?
	displace = time.time()-self.timerz
	newy = self.rect.center[1]+displace
	if newy> 460:
		DEATH = True
	else:
		self.rect.center=(self.rect.center[0],newy)
	#actual update
	self.image.fill((self.randcolors(level)))        
	self.image.blit(f.render(self.kana,True,(0,0,0)),(0,-5))
	#print self.kana, self.randcolors(level), self.timerz, self.rect.center, DEATH, self.alive()

    def randcolors(self, color): # color vai de 0-9, e eu quero que comece claro, i.e. perto de 255
	colorlist = [(220,245,245),(220,245,220),(220,220,245),(220,245,245),(245,245,220),(235,235,235),(245,220,220),(245,100,100),(245,0,0)]
	r = colorlist[color][0] + random.randint(-2,2) 
	g = colorlist[color][1] + random.randint(-2,2)
	b = colorlist[color][2] + random.randint(-2,2)
	return (r%255, g%255, b%255) 



def listfind(listlist, what):
	return [ (listlist.index(x),x.index(y)) for x in listlist for y in x if y == what]  

def instructscreen(text,width, height):
	offset = width+0
	shadowoffset = 1
	firstline = placarf.render(text, True,(40,0,0))
	light =  placarf.render(text, True,(240,240,240))	
	shadow =  placarf.render(text, True,(200,200,200))
	screen.blit(shadow, (offset+shadowoffset, height+shadowoffset))
	screen.blit(shadow, (offset, height+shadowoffset))
	screen.blit(shadow, (offset+shadowoffset, height))
	screen.blit(light, (offset-shadowoffset, height-shadowoffset))
	screen.blit(firstline, (offset, height))
 
def main():
    global KPM, DEATH
    background=pygame.Surface((502,160))
    background=background.convert()
    background.fill(bg_color)
    wrongs = 0

#place where I am loading images
#splash screen! :D
    try:
	splashscreen = pygame.image.load("background.png")
	screen.blit(splashscreen.convert_alpha(),(0,0))
	pygame.display.flip()
	pygame.time.wait(1000)
    except pygame.error, message:
	print "OH NO! My background file!!!! :("
    try:
#alright, not only splashscreen also awesome bill murray is awesome
	awesome = pygame.image.load("awesomesm.png")
	baby = pygame.image.load("bo.png")
	death = pygame.image.load("death.jpg")
	angel = pygame.image.load("angel.png")
	instruc = pygame.image.load("instruc.png")
    except pygame.error, message:
	print "OH NO! Bill murray!!! :(           and possibly other pictures"
#instructions screen

    screen.blit(instruc,(0,0))	
    pygame.display.flip()
    instructscreen("Press the right key according ",300,60)
    instructscreen("to the kana. A mistake makes 2 ",300,90)
    instructscreen("kana appear instead of one. Do ",300,120)
    instructscreen("not let kanas pile up on the ",300,150)
    instructscreen("screen! After 10 kanas, if you ",300,180)
    instructscreen("make a mistake, you die.",300,210)
    pygame.display.flip()
    pygame.time.wait(4000)
    
#initializing variables
    boxes = []
    alltime = 0
    rights = 0
    avgresptime = 10000.0
    level = 0 #tem tantas coisas associadas a level, que level deve ser um objeto, mas eu teria que pensar
#    for j in xrange(0,48):
#	boxes.append(Boxes(j,level))

    allSprites=  pygame.sprite.Group()
    allSprites.kanalist = []
    allSprites.kanalindex = []
    counter = 0.0

    pygame.time.set_timer(USEREVENT, 100) #hack pra começar o jogo com uma kana na tela. necessário em velocidades baixas
    DEATH = False
    mistake = True #pra começar com 3 kanas

##### isso deveria ser possivel mexer por um menu
    KPM = 20			   # Kanas per minute to generate
    leveluptime = 10 # tempo em segundos para level up


    levelstarttime = time.time()	
    newlevel=True # inicio do jogo, seta a variavel newlevel p true
    countnewlevel= False #eu estou setando muitas variaveis malucas, agora já me perdi todo...
    lastboxditched = []
    pygame.mixer.music.play(-1,0.0)
    while 1:
	screen.blit(instruc,(0,0))	
	screen.blit(background,(88,100))
	milliseconds = clock.tick(FPS)  # milliseconds passed since last frame

        for i in pygame.event.get():
            if i.type==QUIT:
                sys.exit()
	    elif i.type==USEREVENT:
		# new kana appending routine	
		for jjj in xrange(0,1+2*mistake):
			randbox = random.randint(0,46) # randbox = random.randint(0,47) #antigo, vou evitar o segundo ro que é desnecessário e não existe em alguns teclados
			while randbox in allSprites.kanalist:
				randbox = random.randint(0,46) #same as before
			a = Boxes(randbox,level)
			pygame.sprite.Group.add(allSprites, a)
			allSprites.kanalindex.append(randbox)
			allSprites.kanalist.append(a)
			#print randbox, "<-rand, wholelist ->", allSprites.kanalindex, "what kana", a.kana
			pygame.time.set_timer(USEREVENT, 60000/KPM) #this is a hack. o contador é ciclico, mas eu resseto pra o valor correto a cada adição pra poder colocar uma kana na tela bem rápido
		mistake = False
	    elif i.type==USEREVENT+1: #level up!
		# allSprites = pygame.sprite.Group() # erases sprites
		KPM +=10
		pygame.time.set_timer(USEREVENT, int(60000.0/KPM))
		newlevel=True
		level +=1
		levelstarttime = time.time()
		pygame.time.set_timer(USEREVENT+1, 0)
	    elif i.type==USEREVENT+2: #been in level for > 30 secs
		newlevel=False
		countnewlevel=False
		pygame.time.set_timer(USEREVENT+2, 0)


	if newlevel and not countnewlevel:
		pygame.time.set_timer(USEREVENT+2, leveluptime*1000)
		countnewlevel=True	#latch pra não inciar contagem 10000 vezes
	if newlevel:
		screen.blit(baby.convert_alpha(),(10,30))
		stoppan = placarf.render("Leveling-up will be enabled in", True,(120,0,0))
		cantnewlevel = placarf.render("{:10.1f}".format(leveluptime-time.time()+levelstarttime)+ " seconds.", True,(120,0,0))
		screen.blit(stoppan, (300, 300))
		screen.blit(cantnewlevel, (300, 320))
	
	# if you can have less than 2 kana show cool message and if lasts 10 seconds, increments KPM
	if len(allSprites.sprites())<3 and not newlevel and not mistake:
        	if not latchtimerdown:
			pygame.time.set_timer(USEREVENT+1, 10000)
			#Seta latch down que começou o timer pra não iniciar a contagem 1000 vezes...
			latchtimerdown = True
			nextleveltime = time.time()
		nextlevel= placarf.render("NEXT LEVEL IN: {:10.3f}".format(10-time.time() + nextleveltime),True,(60,30,30))
		screen.blit(nextlevel,(320,30))
		screen.blit(awesome.convert_alpha(),(500,10))
	else: #tem mais sprites na tela? então reseta timer
		latchtimerdown = False
		pygame.time.set_timer(USEREVENT+1, 0) # e reseta timer
	#imprime placar
	placar=placarf.render(u"MÉDIA: {:10.3f}".format(avgresptime) ,True,(30,30,60))
	kanapmplacar = placarf.render(u"仮名　POR MINUTO: " + str(KPM)  ,True,(30,30,60))
        screen.blit(placar,(10,10))
        screen.blit(kanapmplacar,(320,10))
	if pygame.key.get_focused():
	   press=pygame.key.get_pressed()
	   for i in xrange(0,len(press)):
	    if press[i]==1:
	     logging.debug(i)
	     zz = listfind(keystr,i) 	     # cria uma lista com os endereços dos locais onde achou o i dentro de keystr
	     if len(zz)==0:		#não achou nenhuma ocorrência
		if 'lasterror' in locals(): # checa se variável já existe para evitar logar coisas repetidas
			if not lasterror == i:
				logging.info("To key num. " + str(i) + " no kana box is assigned.")
		else:
			logging.info("To key num. " + str(i) + " no kana box is assigned.")
		lasterror=i
	     else:
		for kkk in xrange(0,len(zz)):		#se em o press gerar um zz com mais de uma remoção, faz um for pra remover tudo.
			z = zz[kkk]
		     	boxtoditch = z[0]*12+z[1]
			logging.debug("z: " + str(z) + "  keynumber from pygame.key.get_pressed():" + str(i) + "  order on boxes list: " + str(boxtoditch))
			# zera timer, integra tempo, calcula média de tempo de reação
			#as vezes os timers enlouquecem. não sei porque
			# insisti no meu erro e simplesmente colocar um latch aqui; na verdade não é bem um latch, vou testar se o sprite existe, no fim dá no mesmo
			#print "i wanto to remove", boxtoditch
			if boxtoditch in allSprites.kanalindex: 
				#print "hey, its on my list, but where?"
				cu = allSprites.kanalindex.index(boxtoditch) # ao usar index, eu pego a primeira ocorrencia da kana. portanto a propriedade kanalindex contem todas as kanas que podem ser removidas.
				#print "tha list is", allSprites.kanalindex, "the index to it is", cu
				alltime += time.time() - allSprites.sprites()[cu].timerz 
				rights += 1
			     	avgresptime = alltime/rights
				logging.debug(str(alltime)+ " "+ str(rights)+ " "+str(avgresptime))
				allSprites.remove(allSprites.kanalist[cu])
				lastboxditched = boxtoditch #latch pra lembrar ultima kana deletada e não penalizar keypresses longos ou repetidos
				mistake = False
				allSprites.kanalist.pop(cu)
				allSprites.kanalindex.pop(cu)
			else: #se chegou aqui ou tem uma tecla apertada por muito tempo, ou tecla errada
				if not lastboxditched == boxtoditch:
					#print lastboxditched, "<-last, to ditch-> ", boxtoditch
					errorfuck = placarf.render(u"3,R-R.0Ř" ,True,(255,0,0))
					screen.blit(errorfuck,(400,50))
					mistake = True
					wrongs += 1
	if len(allSprites.sprites())>10 or DEATH:
		danger = placarf.render("DANGER! NO MORE MISTAKES ALLOWED WITH 10+ KANA! OR REACHING BOTTOM", True,(220,0,0))
		screen.blit(danger,(160,340))
		if mistake: # or DEATH:
			#deathmusic
			#condition here could bring up a nice screen angel
			pygame.mixer.music.stop
			pygame.mixer.music.load('Masterofpuppets.ogg')
			pygame.mixer.music.play(0,0.5)
			pygame.mixer.music.set_endevent()
			#deathscreen
			screen.blit(death,(0,0))
			instructscreen(u"あなたが　死んでいます。At level " + str(level) + ".",5,0)
			instructscreen("Average time {:10.3f}".format(avgresptime),5,30)
			instructscreen("You got " +str(rights) +" kanas right... But " + str(wrongs) + " wrong presses...",5,60)
			instructscreen("...which is not impressive",5,90)
			instructscreen("Practice more to suck less.",5,120)
	  		pygame.display.flip()
			while 1:			
				for i in pygame.event.get():
			            if i.type==QUIT or i.type==NOEVENT:
        	        		sys.exit()
	allSprites.clear(screen,background)
	allSprites.update(level)
	allSprites.draw(screen)
        pygame.display.flip()
		
if __name__=='__main__':
    main()
  
"""You can also check the collision about the rect attributes. There are many ways to do that.Example:
1.circle.rect.colliderect(box1) will check the collision between the circle and box1 collision
2. pygame.sprite.collide_rect(sprite1,sprite2) willl also do the same """
  
