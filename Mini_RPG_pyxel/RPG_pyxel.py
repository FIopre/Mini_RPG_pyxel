import pyxel
import random
import math

LOBBY = 0
GAME = 1
GAMEOVER = 2

ROOM_SIZE = 128
SPACE_BETWEEN_ROOM = 32
CORRIDOR_SIZE = 64

PLAYER_WITHE = 16
PLAYER_HEIGHT = 16

monstres = []

def is_a_room(player,dungeon,direction):
    libre = False
    for i in range(len(dungeon.dungeonRoomPos)):
        if(dungeon.dungeonRoomPos[i][0] < player.x and dungeon.dungeonRoomPos[i][2]+dungeon.dungeonRoomPos[i][0] > player.x+PLAYER_WITHE and dungeon.dungeonRoomPos[i][1] < player.y and dungeon.dungeonRoomPos[i][3]+dungeon.dungeonRoomPos[i][1] > player.y+PLAYER_HEIGHT):
            if direction == 1 and dungeon.dungeonRoomPos[i][1] < player.y-1 and dungeon.dungeonRoomPos[i][3]+dungeon.dungeonRoomPos[i][1] > player.y+PLAYER_HEIGHT:
                libre = True
            if direction == 2 and dungeon.dungeonRoomPos[i][0] < player.x and dungeon.dungeonRoomPos[i][2]+dungeon.dungeonRoomPos[i][0] > player.x+PLAYER_WITHE+1:
                libre = True
            if direction == 3 and dungeon.dungeonRoomPos[i][1] < player.y and dungeon.dungeonRoomPos[i][3]+dungeon.dungeonRoomPos[i][1] > player.y+PLAYER_HEIGHT+1:
                libre = True
            if direction == 4 and dungeon.dungeonRoomPos[i][0] < player.x-1 and dungeon.dungeonRoomPos[i][2]+dungeon.dungeonRoomPos[i][0] > player.x+PLAYER_WITHE:
                libre = True
    return libre

class Dungeon:
    def __init__(self):
        self.iteration = 50
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
            yCorridor += CORRIDOR_SIZE
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
            xCorridor += CORRIDOR_SIZE
            yCorridor += ROOM_SIZE//2 - CORRIDOR_SIZE//2
            corridor = [xCorridor, yCorridor, CORRIDOR_SIZE*3, CORRIDOR_SIZE]
        
        print(xCorridor,yCorridor,direction)
        return corridor
            
    def room(self, direction):
        room = [self.x,self.y,ROOM_SIZE,ROOM_SIZE]
        if direction == 1:
            self.y -= ROOM_SIZE + SPACE_BETWEEN_ROOM
        elif direction == 2:
            self.x += ROOM_SIZE + SPACE_BETWEEN_ROOM
        elif direction == 3:
            self.y += ROOM_SIZE + SPACE_BETWEEN_ROOM
        else:
            self.x -= ROOM_SIZE + SPACE_BETWEEN_ROOM
        return room

class Player:
    def __init__(self):
        self.x = 60
        self.y = 60
        self.velocity = 1
        # Direction 1 = haut
        # Direction 2 = droite
        # Direction 3 = bas
        # Direction 4 = gauche
        self.direction = 2
        self.isAttacking = False
        self.attackDuration = 0
        self.attackZone = [0,0,0,0] # x,y,w,h
        self.noClip = False
        
    def deplacement(self,dungeon):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = 2
            if is_a_room(self,dungeon,self.direction) or self.noClip == True:
                self.x = self.x + self.velocity
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = 4
            if is_a_room(self,dungeon,self.direction) or self.noClip == True:
                self.x = self.x - self.velocity
        if pyxel.btn(pyxel.KEY_DOWN):
            self.direction = 3
            if is_a_room(self,dungeon,self.direction) or self.noClip == True:
                self.y = self.y + self.velocity
        if pyxel.btn(pyxel.KEY_UP):
            self.direction = 1
            if is_a_room(self,dungeon,self.direction) or self.noClip == True:
                self.y = self.y - self.velocity
        
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.noClip = True
        pyxel.camera(self.x-56, self.y-56)
        if pyxel.btnp(pyxel.KEY_E) and self.isAttacking == False:
            self.isAttacking = True
            self.attackDuration = pyxel.frame_count
        if self.attackDuration+15 < pyxel.frame_count:
            self.isAttacking = False
    
    def draw(self,dungeon):
        self.deplacement(dungeon)
        pyxel.rect(self.x, self.y, 16, 16, 11)
        if self.isAttacking == True:
            if self.direction == 1:
                pyxel.blt(self.x,self.y-16,0,0,32,16,16,0)
                self.attackZone = [self.x,self.y-16,16,16]
                
            elif self.direction == 2:
                pyxel.blt(self.x+16,self.y,0,0,32,16,16,0,90)
                self.attackZone = [self.x+16,self.y,16,16]
                
            elif self.direction == 3:
                pyxel.blt(self.x,self.y+16,0,0,32,16,16,0,180)
                self.attackZone = [self.x,self.y+16,16,16]
                
            else:
                pyxel.blt(self.x-16,self.y,0,0,32,16,16,0,270)
                self.attackZone = [self.x-16,self.y,16,16]
            
    
    def reset(self):
        self.x = 60
        self.y = 60
        self.direction = 2

class Monstre:
    def __init__(self):
        self.x = 60
        self.y = 60
        self.status = "Walking"
        self.velocity = random.uniform(0.1,0.9)
        self.attacking = 0
        self.isAttacking = False
        self.flip = 1
        self.dealDmg = False
        self.isAlive = True
        
    def deplacement(self,player):
        if player.x > self.x+8:
            self.flip = 1 
            self.x = self.x + self.velocity
        if player.x < self.x-6:
            self.flip = -1 
            self.x = self.x - self.velocity
        if player.y > self.y+8:
            self.y = self.y + self.velocity
        if player.y < self.y-8:
            self.y = self.y - self.velocity
        
    
    def update(self,player):
        if math.sqrt((player.x-self.x)**2+(player.y-self.y)**2) <= 12 and self.isAttacking == False:
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
            self.deplacement(player)
        
        if self.dealDmg == True:
            if player.x < self.x+8 and player.x > self.x-8 and player.y < self.y+8 and player.y > self.y-8:
                return "fin"

    
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
        self.player.update()
        if pyxel.btnp(pyxel.KEY_R):
            monstres.append(Monstre())
            
        for monstre in monstres:
            monstre.update(self.player)
            if monstre.x < self.player.attackZone[0] + self.player.attackZone[2] and monstre.x + 16 > self.player.attackZone[0] and monstre.y < self.player.attackZone[1] + self.player.attackZone[3] and monstre.y + 16 > self.player.attackZone[1] and self.player.isAttacking == True:
                monstre.isAlive = False
            if monstre.update(self.player) == "fin":
                self.scene = GAMEOVER
        
        # Clear les mobs mort
        for monstre in monstres:
            if monstre.isAlive == False:
                monstres.remove(monstre)
    
    def update_gameover(self):
        pyxel.camera(0,0)
        pyxel.mouse(True)
        monstres.clear()
        self.player.reset()
        if 48 <= pyxel.mouse_x <= 80 and 60 <= pyxel.mouse_y <= 70:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
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
        self.player.draw(self.dungeon)
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
