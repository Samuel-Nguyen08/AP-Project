#TODO animations
import pygame
import random as rand
import sys
# THIS GAME REQUIRES THE IMAGE FILES TO RUN


# Initialize pygame
pygame.init()


# Screen dimensions
screenwidth = 1280
screenheight = 720
bottompanel = 150


# Create the screen
screen_game = pygame.display.set_mode((screenwidth, screenheight))


# Name Screen
pygame.display.set_caption("Jimmy's Journey V0.98beta")


# Clock for controlling frame rate
clock = pygame.time.Clock()


# Font for rendering text
font = pygame.font.Font(None, 36)


# City Background
background_image = pygame.Surface((screenwidth, screenheight))
background_image = pygame.image.load("img/background.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (screenwidth, screenheight))


# Shop Background
shopbackground_image = pygame.Surface((screenwidth, screenheight))
shopbackground_image = pygame.image.load("img/shop.png").convert_alpha()
shopbackground_image = pygame.transform.scale(shopbackground_image, (screenwidth, screenheight))


# Battle Background
battle_background = pygame.Surface((screenwidth, screenheight))
battle_background = pygame.image.load("img/battle_background.png").convert_alpha()
battle_background = pygame.transform.scale(battle_background, (screenwidth, screenheight))

# Explore Background
explore_background = pygame.Surface((screenwidth, screenheight))
explore_background = pygame.image.load("img/explore_background.png").convert_alpha()
explore_background = pygame.transform.scale(explore_background, (screenwidth, screenheight))

# Defeat
defeat = pygame.Surface((screenwidth, screenheight))
defeat = pygame.image.load("img/Dead.png").convert_alpha()
defeat = pygame.transform.scale(defeat, (screenwidth, screenheight))


# Camp
camp = pygame.Surface((screenwidth, screenheight))
camp = pygame.image.load("img/Camp.png").convert_alpha()
camp = pygame.transform.scale(camp, (screenwidth, screenheight))


# Player image
jimmy_battle = pygame.Surface((screenwidth, screenheight))
jimmy_battle = pygame.image.load("img/jimmy_battle.png").convert_alpha()
jimmy_battle = pygame.transform.scale(jimmy_battle, (175, 175))

directions = ["down", "up", "right", "left"]
down_frames = []
up_frames = []
right_frames = []
left_frames = []

# Loop through each direction and load frames dynamically
for direction in directions:
    for i in range(3):  # Assuming 3 frames per animation
        img = pygame.image.load(f"img/Jimmy_{direction}/Jimmy_{i + 1}.png").convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        if direction == "down":
            down_frames.append(img)
        elif direction == "up":
            up_frames.append(img)
        elif direction == "right":
            right_frames.append(img)
        elif direction == "left":
            left_frames.append(img)
            
animations = {
    "right": right_frames,
    "left": left_frames,
    "up": up_frames,
    "down": down_frames
}

# Goblin Image
gobo = pygame.Surface((screenwidth, screenheight))
gobo = pygame.image.load("img/gobo.png").convert_alpha()
gobo = pygame.transform.scale(gobo, (100, 100))


# Cursor image
dagger_cursor = pygame.Surface((screenwidth, screenheight))
dagger_cursor = pygame.image.load("img/dagger_cursor.png").convert_alpha()
dagger_cursor = pygame.transform.scale(dagger_cursor, (35, 35))


# Battle Screen Panel
panel = pygame.Surface((screenwidth, screenheight))
panel = pygame.image.load("img/panel.png").convert_alpha()
panel = pygame.transform.scale(panel, (screenwidth, 150))


# Place Holders


placeholderwin = pygame.Surface((screenwidth, screenheight))
placeholderwin.fill("green")
placeholderpuzzle = pygame.Surface((screenwidth, screenheight))
placeholderpuzzle.fill("yellow")
placeholderempty = pygame.Surface((screenwidth, screenheight))
placeholderempty.fill("white")


# Global Variables
hpc = 100
atk = 100
hpp = 100
fps = 60
shop_stock = ["HP_CRYSTAL", "ATK_CRYSTAL", "HP_POTION"]
shop_prices = [hpc, atk, hpp]
inventory = []
puzzle = False
event_active = False
# Fuction for random events
def random_event(last_event):
    available_events = [0,1,2]
    if last_event is not None:
        if last_event in available_events:
            available_events.remove(last_event)
        return rand.choice(available_events)
    else:
        return rand.choice(available_events)
   
#create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen_game.blit(img, (x, y))




#function for drawing background
def draw_bg(background):
    screen_game.blit(background, (0, 0))




#Damage Text Class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp


    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen_game, "red", (self.x, self.y, 150, 20))
        pygame.draw.rect(screen_game, "green", (self.x, self.y, 150 * ratio, 20))


# Define Player Classe
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, name, max_hp, strength, potions, image, animations):
        super().__init__()
        # INIT VARIABLES ==================================================================
        self.money = 1500
        self.speed = 3
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.strength_buff_active = False
        # LOAD IMAGE ======================================================================
        self.battle_image = image
        self.rect = image.get_rect()
        self.rect.center = (x, y)
         # LOAD ANIMATIONS =================================================================
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.animations = animations
        self.direction = "down"
        self.current_frames = self.animations[self.direction]
        self.image = self.current_frames[self.frame_index]
        self.animation_cooldown = 100  # Time between frames in milliseconds
        self.rect = self.image.get_rect(topleft=(x, y))

    def idle(self):
        #set variables for attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
       
    def update(self, keys=None, battle = False):
        global last_event, event_active
        if keys is None:
            return battle
    
        if battle:
            # Use the static battle image
            self.image = self.battle_image
            if keys:
                if keys[pygame.K_b]:
                    self.strength_buff_active = True
                    print("Strength buff activated!")
                    animation_cooldown = 100
                    # Update animation frame when moving

        if not battle:
            #Reset movement flags
            dx, dy = 0, 0
            # Check for vertical movement conflicts (W and S)
            if keys[pygame.K_w] and keys[pygame.K_s]:
                dy = 0  # Cancel vertical movement if both W and S are pressed
            elif keys[pygame.K_w]:  # Move up
                dy = -self.speed
                self.direction = "up"
            elif keys[pygame.K_s]:  # Move down
                dy = self.speed
                self.direction = "down"
            # Check for horizontal movement conflicts (A and D)
            if keys[pygame.K_a] and keys[pygame.K_d]:
                dx = 0  # Cancel horizontal movement if both A and D are pressed
            elif dy == 0:  # Only allow horizontal movement if no vertical movement
                if keys[pygame.K_a]:  # Move left
                    dx = -self.speed
                    self.direction = "left"
                elif keys[pygame.K_d]:  # Move right
                    dx = self.speed
                    self.direction = "right"


            # Update animation frames only if moving
            if dx != 0 or dy != 0:
                self.current_frames = self.animations[self.direction]  # Update animation list
                if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    self.frame_index += 1
                    if self.frame_index >= len(self.current_frames):  # FIXED: Check the correct list
                        self.frame_index = 0
                    self.image = self.current_frames[self.frame_index]
            else:
                self.image = self.current_frames[0]  # Idle frame when not moving
            print(dx, dy)
            # Update position
            self.rect.x += dx
            self.rect.y += dy

            #transitions
            if self.rect.right >= screenwidth:
                self.rect.right = 0 + self.rect.width
            #Boundaries
            if self.rect.top < screenheight/3:
                self.rect.top = screenheight/3
            if self.rect.bottom > screenheight:
                self.rect.bottom = screenheight
            if self.rect.left < 0:
                self.rect.left = 0
            return battle
    
    def attack(self, target):
        #deal damage to enemy
        rand_dmg = rand.randint(-5, 5)
        temp_strength = self.strength  
        if self.strength_buff_active:
            temp_strength *= 5
        damage = temp_strength + rand_dmg
        target.hp -= damage
    #Check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), "red")
        damage_text_group.add(damage_text)


    def reset (self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.action = 0
        self.update_time = pygame.time.get_ticks()
   
    def draw(self):
        if self.hp > 0:
            screen_game.blit(self.image, self.rect)


def updateprice():
    global hpc, hpp, atk
    hpc = hpc + ((inventory.count("HP_CRYSTAL")) * 25)
    hpp = hpp + (inventory.count("HP_POTION") * 25)
    atk = atk + (inventory.count("ATK_CRYSTAL") * 25)


player = None
def game():
    global puzzle, last_event, player, event_active
    # Game states
    keys = pygame.key.get_pressed()
    running = True
    paused = False
    menu = False
    day = 0
    city = True
    shop = False
    shop2 = False
    gamba = False
    citymenu = False
    cityname_flag = False
    cityname_flag2 = False
    inventory_menu = False
    animationupdate = 0 
    shop_timer = 0
    puzzle = False
    last_event = None
    game_over = 0
    # Battle Variables
    battle = False
    current_fighter = 1
    total_fighters = 2
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    clicked = False
    gameover = 0


    # Battle Definitions
    jimmy = Player(450, 470, 'Jimmy', 50, 6, 3, jimmy_battle, animations)
    enemy1 = Player(800, 500, 'Enemy', 20, 6, 1, gobo, animations)
    enemy2 = Player(920, 500, 'Enemy', 20, 6, 1, gobo, animations)
    player = jimmy
   
    # Enemy List
    enemylist = []
    enemylist.append(enemy1)
    enemylist.append(enemy2)


    # Healthbars
    jimmyhealthbar = HealthBar(390, screenheight - bottompanel + 40, jimmy.hp, jimmy.max_hp)
    enemy1healthbar = HealthBar(800, screenheight - bottompanel + 40, enemy1.hp, enemy1.max_hp)
    enemy2healthbar = HealthBar(800, screenheight - bottompanel + 100, enemy2.hp, enemy2.max_hp)


    # function for drawing panel
    def draw_panel():
        # draw panel rectangle
        screen_game.blit((panel), (0, screenheight - bottompanel))
        #show jimmy stats
        draw_text(f'{jimmy.name} HP: {jimmy.hp}', font, "red", 390, screenheight - bottompanel + 10)
        for count, i in enumerate(enemylist):
            #show name and health
            draw_text(f'{i.name} HP: {i.hp}', font, "red", 800, (screenheight - bottompanel + 10) + count * 60)




    # Shop Font ===============================================================================
    shop_font = pygame.font.Font(None, 20)
    # PAUSE ==================================================================================
    mouse_y = 0  # Initialize mouse_y variable


    pause_overlay = pygame.Surface((screenwidth, screenheight))  # Semi-transparent overlay
    pause_overlay.set_alpha(128)  # Set transparency (0 = fully transparent, 255 = fully opaque)
    pause_overlay.fill("black")  # Fill with black color


    # Pause Text
    pause_text = font.render("Paused", True, "white")
    resume_text = font.render("Press ESC to Resume", True, "white")
    quit_text = font.render("Press Q to Quit", True, "white")


    # MENU ====================================================================================
    menu_overlay = pygame.Surface((screenwidth, screenheight))
    menu_overlay.set_alpha(200)
    menu_overlay.fill("black")


    # Menu Text
    day_text = font.render("Day: " + str(day), True, "white")
    explore_text = font.render("Explore", True, "white")
    explore_rect = explore_text.get_rect(center=((0 + (day_text.get_width()), screenheight - 75)))


    # CITY =====================================================================================


    city_t_overlay = pygame.Surface((screenwidth, screenheight))
    city_t_overlay.set_alpha(255)
    city_t_overlay.fill("black")


    city_b_overlay = pygame.Surface((screenwidth, screenheight))
    city_b_overlay.set_alpha(255)
    city_b_overlay.fill("black")


    # CITY =====================================================================================

    city_t_overlay = pygame.Surface((screenwidth, screenheight))
    city_t_overlay.set_alpha(255)
    city_t_overlay.fill("black")

    city_b_overlay = pygame.Surface((screenwidth, screenheight))
    city_b_overlay.set_alpha(255)
    city_b_overlay.fill("black")

    # City Text
    cityname_text = font.render("B'yeah town", True, "White")
    cityname_text.set_alpha(0)

    embark_text = font.render("Embark", True, "white")
    embark_rect = embark_text.get_rect(center=((50 + (day_text.get_width()), screenheight - 50)))

    # Inventory access menu                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    inventory_text = font.render("Inventory", True, "white")
    inventory_rect = inventory_text.get_rect(center=((screenwidth // 2, screenheight - 50)))
    inventory_layer = pygame.Surface((screenwidth, screenheight))
    inventory_layer.set_alpha(12)
    inventory_layer.fill("black")

    inventory_layer2 = pygame.Surface((screenwidth// 1.2 , screenheight // 1.2))
    inventory_layer2.set_alpha(255)
    inventory_layer2.fill("gray")

    exit_image = pygame.image.load("img/Exit_button.png").convert_alpha()
    exit_image = pygame.transform.scale(exit_image, (64, 64))
    exitinv_rect = exit_image.get_rect(center=((screenwidth // 2) + (inventory_layer2.get_width() // 2), (screenheight // 2) - (inventory_layer2.get_height() // 2)))

    # SHOP =====================================================================================

    shop_image = pygame.image.load("img/indicator.png").convert_alpha()
    shop_image = pygame.transform.scale(shop_image, (125, 125))
    shop_rect = shop_image.get_rect(center=(150,550))

    shop_keeper = pygame.image.load("img/shop_keeper.png").convert_alpha()
    shop_keeper = pygame.transform.scale(shop_keeper, (shop_keeper.get_width() * 2.5, shop_keeper.get_height() * 2.5))

    kiosk_image = pygame.image.load("img/kiosk.png").convert_alpha()
    kiosk_image = pygame.transform.scale(kiosk_image, (kiosk_image.get_width() * 2.5, kiosk_image.get_height() * 2.5))

    hpc_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
    hpc_buy_img = pygame.transform.scale(hpc_buy_img, (125, 125))
    hpc_price_text = shop_font.render(("Health Crystal: $" + str(hpc)), True, "White")
    hpc_buy = shop_image.get_rect(center=(140,525))

    atk_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
    atk_buy_img = pygame.transform.scale(atk_buy_img, (125,125))
    atk_price_text = shop_font.render(("Attack Crystal: $" + str(atk)), True, "White")
    atk_buy = atk_buy_img.get_rect(center=(400,525))

    hpp_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
    hpp_buy_img = pygame.transform.scale(hpp_buy_img, (125,125))
    hpp_price_text = shop_font.render(("Health Potion: $" + str(hpp)), True, "White")
    hpp_buy = hpp_buy_img.get_rect(center=(600,525))
    
    exitshop_rect = exit_image.get_rect(center=(screenwidth - (exit_image.get_width() // 2), 0 + (exit_image.get_height() // 2)))

    # SHOP 2 ======================================================================================

    shop2_image = pygame.image.load("img/indicator.png").convert_alpha()
    shop2_image = pygame.transform.scale(shop2_image, (125, 125))
    shop2_rect = shop2_image.get_rect(center=(1050, 500))

    # GAMBA ======================================================================================

    gamba_image = pygame.image.load("img/indicator.png").convert_alpha()
    gamba_image = pygame.transform.scale(gamba_image, (125, 125))
    gamba_rect = gamba_image.get_rect(center=(810, 550))


    # Create Instances =========================================================================

    all_sprites = pygame.sprite.Group(jimmy)
    
    updateprice()
    # Create Buying Mechanic
    def addtolist(item):
        global hpc, hpp, atk
        for player in all_sprites:
            updateprice()
            inventory.append(item)
            if item == "HP_CRYSTAL":
                if player.max_hp < 100:
                    player.max_hp = player.max_hp + 25
                    player.hp = player.hp + 25
                elif player.max_hp >= 100:
                    player.max_hp = player.max_hp + inventory.count("HP_CRYSTAL") * 25
                    player.hp = player.hp + inventory.count("HP_CRYSTAL") * 25
            if item == "ATK_CRYSTAL":
                if player.strength < 50:
                    player.strength = round(player.strength * 1.1)
                elif player.strength < 200:
                    player.strength = round(player.strength * 1.25)
            print(hpc, hpp, atk)
            updateprice()
            print(hpc, hpp, atk)
            print(player.max_hp, player.hp)

    def statsupdate():
        global stats_atk_text, stats_hp_text, healthbar, health_cap_bar
        for player in all_sprites:
            stats_hp_text = font.render(("Health: " + str(player.hp) + "/" + str(player.max_hp)), True, "white")
            stats_atk_text = font.render(("Strength: " + str(player.strength)), True, "white")
            health_cap_bar = pygame.Surface((100, 25))
            health_cap_bar.fill("black")
            healthbar = pygame.Surface(((100*(player.hp / player.max_hp)), 25))
            healthbar.fill("green")


    while running:
        keys = pygame.key.get_pressed() # Initialize keys
        # EVENT HANDLER ========================================================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Toggle pause state with Escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not menu and not city:
                    paused = not paused  # Toggle pause state
                if paused and event.key == pygame.K_q: # Quit the game if 'Q' is pressed while paused
                    running = False
                if event.key == pygame.K_BACKSPACE and not paused and not city and not shop and not inventory_menu:
                    menu = not menu
                if event.key == pygame.K_p:
                    player.hp = player.hp // 2
                    statsupdate()
            if city == False:
                if menu and explore_rect.collidepoint(pygame.mouse.get_pos()):
                    explore_text = font.render("Explore", True, "yellow")
                else:
                    explore_text = font.render("Explore", True, "white")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu and explore_rect.collidepoint(event.pos):  # Check if mouse click i s on the "Quit" button
                        menu = not menu
                        day += 1
            if city == True:
                if inventory_rect.collidepoint(pygame.mouse.get_pos()):
                    inventory_text = font.render("Inventory", True, "yellow")
                else:
                    inventory_text = font.render("Inventory", True, "white")
                if embark_rect.collidepoint(pygame.mouse.get_pos()):
                    embark_text = font.render("Embark", True, "yellow")
                else:
                    embark_text = font.render("Embark", True, "white")
                if shop_rect.collidepoint(pygame.mouse.get_pos()):
                    shop_image = pygame.image.load("img/indicator.png").convert_alpha()
                    shop_image = pygame.transform.scale(shop_image, (100, 100))
                    shop_image.set_alpha(100)
                else:
                    shop_image = pygame.image.load("img/indicator.png").convert_alpha()
                    shop_image = pygame.transform.scale(shop_image, (100, 100))
                    shop_image.set_alpha(0)
                if shop2_rect.collidepoint(pygame.mouse.get_pos()):
                    shop2_image = pygame.image.load("img/indicator.png").convert_alpha()
                    shop2_image = pygame.transform.scale(shop2_image, (100, 100))
                    shop2_image.set_alpha(100)
                else:
                    shop2_image = pygame.image.load("img/indicator.png").convert_alpha()
                    shop2_image = pygame.transform.scale(shop2_image, (100, 100))
                    shop2_image.set_alpha(0)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if embark_rect.collidepoint(event.pos):  # Check if mouse click is on the "Quit" button
                        for player in all_sprites:
                            player.rect.y = screenheight // 2
                            player.rect.x = screenwidth // 4
                        city = not city
                    if inventory_rect.collidepoint(event.pos):
                        inventory_menu = True
                        city = False
                        statsupdate()
                        print(inventory_menu)
                    if shop_rect.collidepoint(event.pos):
                        # set mouse position to the center of the screen
                        pygame.mouse.set_pos(screenwidth // 2, screenheight // 2)
                        # set flags
                        shop = True
                        city = False
                    if shop2_rect.collidepoint(event.pos):
                        # set mouse position to the center of the screen
                        pygame.mouse.set_pos(screenwidth // 2, screenheight // 2)
                        # set flags
                        shop2 = True
                        city = False
            elif inventory_menu:
                if exitinv_rect.collidepoint(pygame.mouse.get_pos()):
                    exit_image = pygame.image.load("img/Exit_button2.png").convert_alpha()
                    exit_image = pygame.transform.scale(exit_image, (64, 64))
                else:
                    exit_image = pygame.image.load("img/Exit_button.png").convert_alpha()
                    exit_image = pygame.transform.scale(exit_image, (64, 64))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exitinv_rect.collidepoint(event.pos):
                        inventory_menu = False
                        city = True            
            elif shop == True:
                if shop_timer > 0:
                    pass
                else:
                    if exitshop_rect.collidepoint(pygame.mouse.get_pos()):
                        exit_image = pygame.image.load("img/Exit_button2.png").convert_alpha()
                        exit_image = pygame.transform.scale(exit_image, (64, 64))
                    else:
                        exit_image = pygame.image.load("img/Exit_button.png").convert_alpha()
                        exit_image = pygame.transform.scale(exit_image, (64, 64))
                    if hpc_buy.collidepoint(pygame.mouse.get_pos()):
                        hpc_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
                        hpc_buy_img = pygame.transform.scale(hpc_buy_img, (100, 100))
                        hpc_buy_img.set_alpha(255)
                    else:
                        hpc_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
                        hpc_buy_img = pygame.transform.scale(hpc_buy_img, (100, 100))
                        hpc_buy_img.set_alpha(0)
                    if atk_buy.collidepoint(pygame.mouse.get_pos()):
                        atk_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
                        atk_buy_img = pygame.transform.scale(atk_buy_img, (100, 100))
                        atk_buy_img.set_alpha(255)
                    else:
                        atk_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
                        atk_buy_img = pygame.transform.scale(atk_buy_img, (100, 100))
                        atk_buy_img.set_alpha(0)
                    if hpp_buy.collidepoint(pygame.mouse.get_pos()):
                        hpp_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
                        hpp_buy_img = pygame.transform.scale(hpp_buy_img, (100, 100))
                        hpp_buy_img.set_alpha(255)
                    else:
                        hpp_buy_img = pygame.image.load("img/indicator.png").convert_alpha()
                        hpp_buy_img = pygame.transform.scale(hpp_buy_img, (100, 100))
                        hpp_buy_img.set_alpha(0)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if exitshop_rect.collidepoint(event.pos):
                            shop = False
                            city = True
                        if atk_buy.collidepoint(event.pos):
                            if player.money >= atk:
                                player.money -= atk
                                addtolist("ATK_CRYSTAL")
                                atk_price_text = shop_font.render(("Attack Crystal: $" + str(atk)), True, "White")
                                print(str(atk), "ATK")
                                print(player.money)
                        if hpc_buy.collidepoint(event.pos):
                            if player.money >= hpc:
                                player.money -= hpc
                                addtolist("HP_CRYSTAL")
                                hpc_price_text = shop_font.render(("Health Crystal: $" + str(hpc)), True, "White")
                                print(str(hpc), "HPC")
                                print(player.money)

                        if hpp_buy.collidepoint(event.pos):
                            if player.money >= hpp:
                                player.money -= hpp
                                addtolist("HP_POTION")
                                hpp_price_text = shop_font.render(("Health Potion: $" + str(hpp)), True, "White")
                                print(str(hpp), "HPP")
                                print(player.money)
                            
        # Decrement the shop timer if it's active
        if shop_timer > 0:
            shop_timer -= 1

        # ======================================================================================================================    
        if battle:
            # draw background
            draw_bg(battle_background)


            # draw panel
            draw_panel()
            jimmyhealthbar.draw(jimmy.hp)
            enemy1healthbar.draw(enemy1.hp)
            enemy2healthbar.draw(enemy2.hp)


            # draw jimmy and enemies
            jimmy.draw()
            for enemy in enemylist:
                enemy.draw()


            # draw the damage text
            damage_text_group.update()
            damage_text_group.draw(screen_game)


            # Reset Actions
            attack = False
            target = None
            mousehidden = False
            any_enemy_hovered = False


            # Change Cursor to sword when hovered over an enemy
            pos = pygame.mouse.get_pos()
            for count, enemy in enumerate(enemylist):
                if enemy.rect.collidepoint(pos):
                    any_enemy_hovered = True  
                    screen_game.blit(dagger_cursor, pos)
                    if clicked == True and enemy.alive == True:
                        attack = True
                        target = enemylist[count]
           
            if enemy1.hp <= 0:
                enemy1.kill()
           
            if any_enemy_hovered and not mousehidden:
                pygame.mouse.set_visible(False)
                mouse_hidden = True
            if any_enemy_hovered == False:
                pygame.mouse.set_visible(True)
                mouse_hidden = False


            # Player Action
            if gameover == 0:
                if jimmy.alive == True:
                    if current_fighter == 1:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            if attack == True and target != None:
                                jimmy.attack(target)
                                current_fighter += 1
                                action_cooldown = 0
                else:
                    game_over = -1


                # Enemy Action
                for count, enemy in enumerate(enemylist):
                    if current_fighter == 2 + count:
                        if enemy.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                damage_text = DamageText(enemy.rect.centerx, enemy.rect.y)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                            else:
                                enemy.attack(jimmy)
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1
                if current_fighter > total_fighters:
                    current_fighter = 1
            alive_enemies = 0
            for enemy in enemylist:
                if enemy.alive == True:
                    alive_enemies += 1
            if alive_enemies == 0:
                game_over = 1


            # Battle Endings
            if game_over != 0:
                if game_over == 1:
                    screen_game.blit(placeholderwin, (0, 0))
                if game_over == -1:
                    screen_game.blit(defeat, (0, 0))
            # Detect Player Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        if puzzle:
            screen_game.blit(placeholderpuzzle, (0, 0))
            if keys[pygame.K_p]: #press p to turn off puzzle event.
                puzzle = False
                event_active = False
                last_event = None
       
        if event_active == False:
            if not paused or city or menu or shop or shop2 or battle:
                battle = player.update(keys, battle)
        else:
            if battle == False and puzzle == False:
                event_active = False
                last_event = None


        # Get pressed keys
        keys = pygame.key.get_pressed()  
        # Update player
        if not paused or city or menu or shop or shop2 or battle or inventory_menu:
            battle = player.update(keys, battle)
        if menu and not paused:
            # Draw the menu
            screen_game.blit(shopbackground_image, (0, 0))
            all_sprites.draw(screen_game)
            screen_game.blit(menu_overlay, (0, 0))


            # Text
            screen_game.blit(day_text, (0 + (day_text.get_width() // 2), 0 + 25))
            screen_game.blit(explore_text, explore_rect)


            # Flip display
            pygame.display.flip()
           
            # Cap framerate
            clock.tick(60)
            continue
        if paused and not menu:
            # Draw the game screen
            screen_game.blit(shopbackground_image, (0, 0))
            all_sprites.draw(screen_game)


            # Draw the pause overlay
            screen_game.blit(pause_overlay, (0, 0))


            # Draw pause text
            screen_game.blit(pause_text, (screenwidth // 2 - pause_text.get_width() // 2, screenheight // 2 - 50))
            screen_game.blit(resume_text, (screenwidth // 2 - resume_text.get_width() // 2, screenheight // 2))
            screen_game.blit(quit_text, (screenwidth // 2 - quit_text.get_width() // 2, screenheight // 2 + 50))


            # Flip the display
            pygame.display.flip()


            # Cap the frame rate
            clock.tick(60)
            continue  # Skip the rest of the loop while paused
       
        if not city and not shop and not battle and not inventory_menu and not shop2:
            screen_game.blit(explore_background, (0, 0))
            all_sprites.draw(screen_game)
           
            # Flip display
            pygame.display.flip()


            # Cap framerate
            clock.tick(60)
            continue
       
        if city:
            # record mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y > screenheight - 100:
                citymenu = True
            elif mouse_y < screenheight - 100:
                citymenu = False
            screen_game.blit(background_image, (0,0))
            screen_game.blit(cityname_text, (((screenwidth // 2) - (cityname_text.get_width() // 2)), (((screenheight // 2)))))

            # Text
            if not cityname_flag:
                if cityname_text.get_alpha() > 0 and cityname_flag2 == False:
                    cityname_text.set_alpha(0)
                    cityname_flag2 = True
                if cityname_text.get_alpha() < 255:
                    cityname_text.set_alpha(cityname_text.get_alpha() + 3)
                    pygame.time.delay(5)  # Add a small delay to control the speed of the fade-in effect
                    if cityname_text.get_alpha() == 255:
                        pygame.time.delay(1000)
                        cityname_flag = True
                        

            if cityname_flag:
                if cityname_text.get_alpha() > 0:
                    cityname_text.set_alpha(cityname_text.get_alpha() - 3)
                    pygame.time.delay(5)
                screen_game.blit(shop_image, shop_rect)
                screen_game.blit(shop2_image, shop2_rect)
                # pop up menu
                if citymenu:
                    if animationupdate == 0:
                        screen_game.blit(city_b_overlay,  (0, screenheight))
                    if animationupdate < 100:
                        screen_game.blit(city_b_overlay, (0, screenheight - animationupdate))
                        animationupdate += 5
                        pygame.time.delay(5)
                        pygame.display.update()
                    if animationupdate >= 100:
                        screen_game.blit(city_b_overlay, (0, screenheight - animationupdate))
                        screen_game.blit(embark_text, embark_rect)
                        screen_game.blit(inventory_text, inventory_rect)
                elif not citymenu:
                    if animationupdate > 0:
                        screen_game.blit(city_b_overlay, (0, screenheight - animationupdate))
                        animationupdate -= 5
                        pygame.time.delay(5)
                        pygame.display.update()

            #Flip display
            pygame.display.flip()


            clock.tick(60)
            continue

        if inventory_menu:
            screen_game.blit(cityname_text, (((screenwidth // 2) - (cityname_text.get_width() // 2)), (((screenheight // 2)))))
            screen_game.blit(inventory_layer2, ((screenwidth // 2) - (inventory_layer2.get_width() // 2), (screenheight // 2) - (inventory_layer2.get_height() // 2)))
            screen_game.blit(inventory_layer, (0, 0))
            screen_game.blit(health_cap_bar, ((screenwidth // 2) - (inventory_layer2.get_width() // 2) + 25, screenheight // 2 - 75))
            screen_game.blit(healthbar, ((screenwidth // 2) - (inventory_layer2.get_width() // 2) + 25, screenheight // 2 - 75))
            screen_game.blit(stats_hp_text, ((screenwidth // 2) - (inventory_layer2.get_width() // 2) + 25, screenheight // 2 - 50))
            screen_game.blit(stats_atk_text, ((screenwidth // 2) - (inventory_layer2.get_width() // 2) + 25, screenheight // 2 - 25))
            screen_game.blit(exit_image, exitinv_rect)
             
            #Flip display
            pygame.display.flip()


            clock.tick(60)
            continue



        if shop:
            screen_game.blit(shopbackground_image, (0,0))
            screen_game.blit(shop_keeper, (screenwidth - shop_keeper.get_width(), screenheight - (shop_keeper.get_height() + 75)))
            screen_game.blit(kiosk_image, (screenwidth - kiosk_image.get_width(), screenheight - kiosk_image.get_height()))
            screen_game.blit(hpc_price_text, ((190 - hpc_price_text.get_width()), screenheight - 75))
            screen_game.blit(hpc_buy_img, hpc_buy)
            screen_game.blit(atk_price_text, ((420 - atk_price_text.get_width(), screenheight - 75)))
            screen_game.blit(atk_buy_img, atk_buy)
            screen_game.blit(hpp_price_text, ((650 - hpp_price_text.get_width(), screenheight - 100)))
            screen_game.blit(hpp_buy_img, hpp_buy)
            screen_game.blit(exit_image, exitshop_rect)

            pygame.display.flip()
            clock.tick(60)
            continue
        
        if shop2:
            screen_game.blit(shopbackground_image, (0,0))

            pygame.display.flip()
            clock.tick(60)
            continue

        # Flip the display
        pygame.display.flip()


        # Cap the frame rate
        clock.tick(60)


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()

# this is a test comment