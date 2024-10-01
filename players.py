import asyncio

class Player:
    def __init__(self, user, name, text_channel_id, voice_channel_id, constTraits, xCoord, yCoord, direction, inventory, action, ticks, cooldown, statWarmth, statHunger, statHealth, statSanity, statStamina, statWeight, maxWeight, modWarmth, modHunger, modHealth, modSanity, modStamina, modStrength, condition):
        self.user = user
        self.name = name
        self.text_channel_id = text_channel_id
        self.voice_channel_id = voice_channel_id
        self.constTraits = constTraits

        self.xCoord = xCoord
        self.yCoord = yCoord
        self.direction = direction
        self.inventory = inventory
        self.action = action
        self.ticks = ticks
        self.cooldown = cooldown

        self.statWarmth = statWarmth
        self.statHunger = statHunger
        self.statHealth = statHealth
        self.statSanity = statSanity
        self.statStamina = statStamina
        self.statWeight = statWeight

        self.maxWeight = maxWeight

        self.modWarmth = modWarmth
        self.modHunger = modHunger
        self.modHealth = modHealth
        self.modSanity = modSanity
        self.modStamina = modStamina
        self.modStrength = modStrength

        self.condition = condition

# conditions: encumbered, burning, bleeding, poisoned

# self.cooldown = int((16-self.statStrength)*0.5) UNIVERSAL COOLDOWN

    def move(direction):
        if type(self.xCoord)==int and type(self.yCoord)==int:
            board[self.xCoord][self.yCoord].players.remove(self.name)

            if self.action!='hiding':
                for player in player_list:
                    if ((self.xCoord+(direction=='west')>player.xCoord>self.xCoord-(direction=='east') and self.yCoord==player.yCoord) or (self.yCoord+(direction=='north')>player.yCoord>self.yCoord-(direction=='south') and self.xCoord==player.xCoord)) and player.action not in ['hiding','sleeping','knockedout','faking_sleeping','faking_knockedout','faking_dead']:
                        move_to_vc(player.voice_channel_id)
                        if len(board[self.xCoord][self.yCoord].players)==0:
                            board[self.xCoord][self.yCoord].channel=delete_channel(board[self.xCoord][self.yCoord].channel)
                        self.voice_channel_id = player.voice_channel_id
                        break

            if self.voice_channel_id == board[self.xCoord][self.yCoord].channel:
                self.voice_channel_id = create_vc(self.name)
                move_to_vc(self.voice_channel_id)
                if len(board[self.xCoord][self.yCoord].players)==0:
                    board[self.xCoord][self.yCoord].channel=delete_channel(board[self.xCoord][self.yCoord].channel)

            self.xCoord+=((direction=='east')-(direction=='west'))*0.01
            self.yCoord+=((direction=='north')-(direction=='south'))*0.01

        else:
            self.xCoord = round(self.xCoord)
            self.yCoord = round(self.yCoord)
            board[self.xCoord][self.yCoord].players.append(self.name)

            if self.action!='hiding':
                for player in player_list:
                    if player.voice_channel_id==self.voice_channel_id:
                        self.voice_channel_id = None
                        break

                if len(board[self.xCoord][self.yCoord].players)==0:
                    board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type)

                move_to_vc(board[self.xCoord][self.yCoord].channel)

                if self.voice_channel_id != None:
                    self.voice_channel_id = delete_channel(self.voice_channel_id)

                self.voice_channel_id=board[self.xCoord][self.yCoord].channel

 
#                board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type)
#                move_to_vc(board[self.xCoord][self.yCoord].channel)
#            board[self.xCoord][self.yCoord].players.append(self.name)

            match direction:
                case 'n':
                    pass
                case 's':
                    pass
                case 'e':
                    pass
                case 'w':
                    pass
                case _:
                    message()
           
#
#                if len(board[self.xCoord][self.yCoord].players)==0:
#                    board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type)
#                    move_to_vc(board[self.xCoord][self.yCoord].channel)
#                board[self.xCoord][self.yCoord].players.append(self.name)

    def run():
        pass

    def loot():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.ticks=int((16-self.statStrength)+5) 
            self.action = 'looting'
        else: message()

    def give(player, object):
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            pass
        else: message()

    def search_player(player):
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            pass
        else: message()

    def craft(object):
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            pass
        else: message()

    def use(object, action):
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            pass
        else: message()

    def hunt():
        if self.action == 'hiding' and self.cooldown == -1:
            self.ticks=int((16-self.statStrength)+5) 
            self.action = 'hunting'
        else: message()

    def attack(player):
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'attacking'
        else: message()

    def hide():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'hiding'
            for player in player_list:
                if player.voice_channel_id==self.voice_channel_id:
                    self.voice_channel_id = create_vc(self.name)
                    move_to_vc(self.voice_channel_id)
                    break
            
        else: message()

    def rest():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'resting'
        else: message()

    def sleep():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'sleeping'
            for player in player_list:
                if player.voice_channel_id==self.voice_channel_id:
                    self.voice_channel_id = create_vc(self.name)
                    move_to_vc(self.voice_channel_id)
                    break
        else: message()

    def fakeDeath():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'faking_dead'
            for player in player_list:
                if player.voice_channel_id==self.voice_channel_id:
                    self.voice_channel_id = create_vc(self.name)
                    move_to_vc(self.voice_channel_id)
                    break
        else: message()

    def fakeKnockOut():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'faking_knockedout'
            for player in player_list:
                if player.voice_channel_id==self.voice_channel_id:
                    self.voice_channel_id = create_vc(self.name)
                    move_to_vc(self.voice_channel_id)
                    break
        else: message()

    def fakeSleep():
        if self.action != 'sleeping' and self.action != 'knockedout' and self.cooldown == -1:
            self.action = 'faking_sleeping'
            for player in player_list:
                if player.voice_channel_id==self.voice_channel_id:
                    self.voice_channel_id = create_vc(self.name)
                    move_to_vc(self.voice_channel_id)
                    break
        else: message()

    def wake_up(): # later

        if self.action == 'sleeping':
            if self.statStamina >= 60:
                self.action = 'resting'
                self.cooldown = int((16-self.statStrength)*0.5)
                if len(board[self.xCoord][self.yCoord].players)==1:
                    board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type) 
                move_to_vc(board[self.xCoord][self.yCoord].channel)
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                self.voice_channel_id = board[self.xCoord][self.yCoord].channel

        elif self.action == 'knockedout':
            self.action = 'resting'
            self.cooldown = int((16-self.statStrength)*0.5)
            if type(self.xCoord)==int and type(self.yCoord)==int:
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                if len(board[self.xCoord][self.yCoord].players)==1:
                    board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type)
                move_to_vc(board[self.xCoord][self.yCoord].channel)
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                self.voice_channel_id = board[self.xCoord][self.yCoord].channel
            else:
                for player in player_list:
                    if ((int(self.xCoord)+1>player.xCoord>int(self.xCoord) and self.yCoord==player.yCoord) or (int(self.yCoord)+1>player.yCoord>int(self.yCoord) and self.xCoord==player.xCoord)) and player.action not in ['hiding','sleeping','knockedout','faking_sleeping','faking_knockedout','faking_dead']:
                        move_to_vc(player.voice_channel_id)
                        self.voice_channel_id = delete_channel(self.voice_channel_id)
                        self.voice_channel_id = player.voice_channel_id
                        break

        elif self.action in ['hiding','faking_knockedout','faking_dead','faking_sleeping']:
            self.action = 'resting'
            if type(self.xCoord)==int and type(self.yCoord)==int:
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                if len(board[self.xCoord][self.yCoord].players)==1:
                    board[self.xCoord][self.yCoord].channel=create_vc(board[self.xCoord][self.yCoord].Type)
                move_to_vc(board[self.xCoord][self.yCoord].channel)
                self.voice_channel_id = delete_channel(self.voice_channel_id)
                self.voice_channel_id = board[self.xCoord][self.yCoord].channel
            else:
                for player in player_list:
                    if ((int(self.xCoord)+1>player.xCoord>int(self.xCoord) and self.yCoord==player.yCoord) or (int(self.yCoord)+1>player.yCoord>int(self.yCoord) and self.xCoord==player.xCoord)) and player.action not in ['hiding','sleeping','knockedout','fake_sleeping','fake_knockedout','fake_dead']:
                        self.voice_channel_id = delete_channel(self.voice_channel_id)
                        self.voice_channel_id = player.voice_channel_id
                        move_to_vc(player.voice_channel_id)
                        break

    def die():
        pass
    def quit():
        pass

    def tick():

        if self.statWarmth>100: self.statWarmth=100
        if self.statHunger>100: self.statHunger=100
        if self.statSanity>100: self.statSanity=100
        if self.statStamina>100: self.statStamina=100

        if self.statWarmth>=50 and self.statWarmth+self.modWarmth<=50: message()
        if self.statHunger>=50 and self.statHunger+self.modHunger<=50: message()
        if self.self.statHealth>=50 and self.statHealth+self.modHealth<=50: message()
        if self.self.statSanity>=50 and self.statSanity+self.modSanity<=50: message()
        if self.statStamina>=50 and self.statStamina+self.modStamina<=50: message()

        if self.statStamina<50:
            if randint(0,100)<=((50-self.statStamina)/50)*10: sleep()
        if self.statSanity<50:
            if randint(0,100)<=((50-self.statSanity)/50)*10: breakdown()

        self.ticks-=1
        self.statWarmth+=self.modWarmth
        self.statHunger+=self.modHunger
        self.statHealth+=self.modHealth
        self.statSanity+=self.modSanity
        self.statStamina+=self.modStamina
        if self.cooldown>-1: self.cooldown-=1

# STATE LIST
#
# walking
# running
# looting
# hunting
# hiding
# resting
# sleeping
# breakdown
# faking_dead
# faking_knockedout
# knockedout
#

        self.modStrength = self.statWarmth*self.statHunger*self.statHealth*self.statStamina*(1-self.statWeight/20)*(0.02**4) #VARIABLE

        self.modWarmth=0 #later
        self.modHunger=-0.07
        self.modHealth=(-('bleeding' in self.condition)-('poisoned' in self.condition)-('burning' in self.condition)*2+((self.statWarmth-50)-abs(self.statWarmth-50)*0.5)*0.01+((self.statHunger-50)-abs(self.statHunger-50)*0.5)*0.01)*0.2 #VARIABLE
        self.modSanity=((self.statWarmth-50)+(self.statHunger-50)+(self.statHealth-50)+(self.statStamina-50)-100)*0.01*0.07 #VARIABLE
        self.modStamina=-(self.statWeight/self.maxWeight)*0.07+(-(self.action=='walking')-(self.action=='running')*3-(self.action=='hunting')-(self.action=='hiding'))*0.5*0.07-0.07 #VARIABLE

        if self.statWarmth<0:
            self.statWarmth=0
        if self.statHunger<0:
            self.statHunger=0
        if self.statHealth<=0:
            die()
        if self.statSanity<=0:
            die()
        if self.statStamina<=0:
            die()

        match self.action:
            case 'walking':
                xStep=((direction=='east')-(direction=='west'))*(board[int(self.xCoord)][self.yCoord].terrain_bonus+board[int(self.xCoord)+1][self.yCoord].terrain_bonus+self.modStrength) # CALCULATIONS NEEDED
                yStep=((direction=='north')-(direction=='south'))*(board[self.xCoord][int(self.yCoord)].terrain_bonus+board[self.xCoord][int(self.yCoord)+1].terrain_bonus+self.modStrength) # CALCULATIONS NEEDED
                if int(self.xCoord)==int(self.xCoord+xStep) and int(self.yCoord)==int(self.yCoord+yStep) and self.xCoord+xStep!=int(self.xCoord) and self.yCoord+yStep!=int(self.yCoord):
                    self.xCoord+=xStep
                    self.yCoord+=yStep
                else:
                    message()
                    self.action=None

            case 'running':
                xStep=((direction=='east')-(direction=='west'))*(board[int(self.xCoord)][self.yCoord].terrain_bonus+board[int(self.xCoord)+1][self.yCoord].terrain_bonus+self.modStrength) # CALCULATIONS NEEDED
                yStep=((direction=='north')-(direction=='south'))*(board[self.xCoord][int(self.yCoord)].terrain_bonus+board[self.xCoord][int(self.yCoord)+1].terrain_bonus+self.modStrength) # CALCULATIONS NEEDED
                if int(self.xCoord)==int(self.xCoord+xStep) and int(self.yCoord)==int(self.yCoord+yStep) and self.xCoord+xStep!=int(self.xCoord) and self.yCoord+yStep!=int(self.yCoord):
                    self.xCoord+=xStep*2
                    self.yCoord+=yStep*2
                else:
                    message()
                    self.action=None

            case 'looting':
                if self.ticks=='0':
                    item = board[self.xCoord][self.yCoord].loot.pop(random.randint(0,len(board[self.xCoord][self.yCoord].loot)-1))
                    board[self.xCoord][self.yCoord].loot.append(None)
                    if item != None:
                        self.inventory.append(item)
                        message() 
                    self.ticks=int((16-self.statStrength)+5) #VARIABLE
            case 'hunting':
                pass
            case 'hiding':
                if self.cooldown == 0:
                    if randint(0,900)<=(1-self.statStrength/16): #VARIABLE
                        wake_up()
                        triggerQTE()
            case 'resting':
                self.modStamina=0.1
            case 'sleeping':
                if self.statStamina>=100:
                    wake_up()
                else:
                    self.modStamina=0.4
            case 'breakdown':
                pass
            case 'faking_dead':
                pass
            case 'faking_knockedout':
                pass
            case 'faking_sleeping':
                pass
            case 'knockedout':
                self.modStamina=0.07
                if self.cooldown=='0':
                    wake_up()            

player_list = []

def add_player(user, channel):
    player_list.append(Player(user=user, name=user.nick, text_channel_id=channel, voice_channel_id=None, constTraits=[], xCoord=0, yCoord=0, direction=None, inventory=[], action=None, ticks=0, cooldown=0, statWarmth=100, statHunger=100, statHealth=100, statSanity=100, statStamina=100, statWeight=0, maxWeight=5, modWarmth=0, modHunger=0, modHealth=0, modSanity=0, modStamina=0, modStrength=0, condition=[]))

def remove_player(user):
    player_list.pop(find_player(user)) 

def find_player(name):
    for i in range(len(player_list)):
        if player_list[i].name==name:
            return i

async def message(name):
    bot.get_channel(player_list[find_player(name)].text_channel_id)