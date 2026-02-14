import pyxel
import random
import math

LOBBY = 0
GAME = 1
GAMEOVER = 2

ROOM_SIZE = 128
SPACE_BETWEEN_ROOM = ROOM_SIZE//4
CORRIDOR_SIZE = ROOM_SIZE//2
NUMBER_OF_ROOM = 200

PLAYER_WITHE = 16
PLAYER_HEIGHT = 16
PLAYER_VELOCITY = 1 # Si la velocite est au dessus de 1 le joueur peut finir bloquer dans les murs

BULLET_SIZE = 16
BULLET_LIFE = 40

MONSTRE_SIZE = 16

monstres = []
bullets = []

def isRoom(entitie,dungeon,direction):
    libre = False
    for i in range(len(dungeon.dungeonRoomPos)):
        if(dungeon.dungeonRoomPos[i][0] < entitie.x and dungeon.dungeonRoomPos[i][2]+dungeon.dungeonRoomPos[i][0] > entitie.x+PLAYER_WITHE and dungeon.dungeonRoomPos[i][1] < entitie.y and dungeon.dungeonRoomPos[i][3]+dungeon.dungeonRoomPos[i][1] > entitie.y+PLAYER_HEIGHT):
            if direction == 1 and dungeon.dungeonRoomPos[i][1] < entitie.y-1 and dungeon.dungeonRoomPos[i][3]+dungeon.dungeonRoomPos[i][1] > entitie.y+PLAYER_HEIGHT:
                libre = True
            if direction == 2 and dungeon.dungeonRoomPos[i][0] < entitie.x and dungeon.dungeonRoomPos[i][2]+dungeon.dungeonRoomPos[i][0] > entitie.x+PLAYER_WITHE+1:
                libre = True
            if direction == 3 and dungeon.dungeonRoomPos[i][1] < entitie.y and dungeon.dungeonRoomPos[i][3]+dungeon.dungeonRoomPos[i][1] > entitie.y+PLAYER_HEIGHT+1:
                libre = True
            if direction == 4 and dungeon.dungeonRoomPos[i][0] < entitie.x-1 and dungeon.dungeonRoomPos[i][2]+dungeon.dungeonRoomPos[i][0] > entitie.x+PLAYER_WITHE:
                libre = True
    return libre


class Dungeon:
    def __init__(self):
        self.iteration = NUMBER_OF_ROOM
        self.x = 0
        self.y = 0
        self.dungeonRoomPos = [] #x,y,w,h
        
        self.dungeonPath()
    
    def dungeonPath(self):
        for i in range(self.iteration):
            # Direction 1 = haut
            # Direction 2 = droite
            # Direction 3 = bas
            # Direction 4 = gauche
            direction = random.randint(1,4)
            self.dungeonRoomPos.append(self.corridor(direction))
            self.dungeonRoomPos.append(self.room(direction))
        #Piece final
        self.dungeonRoomPos.append(self.room(0))
    
    def draw(self,player):
        for i in range(len(self.dungeonRoomPos)):
            if i%2 == 0:
                pyxel.rect(self.dungeonRoomPos[i][0],self.dungeonRoomPos[i][1],self.dungeonRoomPos[i][2],self.dungeonRoomPos[i][3],7)
            else:
                pyxel.rect(self.dungeonRoomPos[i][0],self.dungeonRoomPos[i][1],self.dungeonRoomPos[i][2],self.dungeonRoomPos[i][3],6)
                
    def corridor(self, direction):
        xCorridor = self.x
        yCorridor = self.y
        if direction == 1:
            xCorridor += ROOM_SIZE//2 - CORRIDOR_SIZE//2
            yCorridor -= CORRIDOR_SIZE*2
            corridor = [xCorridor, yCorridor, CORRIDOR_SIZE, CORRIDOR_SIZE*3]
        elif direction == 2:
            xCorridor += ROOM_SIZE - CORRIDOR_SIZE
            yCorridor += ROOM_SIZE//2 - CORRIDOR_SIZE//2
            corridor = [xCorridor, yCorridor, CORRIDOR_SIZE*3, CORRIDOR_SIZE]
        elif direction == 3:
            xCorridor += ROOM_SIZE//2 - CORRIDOR_SIZE//2
            yCorridor += ROOM_SIZE - CORRIDOR_SIZE
            corridor = [xCorridor, yCorridor, CORRIDOR_SIZE, CORRIDOR_SIZE*3]
        else:
            xCorridor -= CORRIDOR_SIZE*2
            yCorridor += ROOM_SIZE//2 - CORRIDOR_SIZE//2
            corridor = [xCorridor, yCorridor, CORRIDOR_SIZE*3, CORRIDOR_SIZE]
        return corridor
            
    def room(self, direction):
        room = [self.x,self.y,ROOM_SIZE,ROOM_SIZE]
        self.generateZombie()
        if direction == 1:
            self.y -= ROOM_SIZE + SPACE_BETWEEN_ROOM
        elif direction == 2:
            self.x += ROOM_SIZE + SPACE_BETWEEN_ROOM
        elif direction == 3:
            self.y += ROOM_SIZE + SPACE_BETWEEN_ROOM
        elif direction == 4:
            self.x -= ROOM_SIZE + SPACE_BETWEEN_ROOM
        return room
    
    def generateZombie(self):
        nb_ennemie = random.randint(1,4)
        for i in range(nb_ennemie):
            #On genere pas de zombie dans la premiere salle
            if (self.x != 0 or self.y != 0):
                monstres.append(Zombie(self.x+random.randint(20,100),self.y+random.randint(20,100)))


class Bullet:
    def __init__(self, x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.life_duration = pyxel.frame_count
        self.is_alive = True
    
    def update(self):
        if self.direction == 1:
            self.y -= 2
        elif self.direction == 2:
            self.x += 2
        elif self.direction == 3:
            self.y += 2
        else:
            self.x -= 2
        
        if pyxel.frame_count - self.life_duration > BULLET_LIFE:
            self.is_alive = False
    
    def draw(self):
        if self.direction == 1:
            pyxel.blt(self.x,self.y,0,16,32,16,16,0,270)
        elif self.direction == 2:
            pyxel.blt(self.x,self.y,0,16,32,16,16,0,0)
        elif self.direction == 3:
            pyxel.blt(self.x,self.y,0,16,32,16,16,0,90)
        else:
            pyxel.blt(self.x,self.y,0,16,32,16,16,0,180)
           
        
class Player:
    def __init__(self):
        self.PlayerVie = {
            "Coeur": 3,
            "Vie":3,
            "CoeurBleu": 0
        }
        self.x = 60
        self.y = 60
        # Direction 1 = haut
        # Direction 2 = droite
        # Direction 3 = bas
        # Direction 4 = gauche
        self.direction = 2
        self.isAttacking = False
        self.attackDuration = 0
        self.attackZone = [0,0,0,0] # x,y,w,h
        self.noClip = False
        self.hitable = True
        self.hitCd = 0
        self.minimap_open = False
        
    def deplacement(self,dungeon):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = 2
            if isRoom(self,dungeon,self.direction) or self.noClip == True:
                self.x = self.x + PLAYER_VELOCITY
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = 4
            if isRoom(self,dungeon,self.direction) or self.noClip == True:
                self.x = self.x - PLAYER_VELOCITY
        if pyxel.btn(pyxel.KEY_DOWN):
            self.direction = 3
            if isRoom(self,dungeon,self.direction) or self.noClip == True:
                self.y = self.y + PLAYER_VELOCITY
        if pyxel.btn(pyxel.KEY_UP):
            self.direction = 1
            if isRoom(self,dungeon,self.direction) or self.noClip == True:
                self.y = self.y - PLAYER_VELOCITY
        
    
    def update(self, dungeon):
        if pyxel.btnp(pyxel.KEY_P):
            self.noClip = True
        self.deplacement(dungeon)
        pyxel.camera(self.x-56, self.y-56)
        if pyxel.btnp(pyxel.KEY_E) and self.isAttacking == False:
            self.isAttacking = True
            self.attackDuration = pyxel.frame_count
            bullets.append(Bullet(self.x,self.y,self.direction))
        
        if pyxel.btnp(pyxel.KEY_TAB):
            self.minimap_open = not self.minimap_open
            
        if self.attackDuration+15 < pyxel.frame_count:
            self.isAttacking = False
        if self.hitable == False and pyxel.frame_count - self.hitCd > 15:
            self.hitable = True
    
    def draw(self):
        vie = self.PlayerVie["Vie"]
        for i in range(self.PlayerVie["Coeur"]) : 
            if vie > 0:
                vie=vie-1
                pyxel.blt(self.x-57+16*i,self.y-57,0,0,96,16,16,5)
            else:
                pyxel.blt(self.x-57+16*i,self.y-57,0,16,96,16,16,5)
        for i in range(self.PlayerVie["CoeurBleu"]) :
            pyxel.blt(self.x-57+18*i,self.y-41,0,32,96,16,16,0)

        if self.minimap_open:
            pyxel.rectb(self.x-56,self.y-56,128,128,9)
            pyxel.rect(self.x-56,self.y-56,128,128,10)
        
        
        pyxel.rect(self.x, self.y, 16, 16, 11)
            
    
    def reset(self):
        self.x = 60
        self.y = 60
        self.direction = 2
        self.PlayerVie["Vie"] = 3


#Ne pas utiliser la class monstre directement
class Monstre:
    #Parametre par default (ceux du zombie), ces parametre sont la a but informatif
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.status = "Walking"
        self.velocity = random.uniform(0.1,0.9)
        self.attacking = 0
        self.is_attacking = False
        self.flip = 1
        self.dealDmg = False
        self.is_alive = True
        self.direction = 2
        self.range_detection = 60
        self.attack_range = 8
        self.hp = 3
        self.hit_cd = 0
        self.hitable = True

    def deplacement(self,player,dungeon):
        #Deplacement tout droit vers le joueur
        if(self.detected(player)):
            if player.x > self.x:
                self.direction = 2
                if isRoom(self,dungeon,self.direction):
                    self.flip = 1 
                    self.x = self.x + self.velocity
            if player.x < self.x:
                self.direction = 4
                if isRoom(self,dungeon,self.direction):
                    self.flip = -1 
                    self.x = self.x - self.velocity
            if player.y > self.y:
                self.direction = 3
                if isRoom(self,dungeon,self.direction):
                    self.y = self.y + self.velocity
            if player.y < self.y:
                self.direction = 1
                if isRoom(self,dungeon,self.direction):
                    self.y = self.y - self.velocity
    
    def detected(self,player):
        return self.x - self.range_detection < player.x < self.x + self.range_detection and self.y - self.range_detection < player.y < self.y + self.range_detection
    
    def update(self,player,dungeon):
        if self.hp <= 0:
            self.is_alive = False
        if pyxel.frame_count-self.hit_cd>30:
            self.hitable = True
        if math.sqrt((player.x-self.x)**2+(player.y-self.y)**2) <= self.attack_range and self.isAttacking == False:
            self.attacking = pyxel.frame_count
            self.isAttacking = True
            
        if pyxel.frame_count-24 < self.attacking:
            self.status = "Attacking"
            if pyxel.frame_count-18 > self.attacking:
                self.dealDmg = True
        else:
            self.isAttacking = False
            self.dealDmg = False
            self.status = "Walking"
        
        if self.status == "Walking":
            self.deplacement(player,dungeon)
        
        if self.dealDmg == True:
            if player.x < self.x+8 and player.x > self.x-8 and player.y < self.y+8 and player.y > self.y-8 and player.hitable:
                player.PlayerVie["Vie"] -= 1
                player.hitCd = pyxel.frame_count
                player.hitable = False
     
                
class Zombie(Monstre):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.status = "Walking"
        self.velocity = random.uniform(0.1,0.9)
        self.attacking = 0
        self.is_attacking = False
        self.flip = 1
        self.dealDmg = False
        self.is_alive = True
        self.direction = 2
        self.range_detection = 60
        self.attack_range = 8
        self.hp = 3
        self.hit_cd = 0
        self.hitable = True
    
    def draw(self):
        if pyxel.frame_count-24 < self.attacking:
            # Animation d'attaque
            if pyxel.frame_count-6 < self.attacking:
                pyxel.blt(self.x,self.y,0,0,16,16*self.flip,16,0)
            elif pyxel.frame_count-12 < self.attacking:
                pyxel.blt(self.x,self.y,0,16,16,16*self.flip,16,0)
            elif pyxel.frame_count-18 < self.attacking:
                pyxel.blt(self.x,self.y,0,32,16,16*self.flip,16,0)
            else:
                pyxel.blt(self.x,self.y,0,48,16,16*self.flip,16,0)
        else:
            # Animation de marche*
            if self.velocity >0.3 and self.velocity < 0.7:
                frame = pyxel.frame_count % 8
                if frame == 0 or frame == 1 :
                    pyxel.blt(self.x,self.y,0,0,0,16*self.flip,16,0)
                elif frame == 2 or frame == 3 : 
                    pyxel.blt(self.x,self.y,0,16,0,16*self.flip,16,0)
                elif frame == 4 or frame == 5: 
                    pyxel.blt(self.x,self.y,0,32,0,16*self.flip,16,0)
                elif frame == 6 or frame == 7 :
                    pyxel.blt(self.x,self.y,0,48,0,16*self.flip,16,0)
            elif self.velocity > 0.6:
                frame = pyxel.frame_count % 4
                if frame == 0:
                    pyxel.blt(self.x,self.y,0,0,0,16*self.flip,16,0)
                elif frame == 1 : 
                    pyxel.blt(self.x,self.y,0,16,0,16*self.flip,16,0)
                elif frame == 2: 
                    pyxel.blt(self.x,self.y,0,32,0,16*self.flip,16,0)
                elif frame == 3:
                    pyxel.blt(self.x,self.y,0,48,0,16*self.flip,16,0)
            elif self.velocity < 0.4 :
                frame = pyxel.frame_count % 16
                if frame == 0 or frame == 1 or frame == 2 or frame == 3:
                    pyxel.blt(self.x,self.y,0,0,0,16*self.flip,16,0)
                elif frame == 4 or frame == 5 or frame == 6 or frame == 7: 
                    pyxel.blt(self.x,self.y,0,16,0,16*self.flip,16,0)
                elif frame == 8 or frame == 9 or frame == 10 or frame == 11: 
                    pyxel.blt(self.x,self.y,0,32,0,16*self.flip,16,0)
                elif frame == 12 or frame == 13 or frame == 14 or frame == 15:
                    pyxel.blt(self.x,self.y,0,48,0,16*self.flip,16,0)


class App: 
    def __init__(self):
        pyxel.init(128, 128, title="Slayer")
        #pyxel.mouse(True)
        pyxel.load("res.pyxres")
        
        self.scene = LOBBY
        
        self.player = Player()
        self.dungeon = Dungeon()
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.scene == LOBBY:
            self.update_lobby()
        elif self.scene == GAME:
            self.update_game()
        elif self.scene == GAMEOVER:
            self.update_gameover()
    
    def update_lobby(self):
        pyxel.mouse(True)
        if 48 <= pyxel.mouse_x <= 80 and 60 <= pyxel.mouse_y <= 70:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.scene = GAME
    
    def update_game(self):
        pyxel.mouse(False)
        self.player.update(self.dungeon)
        for bullet in bullets:
            bullet.update()
        
        for monstre in monstres:
            monstre.update(self.player,self.dungeon)
            
            # Si la balle touche un ennemie elle ce detruit et le monstre perd 1 hp
            for bullet in bullets:
                if monstre.x < bullet.x + BULLET_SIZE and monstre.x + MONSTRE_SIZE > bullet.x and monstre.y < bullet.y + BULLET_SIZE and monstre.y + MONSTRE_SIZE > bullet.y and monstre.hitable:
                    monstre.hp -= 1
                    monstre.hit_cd = pyxel.frame_count
                    monstre.hitable = True
                    bullet.is_alive = False
        
        if self.player.PlayerVie["Vie"] <= 0:
            self.scene = GAMEOVER
        
        # Clear les mobs mort
        for monstre in monstres:
            if monstre.is_alive == False:
                monstres.remove(monstre)
        # Clear les balles "morte"
        for bullet in bullets:
            if bullet.is_alive == False:
                bullets.remove(bullet)
    
    def update_gameover(self):
        pyxel.camera(0,0)
        pyxel.mouse(True)
        monstres.clear()
        self.player.reset()
        if 48 <= pyxel.mouse_x <= 80 and 60 <= pyxel.mouse_y <= 70:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.dungeon = Dungeon()
                self.scene = GAME
    
    def draw(self):
        if self.scene == LOBBY:
            self.draw_lobby()
        elif self.scene == GAME:
            self.draw_game()
        elif self.scene == GAMEOVER:
            self.draw_gameover()
        
    def draw_lobby(self):
        pyxel.cls(3)
        if 48 <= pyxel.mouse_x <= 80 and 60 <= pyxel.mouse_y <= 70:
            pyxel.rectb(48,60,32,10,1)
            pyxel.rect(49,61,30,8,5)
            pyxel.text(56,62,"Play",7)
        else:
            pyxel.rectb(48,60,32,10,1)
            pyxel.rect(49,61,30,8,6)
            pyxel.text(56,62,"Play",0)
    
    def draw_game(self):
        pyxel.cls(0)
        self.dungeon.draw(self.player)
        self.player.draw()
        for bullet in bullets:
            bullet.draw()
        for monstre in monstres:
            monstre.draw()
        

    def draw_gameover(self):
        pyxel.cls(8)
        if 48 <= pyxel.mouse_x <= 80 and 60 <= pyxel.mouse_y <= 70:
            pyxel.rectb(48,60,32,10,1)
            pyxel.rect(49,61,30,8,5)
            pyxel.text(51,62,"Respawn",7)
        else:
            pyxel.rectb(48,60,32,10,1)
            pyxel.rect(49,61,30,8,6)
            pyxel.text(51,62,"Respawn",0)


App()