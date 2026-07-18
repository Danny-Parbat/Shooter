import pygame
import os
 
pygame.init()   #initialize pygame
 
screen_width = 800
screen_height = int(screen_width * 0.8)
 
screen = pygame.display.set_mode((screen_width, screen_height))   #create a screen 
pygame.display.set_caption("Shooter")   #set the title of the window
 
#set fps
clock = pygame.time.Clock()   #create a clock object to control the frame rate
fps=60  

#define game variables
GRAVITY = 0.75   #set the gravity variable
TILE_SIZE = 40  #set the tile size variable
 
#define player actions var
moving_left = False
moving_right = False
shoot=False
grenade=False
grenade_thrown=False

#load images
#bullet
bullet_img = pygame.image.load('graphics/icons/bullet.png').convert_alpha()   #load the bullet image

#grenade
grenade_img = pygame.image.load('graphics/icons/grenade.png').convert_alpha()   #load the grenade image

#pickup boxes
health_box_img = pygame.image.load('graphics/icons/health_box.png').convert_alpha()   #load the health box image
ammo_box_img = pygame.image.load('graphics/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('graphics/icons/grenade_box.png').convert_alpha()   #load the grenade box image
item_boxes = {
    'Health' : health_box_img,   #set the health box image
    'Ammo' : ammo_box_img,   #set the ammo box image
    'Grenade' : grenade_box_img   #set the grenade box image
}

#define colors
BG = (144,201,120)   #background color
RED = (255,0,0)   
WHITE = (255,255,255)  
 
#define fonts
font = pygame.font.SysFont('Futura', 30)   #set the font and

def draw_text(text, font, text_col, x, y):   #function to draw text on the screen
    img = font.render(text, True, text_col)   #render the text
    screen.blit(img, (x,y))   #draw the text on the screen

def draw_bg():   #function to draw the bg
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (screen_width, 300))   #draw a red line across the screen at y=300
    
 
class Soldier(pygame.sprite.Sprite):    #create a soldier class that inherits from the pygame sprite class
    def __init__(self, char_type ,player_x, player_y, scale,speed,ammo,grenades):
        pygame.sprite.Sprite.__init__(self)   #initialize the sprite class
        self.alive = True   #set the alive variable to true
        self.char_type = char_type   #set the character type
        self.speed = speed   #set the speed of the player
        self.ammo = ammo  #set the ammo of the player
        self.start_ammo = ammo   #set the starting ammo of the player
        self.shoot_cooldown = 0   #set the shoot cooldown to 0
        self.grenades = grenades   #set the grenades of the player
        self.health = 100   #set the health of the player
        self.max_health = self.health   #set the max health of the player
        self.vel_y = 0   #set the vertical velocity of the player
        self.direction = 1   #set the direction of the player
        self.jump=False
        self.in_air = True   #set the in air variable to true
        self.flip = False   #set the flip of the player
 
        self.animation_list = []   #create a list to hold the animations
        self.frame_index=0   #set the index of the animation list
        self.action=0 
        self.update_time = pygame.time.get_ticks()   #get the current time
        
        #load all images for the players
        animation_types = ['Idle', 'Run','Jump','Death']   #create a list of the animation types
        for animation in animation_types:   #loop through the animation types   
            #reset temporary list of images
            temp_list = []   #create a temporary list to hold the images
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'graphics/{self.char_type}/{animation}'))
            for i in range(num_of_frames):   #loop through the range of the animation frames
                img = pygame.image.load(f'graphics/{self.char_type}/{animation}/{i}.png').convert_alpha()   #load the image and convert it to alpha
                img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))   #scale the player image
                temp_list.append(img)   #add the player image to the temporary list
            self.animation_list.append(temp_list)   #add the temporary list to the animation list


        self.player_img=self.animation_list[self.action][self.frame_index]   #set the player image to the first image in the animation list
        #self.player_img = pygame.image.load(f'graphics/{self.char_type}/Idle/0.png')   #load the player image
        self.player_rect = self.player_img.get_rect(center = (player_x, player_y))   #create a rectangle for the player
        self.rect = self.player_rect   #set the rect of the player to the player rect
        #self.player_img = pygame.transform.scale(self.player_img, (int(self.player_img.get_width()*scale), int(self.player_img.get_height()*scale)))   #scale the player image
 
    def update(self):
        self.update_animation()   #call the update animation function
        self.check_alive()   #call the check alive function
        #update cooldowns
        if self.shoot_cooldown > 0:   #if the shoot cooldown is greater than 0
            self.shoot_cooldown -= 1   #decrease the shoot cooldown by 1


    def move(self,moving_left,moving_right):
        #reset movement var:
        dx=0
        dy=0
 
        #assign movement variables moving left/right
        if moving_left:   #if the player is moving left
            dx= -self.speed   #move the player left
            self.flip = True   #flip the player image
            self.direction = -1   #set the direction of the player to left
        if moving_right:   #if the player is moving right
            dx= self.speed   #move the player right
            self.flip = False   #don't flip the player image
            self.direction = 1   #set the direction of the player to right

        #jump
        if self.jump==True and self.in_air==False:   #if the player is jumping and not in the air
            self.vel_y= -11
            self.jump=False
            self.in_air=True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy+= self.vel_y

        #check for collision with the ground
        if self.player_rect.bottom + dy > 300:   #if the player is below the ground
            dy = 300 - self.player_rect.bottom   #set the dy to the distance to the ground
            self.in_air = False   #set the in air variable to false
            self.vel_y = 0   #reset the vertical velocity of the player

        #update rect position
        self.player_rect.x += dx
        self.player_rect.y += dy
        #screen.blit(self.player_img, self.player_rect)   #draw the player on the screen
 
    def shoot(self):
        #shoot bullets
        if self.shoot_cooldown == 0 and self.ammo > 0:   #if the shoot cooldown is 0 and the player has ammo
            self.shoot_cooldown = 20   #set the shoot cooldown to 20
            self.ammo -= 1   #decrease the ammo by 1
            bullet = Bullet(self.player_rect.centerx + (0.6 * self.player_rect.size[0] * self.direction), self.player_rect.centery, self.direction)   #create a bullet object
            bullet_group.add(bullet)   #add the bullet to the bullet group

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100   #set the animation cooldown
        #update image depending on current frame
        self.player_img = self.animation_list[self.action][self.frame_index]   #set the player image to the current frame in the animation list   
        if pygame.time.get_ticks() - self.update_time> ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()   #update the update time
            self.frame_index +=1
 
        if self.frame_index>=len(self.animation_list[self.action]):   #if the frame index is greater than or equal to the length of the animation list
            if self.action==3:   #if the action is death
                self.frame_index = len(self.animation_list[self.action]) - 1   #set the frame index to the last frame in the animation list
            else:
                self.frame_index = 0   #reset the frame index to 0
        

    
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action   #set the action to the new action
            #update the animation settings
            self.frame_index = 0   #reset the frame index to 0
            self.update_time = pygame.time.get_ticks()   #update the update time

    def check_alive(self):
        #check if the player is alive
        if self.health <= 0:   #if the player's health is less than or equal to 0
            self.health = 0   #set the player's health to 0
            self.alive = False   #set the alive variable to false
            self.speed = 0   #set the speed of the player to 0
            self.update_action(3)   #set the action to death

    def draw(self):
        screen.blit(pygame.transform.flip(self.player_img, self.flip, False), self.player_rect)   #draw the player on the screen
        

class ItemBox(pygame.sprite.Sprite):   #create a bullet class that inherits from the pygame sprite class
    def __init__(self, item_type, x,y):
        pygame.sprite.Sprite.__init__(self)   #initialize the sprite class
        self.item_type = item_type   #set the item type
        self.image = item_boxes[self.item_type]   #set the item type to the item boxes dictionary
        self.rect = self.image.get_rect()   #create a rectangle for the item
        self.rect.midtop = (x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))   #set the position of the item
        

    def update(self):
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):   #if the player collides with the item box
            #check what kind of box it was
            if self.item_type == 'Health':   #if the item type is health
                player.health += 25   #increase the player's health by 25
                if player.health > player.max_health:
                    player.health = player.max_health   #set the player's health to the max health
                if player.health > player.max_health:   #if the player's health is greater than the max health
                    player.health = player.max_health   #set the player's health to the max health
            elif self.item_type == 'Ammo':   #if the item type is ammo
                player.ammo += 15   #increase the player's ammo by 15
            elif self.item_type == 'Grenade':   #if the item type is grenade
                player.grenades += 3   #increase the player's grenades by 3
            
            self.kill()   #remove the item box from the game


class Bullet(pygame.sprite.Sprite):   #create a bullet class that inherits from the pygame sprite class
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)   #initialize the sprite class
        self.speed = 10   #set the speed of the bullet
        self.image = bullet_img   #set the image of the bullet
        self.rect = self.image.get_rect(center = (x,y))   #create a rectangle for the bullet
        self.rect.center = (x,y)   #set the position of the bullet
        self.direction = direction   #set the direction of the bullet

    def update(self):
        #move bullet in specified direction
        self.rect.x += (self.direction * self.speed)   #move the bullet in the specified direction
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:   #if the bullet is off the screen
            self.kill()   #remove the bullet from the game

        #check for collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):   #if the bullet
            if player.alive:   #if the player is alive
                player.health -= 5   #decrease the player's health by 10
                
                self.kill()   #remove the bullet from the game
        for enemy in enemy_group:   #loop through the enemies
            if pygame.sprite.spritecollide(enemy, bullet_group, False):   #if the bullet collides with the enemy
                if enemy.alive:   #if the enemy is alive
                    enemy.health -= 25   #decrease the enemy's health by 10
                    print(enemy.health)   #print the enemy's health
                    self.kill()   #remove the bullet from the game    


class Grenade(pygame.sprite.Sprite):   #create a bullet class that inherits from the pygame sprite class
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)   #initialize the sprite class
        self.timer = 100   #set the timer of the grenade
        self.vel_y = -11   #set the vertical velocity of the grenade
        self.speed = 7   #set the speed of the bullet
        self.image = grenade_img   #set the image of the bullet
        self.rect = self.image.get_rect()   #create a rectangle for the bullet
        self.rect.center = (x,y)   #set the position of the bullet
        self.direction = direction   #set the direction of the bullet

    def update(self):
        #move grenade
        self.vel_y += GRAVITY   #apply gravity to the vertical velocity of the grenade
        dx = self.direction * self.speed   #set the horizontal velocity of the grenade
        dy = self.vel_y   #set the vertical velocity of the grenade

        #check for collision with the ground
        if self.rect.bottom + dy > 300:   #if the grenade is below the ground
            dy = 300 - self.rect.bottom   #set the dy to the distance to the ground
            self.speed=0   #set the speed of the grenade to 0
            
        #check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:   #if the grenade is off the screen
            self.direction *= -1   #reverse the direction of the grenade
            dx = self.direction * self.speed   #set the horizontal velocity of the grenade
        #update position
        self.rect.x += dx   #update the x position of the grenade
        self.rect.y += dy   #update the y position of the grenade

        #countdown timer
        self.timer -= 1   #decrease the timer by 1
        if self.timer <= 0:   #if the timer is less than or equal to 0
            self.kill()   #remove the grenade from the game
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)   #create an explosion object
            explosion_group.add(explosion)   #add the explosion to the explosion group
            #do damage to anyone that is nearby
            if abs(self.rect.centerx - player.player_rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.player_rect.centery) < TILE_SIZE * 2:
                player.health -= 50   #decrease the player's health by 50
            for enemy in enemy_group:   #loop through the enemies
                
            
                if abs(self.rect.centerx - enemy.player_rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.player_rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50   #decrease the enemy's health by 50


class Explosion(pygame.sprite.Sprite):   #create a bullet class that inherits from the pygame sprite class
    def __init__(self, x, y,scale):
        pygame.sprite.Sprite.__init__(self)   #initialize the sprite class
        self.images=[]
        for num in range (1,6):
            img = pygame.image.load(f'graphics/explosion/exp{num}.png').convert_alpha()   #load the explosion images
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))   #scale the explosion images
            self.images.append(img)   #add the explosion images to the images list
        self.frame_index=0   #set the frame index to 0
        self.image = self.images[self.frame_index]   #set the image of the explosion
        self.rect = self.image.get_rect()   #create a rectangle for the explosion
        self.rect.center = (x,y)   #set the position of the explosion
        self.counter = 0   #set the counter to 0

    def update(self):
        EXPLOSION_SPEED = 4   #set the explosion speed
        #update explosion animation
        self.counter += 1   #increase the counter by 1

        if self.counter >= EXPLOSION_SPEED:   #if the counter is greater than or equal to the explosion speed
            self.counter = 0   #reset the counter to 0
            self.frame_index += 1   #increase the frame index by 1
            #if the animation is complete, delete the explosion
            if self.frame_index >= len(self.images):   #if the frame index is greater than or equal to the length of the images list
                self.kill()   #remove the explosion from the game
            else:
                self.image = self.images[self.frame_index]   #set the image of the explosion to the current frame in the images list
    

enemy_group = pygame.sprite.Group()   #create a group for the enemies
bullet_group = pygame.sprite.Group()   #create a group for the bullets
grenade_group = pygame.sprite.Group()   #create a group for the grenades
explosion_group = pygame.sprite.Group()   #create a group for the explosions
item_box_group = pygame.sprite.Group()   #create a group for the item boxes

#temp create item boxes
item_box = ItemBox('Health', 200, 260)   #create a health item box
item_box_group.add(item_box)   #add the health item box to the item box group
ammo_box = ItemBox('Ammo', 300, 260)   #create an ammo item box
item_box_group.add(ammo_box)   #add the ammo item box to the item box
grenade_box = ItemBox('Grenade', 400, 260)   #create a grenade item box
item_box_group.add(grenade_box)   #add the grenade item box to the item box

player = Soldier('player',200, 200, 3,5,20,5)   #create a player object
enemy = Soldier('enemy',400, 200, 3,5,20,0) 
enemy2 = Soldier('enemy',300, 300, 3,5,20,0)
enemy_group.add(enemy)   #add the enemy to the enemy group
enemy_group.add(enemy2)   #add the second enemy to the enemy group
# player2= Soldier(400, 200, 3)   #create a second player object
 
 
run = True
while run: #keep running the game
    clock.tick(fps)   #set the fps
    draw_bg()   #draw the background

    #show ammo
    draw_text('AMMO:', font, WHITE, 10, 35)   #draw the ammo text on the screen
    for x in range(player.ammo):   #loop through the player's ammo
        screen.blit(bullet_img, (90 + (x * 10), 40))   #draw the bullet image on the screen for each ammo
    
    #show grenades
    draw_text('GRENADES:', font, WHITE, 10, 65)   #draw the grenades text on the screen
    for x in range(player.grenades):   #loop through the player's grenades
        screen.blit(grenade_img, (135 + (x * 15), 60))   #draw the grenade image on the screen for each grenade
    
 
    player.update()
    player.draw()   #draw the player on the screen
    
    for enemy in enemy_group:   #loop through the enemies
        enemy.update()
        enemy.draw()   #draw the enemy on the screen
        
        enemy2.update()
        enemy2.draw()   #draw the second enemy on the screen
        
    #update and draw groups
    bullet_group.update()   #update the bullets
    explosion_group.update() 
    item_box_group.update()   #update the item boxes
    item_box_group.draw(screen)   #draw the item boxes on the screen
    explosion_group.draw(screen)   #draw the explosions on the screen
    bullet_group.draw(screen)   #draw the bullets on the screen
    grenade_group.update()   #update the grenades
    grenade_group.draw(screen)   #draw the grenades on the screen

    #update player actions
    if player.alive:
        #shoot bullets
        if shoot:
            player.shoot()   #call the shoot function of the player
            shoot=False   #reset the shoot variable to false
        #throw grenades
        elif grenade and grenade_thrown==False and player.grenades>0:
            grenade=Grenade(player.player_rect.centerx + (0.5 * player.player_rect.size[0] * player.direction), \
                            player.player_rect.top, player.direction)  #create a grenade object
            grenade_group.add(grenade)   #add the grenade to the grenade group
            #reduce grenade count
            player.grenades -= 1
            grenade_thrown=True
            
        if player.in_air:
            player.update_action(2)   #2: jump
        elif moving_left or moving_right:
            player.update_action(1)   #1: run
        else:
            player.update_action(0)   #0: idle
        player.move(moving_left,moving_right)   #move the player based on the movement variables
 
    for event in pygame.event.get():   #check for events (quit game)
        if event.type == pygame.QUIT:   #if the user clicks the close button
            run = False   #stop running the game
        
        #keyboard presses
        if event.type == pygame.KEYDOWN:   #if a key is pressed
            if event.key == pygame.K_a:    #if the a key is pressed
                moving_left = True    #move the player left
            if event.key == pygame.K_d:    #if the d key is pressed
                moving_right = True    #move the player right
            if event.key == pygame.K_w and player.alive:
                player.jump=True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump=True
            if event.key == pygame.K_e and player.alive:
                player.jump=True
            if event.key == pygame.K_q:
                grenade=True
            if event.key == pygame.K_ESCAPE:   #if the escape key is pressed
                run = False   #stop running the game
 
        #keyboard releases
        if event.type == pygame.KEYUP:   #if a key is released
            if event.key == pygame.K_a:    #if the a key is released
                moving_left = False    #stop moving the player left
            if event.key == pygame.K_d:    #if the d key is released
                moving_right = False    #stop moving plyr right
            if event.key == pygame.K_q:
                grenade=False
                grenade_thrown=False

        #mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:   #if a mouse button is pressed
            if event.button == 1 and player.alive:    #left click
                shoot=True   #set the shoot variable to true
                
    
    #screen.blit(player2.player_img, player2.player_rect)   #draw the second player on the screen
    pygame.display.update()   #update the display