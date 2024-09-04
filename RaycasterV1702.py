def boot(ScreenSizePlayerSpeed):
    import pygame
    from pygame import font
    import math
    import random
    import gc
    import MainMenuIteration11
    from urllib.request import urlopen
    import io
    pygame.init()
    ###notes/to do list
    #to get the sprites behind the walls we need to either:
    #1. make the blocks inside render after, and the blocks on the outside of the map render first. and the enemy between them
    # we could rename the border as for example 9(still use the texture for 1) and make 9s render first, then enemy, then 1s and 2
    #2. or we rewrite the rendering of the enemy to make it render if their isnt a wall blocking the visibility of its position.

    #ah
    #,.,.,,,,..,..


    #02/09/2023
    #these enemies are becoming a problem✔
    #you should have fixed them before doing more work✔
    #its really boring and i dont know where to start✔

    #bonus note for today
    #original distortion effect found in original iterations was due to limits being placed
    #either worng limits or limits in general
    #fun
    #change the sky to match the floor !!✔
    #clean up code soon its annoying and difficult
    #fix map generation ✔

    # killed numpy
    #numpy survived?



    #create a surface in corner
    #draw map to that surface
    #done??


    ScreenSizePlayerSpeed=ScreenSizePlayerSpeed
    width, height, SpeedMultiplier= ScreenSizePlayerSpeed
    screen = pygame.display.set_mode((width, height))

    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]",
             "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
             "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"
    ]

    progressbar=("")
    progresscount=0
    
    
        
    #image load function via github repository - implemented to save storage/ease of access
    def load_image_from_url(url):
        img_str = urlopen(url).read()
        img_file = io.BytesIO(img_str)
        img = pygame.image.load(img_file).convert_alpha()
        return img
    
    # Textures
    textures = {
        '1': load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/images/walls/1.png?raw=true"),
        '2': load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/images/walls/2.png?raw=true")
    }

    print("textures loaded  1/5")
    
    progressbar = ("\rwaiting.... " + animation[0])
    print(progressbar)
    progresscount+=1
    introhelmetimages = []
    for num in range(0, 20):
        img = load_image_from_url(f"https://github.com/Brown1ie/Python-Raycast/blob/main/images/helmet/{num}.png?raw=true")
        img = pygame.transform.scale(img, (width, height)).convert_alpha()
        introhelmetimages.append(img)

    print("helmet loaded 2/5")

    progressbar = ("\rwaiting.... " + animation[2])
    print(progressbar)

    progresscount+=2

    enemy_images = [
            load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/images/skull/0.png?raw=true"),
            load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/images/skull/1.png?raw=true"),
        ]


    targetimage=load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/images/skull/0.png?raw=true")
    targetimage=pygame.transform.scale(targetimage, (44,52))
    print("Enemy images loaded 3/5")


    progressbar = ("\rwaiting.... " + animation[4])
    print(progressbar)

    progresscount+=2

    hammer_images = []
    for num in range(14):
        img = load_image_from_url(f"https://github.com/Brown1ie/Python-Raycast/blob/main/images/hammer/{num}.png?raw=true")
        img = pygame.transform.scale(img, (width, height)).convert_alpha()
        hammer_images.append(img)
    for num in range(14, -1, -1):
        img = load_image_from_url(f"https://github.com/Brown1ie/Python-Raycast/blob/main/images/hammer/{num}.png?raw=true")
        img = pygame.transform.scale(img, (width, height)).convert_alpha()
        hammer_images.append(img)

    hammer_idle=load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/IDLE.png?raw=true")

    print("loaded hammer images 4/5")

    progressbar = ("\rwaiting.... " + animation[6])
    print(progressbar)

    progresscount+=2

    # Preload images for Sword class
    sword_swing_images = []
    sword_draw_images = []
    for num in range(0, 13):
        swing_img = load_image_from_url(f"https://github.com/Brown1ie/Python-Raycast/blob/main/images/sword/strike/{num}.png?raw=true")
        swing_img = pygame.transform.scale(swing_img, (width, height)).convert_alpha()
        sword_swing_images.append(swing_img)

    for num in range(0, 18):
        draw_img = load_image_from_url(f"https://github.com/Brown1ie/Python-Raycast/blob/main/images/sword/draw/{num}.png?raw=true")
        draw_img = pygame.transform.scale(draw_img, (width, height)).convert_alpha()
        sword_draw_images.append(draw_img)

    sword_idle=load_image_from_url("https://github.com/Brown1ie/Python-Raycast/blob/main/images/sword/IDLESword.png?raw=true")


    print("loaded sword images 5/5")

    progressbar = ("\rwaiting.... " + animation[8])
    print(progressbar)
    progresscount+=2

    def main():
        
        world_map = []
        # Read automap data from file
        with open("automap") as f:
            world_map = f.read().split("\n")

        # Determine the maximum row length
        max_row_length = max(len(row) for row in world_map)
        #print(max_row_length)
        # Pad the shorter rows to make them equal in length

        #old - revert to if breaks
        #padded_world_map = [row.ljust(max_row_length, '0') for row in world_map]

        # Convert padded_world_map to a list of lists
        #world_map = [list(row) for row in padded_world_map]

        #old - end

        #new

        # Convert padded_world_map to a list of lists
        world_map = [list(row) for row in world_map]

        
        #print(world_map)

        # Initialize Pygame
        pygame.init()

        # Set up the display
        #test values
        width, height = 800, 600
        width, height, SpeedMultiplier= ScreenSizePlayerSpeed
        screen = pygame.display.set_mode((width, height))
        
        

        try:
            dmfont = "dmfont.ttf"
            CustomFont=pygame.font.Font(dmfont, 12)
        except:
            dmfont = None
            CustomFont=pygame.font.Font(None,24)


        





        #enemy_sprite = pygame.image.load("enemyMid.png").convert_alpha()
        #enemy_sprite = pygame.transform.smoothscale_by(enemy_sprite, 0.5).convert_alpha()

        

        
        
        #define hammer variable
        max_uses = 5
        
        numberofenemies = 10
        
        
    #gun images
    ##    MP7ReloadImages = []
    ##    for num in range(0, 40):
    ##        img = pygame.image.load(f"MP7\\Reload\\{num}.png").convert_alpha()
    ##        img = pygame.transform.scale(img, (width // 4 * 3, height // 4 * 3)).convert_alpha()
    ##        MP7ReloadImages.append(img)
    ##
    ##    MP7ShootImages = []
    ##    for num in range(0, 2):
    ##        img = pygame.image.load(f"MP7\\Shoot\\{num}.png").convert_alpha()
    ##        img = pygame.transform.scale(img, (width // 4 * 3 , height // 4 * 3 )).convert_alpha()
    ##        MP7ShootImages.append(img)
    ##
    ##
    ##    PistolReloadImages = []
    ##    for num in range(0, 1):
    ##        img = pygame.image.load(f"Pistol\\Reload\\{num}.png").convert_alpha()
    ##        img = pygame.transform.scale_by(img, 1.5).convert_alpha()
    ##        PistolReloadImages.append(img)
    ##
    ##    PistolShootImages = []
    ##    for num in range(0, 7):
    ##        img = pygame.image.load(f"Pistol\\Shoot\\{num}.png").convert_alpha()
    ##        img = pygame.transform.scale_by(img, 1.5).convert_alpha()
    ##        PistolShootImages.append(img)
    ##
    ##
    ##    ShotgunReloadImages = []
    ##    for num in range(0,1):
    ##        img = pygame.image.load(f"Classic Shotgun\\Reload\\{num}.png").convert_alpha()
    ##        img = pygame.transform.scale_by(img, 0.25).convert_alpha()
    ##        ShotgunReloadImages.append(img)
    ##
    ##    ShotgunShootImages = []
    ##    for num in range(0, 7):
    ##        img = pygame.image.load(f"Classic Shotgun\\Shoot\\{num}.png").convert_alpha()
    ##        img = pygame.transform.scale_by(img, 0.25).convert_alpha()
    ##        ShotgunShootImages.append(img)
    ##
    ##    
    ##    
    ##    MP7icon = pygame.image.load("MP7\\MP7Icon.png").convert_alpha()
    ##
    ##    #find better pistol icon
    ##    Pistolicon = pygame.image.load("Pistol\\Pistolicon.png").convert_alpha()
    ##    
    ##    Shotgunicon = pygame.image.load("Classic Shotgun\\shotgunicon.png").convert_alpha()

    ##    shooting= False
    #gun images end

        # Player variables
        player_pos = [1.5, 1.5]
        player_dir = [1.0, 0.0]
        player_plane = [0.0, 0.66]


        vertical_angle = 0.0

        # Mouse sensitivity
        mouse_sensitivity = 0.02

        # Movement speed
        move_speed = 0.05  #start value

        move_speed = move_speed * SpeedMultiplier 

        print("Width",width,"Height",height, "Player Speed=",move_speed)

        vertical_angle = 0.0 #this is here twice? 
        vertical_range = math.pi / 2

        animation_speed = 80  # milliseconds

        weaponselect = 1
        Introlast_image_change_time = pygame.time.get_ticks()
        introstart = True
        Hindex = 0
        SwordIndex=0
        GREY = [128, 128, 128]
        GREEN = [0,255,0]
        RED = [255, 0, 0]
        BLUE = [102,255,255]
        WHITE=[255,255,255]

        print("basic variables assigned")
        
        if width == 600:
            radius = 40
        if width == 800:
            radius = 60
        if width == 1000:
            radius = 80

        minimap_background = pygame.Surface((radius * 2, radius * 2))

        minimap_background.fill(RED)

        minimap_border = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
        minimap_border.fill(BLUE)

        minimap_background_loc=(width - (radius * 2)- 35, height // 12 )
        minimap_border_loc=(width - (radius * 2)- 40, height // 12 - 5)

        print("minimap loaded")
        
        time_elapsed = 0
    ##    with open("leaderboard",encoding="cp437", errors='ignore') as f:
    ##        leaderboard = f.read()
    ##        print(leaderboard)
    ##        f.close()
        with open("leaderboard", "r+") as f:
            highscore = int(f.read())
        best_time=highscore

        print("leaderboard downloaded")
        end_buttons=False
        button_width = 125
        button_height = 50
        class Button(pygame.sprite.Sprite):
            def __init__(self, x, start_y, target_pos, text):
                super().__init__()

                self.rect = pygame.Rect(x - button_width // 2, start_y, button_width, button_height)
                self.start_y = start_y
                self.speed = 5  # Falling speed
                self.target_pos = target_pos
                self.text = text
                self.rect_color = RED  # Added attribute

                all_sprites.add(self)
                buttongroup.add(self)

            def check_click(self, mouse_pos):
                if self.rect.collidepoint(mouse_pos):
                    print("Button clicked:", self.text)
                    if self.text == "Replay":
                        print("Reloading..")
                        
                        pygame.quit()
                        
                        boot(ScreenSizePlayerSpeed)
                    if self.text == "Exit":
                        print("Exiting..")
                        pygame.quit()

            def check_hover(self, mouse_pos):
                if self.rect.collidepoint(mouse_pos):
                    self.rect_color = GREEN
                else:
                    self.rect_color = RED

            def update(self):
                if self.rect.y < self.target_pos[1]:
                    self.rect.y += self.speed

            def draw_text(self):
                text_surface = CustomFont.render(self.text, True, WHITE)
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)

        buttongroup = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        exit_button = Button(width - 100 , 50, (width - 100, 50), "Exit")
        replay_button = Button(100 , 50, (100, 50), "Replay")


        def DrawAutoMap():   # make this more tidy its not tidy
            global player_map_pos
            square_size = 20
            outline_thickness = 2
            PURPLE = (155, 0, 255)
            WHITE = (255, 255, 255)
            GREEN= (0,255,0)

            screen.blit(minimap_border, (minimap_border_loc))
            screen.blit(minimap_background, (minimap_background_loc))
            
            minimap_background.fill(RED)

            # Calculate the offset to center the player on the minimap
            offset_x = int(player_pos[0] * square_size - radius) 
            offset_y = int(player_pos[1] * square_size - radius) 
            #print(offset_x, offset_y)
            for j, row in enumerate(world_map):
                for i, value in enumerate(row):
                    x = i * square_size - offset_x 
                    y = j * square_size - offset_y 
                    #print(x, y)

                    if value == "1":
                        pygame.draw.rect(minimap_background, WHITE, (x  , y , square_size, square_size), outline_thickness)
                    elif value == "2":
                        pygame.draw.rect(minimap_background, GREEN, (x, y , square_size, square_size), outline_thickness)
                    elif value == "0":
                        pygame.draw.rect(minimap_background, (0, 0, 0), (x  , y  , square_size, square_size), outline_thickness)

            # Player location
            
            player_map_pos_x = radius
            player_map_pos_y = radius
            pygame.draw.circle(minimap_background, PURPLE, (player_map_pos_x , player_map_pos_y ), square_size // 4)

            
        def display_coordinates(screen, player_pos):
            coordinates_font = pygame.font.Font(None, 24)  # You can adjust the font size if needed
            
            coordinates_text = f"Coordinates: ({player_pos[0]:.2f}, {player_pos[1]:.2f})"
            coordinates_surface = CustomFont.render(coordinates_text, True, (255, 255, 255))  # White color
            screen.blit(coordinates_surface, (10, 10))  # Render the text at the specified position

            
            uses_text = f"Hammer Uses: {hammer.current_uses}/{hammer.max_uses}"
            text_surface = CustomFont.render(uses_text, True, (255, 255, 255))
            screen.blit(text_surface, (10,30))

            objective_text=("Eliminate all:")
            objective_surface = CustomFont.render(objective_text, True, (255, 255, 255))
            screen.blit(objective_surface, (width // 2 - 85, 20))
            
            screen.blit(targetimage,(width // 2 + 25, 0))

            skullsremaining_text=f"{numberofenemies}          remaining"
            skull_surface = CustomFont.render(skullsremaining_text, True, (255, 255, 255))
            screen.blit(skull_surface, (width // 2 -70, 50))

            screen.blit(targetimage,(width // 2 - 62, 30))

            time_elapsed_text=f"{time_elapsed}   seconds"
            time_elapsed_surface = CustomFont.render(time_elapsed_text, True, (255, 255, 255))
            screen.blit(time_elapsed_surface, (width // 2 - 70, 80))


            best_time_text=f"High score:{best_time}   seconds"
            best_time_surface = CustomFont.render(best_time_text, True, (255, 255, 255))
            screen.blit(best_time_surface, (10, 60))

        def raycast(screen, player_pos, player_dir, player_plane, world_map, textures, width, height, column_width):
            #if it ever woks properly rename this to raycast and sprite render


            # Create a list to store rendering information
            rendering_data = []  

            for x in range(width):
                # Calculate the ray's direction and starting position
                camera_x = 2 * x / width - 1
                ray_dir_x = player_dir[0] + player_plane[0] * camera_x
                ray_dir_y = player_dir[1] + player_plane[1] * camera_x

                map_x, map_y = int(player_pos[0]), int(player_pos[1])

                delta_dist_x = abs(1 / (ray_dir_x + 1e-10))
                delta_dist_y = abs(1 / (ray_dir_y + 1e-10))

                side = None

                # Determine the step direction and initial side distances
                step_x = 1 if ray_dir_x >= 0 else -1
                step_y = 1 if ray_dir_y >= 0 else -1

                if ray_dir_x < 0:
                    side_dist_x = (player_pos[0] - map_x) * delta_dist_x
                else:
                    side_dist_x = (map_x + 1.0 - player_pos[0]) * delta_dist_x

                if ray_dir_y < 0:
                    side_dist_y = (player_pos[1] - map_y) * delta_dist_y
                else:
                    side_dist_y = (map_y + 1.0 - player_pos[1]) * delta_dist_y

                hit = False
                while not hit:
                    # Perform DDA (Digital Differential Analyzer) algorithm
                    if side_dist_x < side_dist_y:
                        side_dist_x += delta_dist_x
                        map_x += step_x
                        side = 0
                    else:
                        side_dist_y += delta_dist_y
                        map_y += step_y
                        side = 1

                    # Check for collisions with walls
                    if map_x < 0 or map_x >= len(world_map[0]) or map_y < 0 or map_y >= len(world_map):
                        break

                    if world_map[map_y][map_x] != '0':
                        hit = True

                # Calculate the perpendicular wall distance and line height
                if side == 0:
                    perp_wall_dist = abs((map_x - player_pos[0] + (1 - step_x) / 2) / ray_dir_x)
                else:
                    perp_wall_dist = abs((map_y - player_pos[1] + (1 - step_y) / 2) / ray_dir_y)

                line_height = int(height / perp_wall_dist)

                # Calculate drawing start and end positions
                draw_start = int(-line_height / 2 + height / 2 + height * vertical_angle / vertical_range)
                draw_end = int(line_height / 2 + height / 2 + height * vertical_angle / vertical_range)

                wall_texture = textures[world_map[map_y][map_x]]

                # Calculate the texture coordinates and scale the texture column
                wall_x = player_pos[1] + perp_wall_dist * ray_dir_y if side == 0 else player_pos[0] + perp_wall_dist * ray_dir_x
                wall_x -= math.floor(wall_x)

                tex_x = int(wall_x * wall_texture.get_width())
                if side == 0 and ray_dir_x > 0:
                    tex_x = wall_texture.get_width() - tex_x - 1
                if side == 1 and ray_dir_y < 0:
                    tex_x = wall_texture.get_width() - tex_x - 1

                wall_height = draw_end - draw_start
                tex_column = pygame.transform.scale(
                    wall_texture.subsurface((tex_x, 0, 1, wall_texture.get_height())),
                    (column_width, wall_height))

                # Store rendering information in the list
                rendering_data.append({
                    'type' : 'wall',
                    'draw_start': draw_start,
                    'draw_end': draw_end,
                    'tex_column': tex_column,
                    'x': x
                })

            return rendering_data

    ##         # Add enemy data to rendering_data
    ##        for enemy in enemies:
    ##            delta_x = enemy.pos_x - player_pos[0]
    ##            delta_y = enemy.pos_y - player_pos[1]
    ##
    ##            distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    ##            angle = math.atan2(delta_y, delta_x) - math.atan2(player_dir[1], player_dir[0])
    ##
    ##            if angle < -math.pi:
    ##                angle += 2 * math.pi
    ##            elif angle >= math.pi:
    ##                angle -= 2 * math.pi
    ##
    ##            if -math.pi / 3 <= angle <= math.pi / 3:
    ##                enemy_height = (height) / distance
    ##                view_angle = math.atan2(player_dir[1], player_dir[0])
    ##                enemy_angle = angle + view_angle
    ##                screen_x = int(round((enemy_angle / (math.pi / 4)) * (width / 2))) + (width // 2)
    ##                vertical_screen_offset = (height / 2) * math.tan(vertical_angle)
    ##                screen_y = int(round((height - enemy_height) / 2 + vertical_screen_offset))
    ##
    ##                enemy_sprite_scaled = pygame.transform.scale(enemy_sprite, (int(enemy_height), int(enemy_height)))
    ##
    ##                sprite_x = enemy.pos_x - player_pos[0]
    ##                sprite_y = enemy.pos_y - player_pos[1]
    ##                inv_det = 1.0 / (player_plane[0] * player_dir[1] - player_dir[0] * player_plane[1])
    ##                transform_x = inv_det * (player_dir[1] * sprite_x - player_dir[0] * sprite_y)
    ##                transform_y = inv_det * (-player_plane[1] * sprite_x + player_plane[0] * sprite_y)
    ##
    ##                sprite_screen_x = int((width / 2) * (1 + transform_x / transform_y))
    ##                sprite_screen_y = screen_y
    ##
    ##                rendering_data.append({
    ##                    'type': 'enemy',
    ##                    'draw_start': sprite_screen_y,
    ##                    'draw_end': sprite_screen_y + enemy_height,
    ##                    'tex_column': enemy_sprite_scaled,
    ##                    'x': sprite_screen_x
    ##                })
    ##
    ##        # Sort the rendering_data list based on descending order of draw_end
    ##        rendering_data.sort(key=lambda data: data['draw_end'], reverse=False)
    ##
    ##        # Draw the elements in the sorted order
    ##        for data in rendering_data:
    ##            if data['type'] == 'wall':
    ##                x = data['x']
    ##                draw_start = data['draw_start']
    ##                tex_column = data['tex_column']
    ##                screen.blit(tex_column, (x * column_width, draw_start))
    ##            elif data['type'] == 'enemy':
    ##                draw_start = data['draw_start']
    ##                draw_end = data['draw_end']
    ##                tex_column = data['tex_column']
    ##                x = data['x']
    ##                screen.blit(tex_column, (x, draw_start))
    #Too many lines
                
        
            

        def helmet_animation():
            nonlocal Hindex, Introlast_image_change_time

            current_time = pygame.time.get_ticks()  # Gets new fps
            if current_time - Introlast_image_change_time >= animation_speed:
                Hindex += 1  # Cycles next image
                if Hindex == 20:  # If at the final image
                    # Sets to False to stop the animation from continuing
                    # This makes it stay blitting the final image
                    Hindex = 19
                    for i in range(19):
                        if introhelmetimages[i] is not None:
                            introhelmetimages[i] = None
                            gc.collect()#deletes old images from memory - does this actually work????
                Introlast_image_change_time = current_time

            screen.blit(introhelmetimages[Hindex], (0, 0))
            
                

        # AnimationLogic class
        class AnimationLogic:
            def __init__(self, images, animation_speed):
                self.images = images
                self.animation_speed = animation_speed
                self.last_image_change_time = 0
                self.index = 0
                self.running = False

            def start_animation(self):
                self.running = True

            def stop_animation(self):
                self.running = False

            def update_animation(self):
                if not self.running:
                    return

                current_time = pygame.time.get_ticks()
                if current_time - self.last_image_change_time >= self.animation_speed:
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                        self.stop_animation()
                    self.last_image_change_time = current_time

            def render(self, screen, position):
                if self.running:
                    screen.blit(self.images[self.index], position)
                else:
                    screen.blit(self.images[0], position)


        #issue  with enemy its drawing from top left corner  , so xpos is the edge of image not middle
        class Enemy:    #we need to cast a line at all time from player to enemy, if it doesnt collide with aything on the wya render enemy , if it collides with anything dont render. THis sounds simple its almost the inverse of the rc algorithm but why doesnt it work
            def __init__(self, pos_x, pos_y, images):
                self.pos_x = pos_x 
                self.pos_y = pos_y
                self.health = 20
                self.images = images  # Store the enemy images
                self.image_index = 0  # Initial index of the current enemy image
                self.image_timer = 0  # Timer to control image switching
        def spawn_enemies():

           
            enemies=[]
            for n in range(numberofenemies):
                
                locx,locy = random.choice(walkable_coordinates)
                locx-=0.5
                locy-=0.5
                if locx > max_row_length:
                    locx,locy = random.choice(walkable_coordinates)
                    print("Relocating enemy to valid location...")
                if locx < 1:
                    locx,locy = random.choice(walkable_coordinates)
                    print("Relocating enemy to valid location...")
                if locy < 2:
                    locx,locy = random.choice(walkable_coordinates)
                    print("Relocating enemy to valid location...")
                #Creates a list of enemy instances at specific positions
                enemies.append(Enemy(locx , locy,enemy_images))
                    #Enemy(8.0, 4.0,enemy_images),
                    #Enemy(2.0, 4.0,enemy_images),
                    # Add more enemy positions as needed
                print("Enemy at:",locx , locy )
                
            return enemies

    ##    def render_enemies(screen, player_pos, player_dir, player_plane, enemies):
    ##        nonlocal vertical_angle
    ##        for enemy in enemies:
    ##            delta_x = enemy.pos_x - player_pos[0]
    ##            delta_y = enemy.pos_y - player_pos[1]
    ##
    ##            distance = math.sqrt(delta_x ** 2 + delta_y ** 2) #a^2+b^2=c^2
    ##            angle = math.atan2(delta_y, delta_x) - math.atan2(player_dir[1], player_dir[0])
    ##
    ##            if angle < -math.pi:
    ##                angle += 2 * math.pi
    ##            elif angle >= math.pi:
    ##                angle -= 2 * math.pi
    ##
    ##            if -math.pi / 3 <= angle <= math.pi / 3:  # Adjusted boundary for rendering enemies
    ##                enemy_height = (height) / distance   #i think i gotta mess around with the height to get it rendered right
    ##                # by dividing by 2 it makes the cacodemons look like they float 
    ##                # just need a better method in general
    ##
    ##                # it turns out its easier to chnage the image size but keep the frame the same. 75% of original image seemed to be fine                
    ##                # Calculate the angle between player's direction and the vector from player to enemy
    ##                view_angle = math.atan2(player_dir[1], player_dir[0]) 
    ##                enemy_angle = angle + view_angle 
    ##
    ##                # Calculate the enemy's screen position based on the current player direction and perspective projection
    ##                screen_x = int(round((enemy_angle / (math.pi / 4)) * (width / 2))) + (width // 2)
    ##
    ##                vertical_screen_offset = (height / 2) * math.tan(vertical_angle)
    ##                screen_y = int(round((height - enemy_height) / 2 + vertical_screen_offset))
    ##
    ##                enemy_sprite_scaled = pygame.transform.scale(enemy_sprite, (int(enemy_height), int(enemy_height)))
    ##
    ##                # Correct sprite position based on the updated player direction
    ##                sprite_x = enemy.pos_x - player_pos[0]
    ##                sprite_y = enemy.pos_y - player_pos[1]
    ##                inv_det = 1.0 / (player_plane[0] * player_dir[1] - player_dir[0] * player_plane[1])
    ##                transform_x = inv_det * (player_dir[1] * sprite_x - player_dir[0] * sprite_y)
    ##                transform_y = inv_det * (-player_plane[1] * sprite_x + player_plane[0] * sprite_y)
    ##
    ##                sprite_screen_x = int((width / 2) * (1 + transform_x / transform_y))
    ##
    ##                sprite_screen_y = screen_y
    ##
    ##                screen.blit(enemy_sprite_scaled, (sprite_screen_x, sprite_screen_y))

        def render_enemies(screen, player_pos, player_dir, player_plane, enemies):
            # Create a list to store rendering information
            rendering_data = []  
            #notes , it just needs to render more to the left
            for enemy in enemies:
                delta_x = enemy.pos_x - player_pos[0]
                delta_y = enemy.pos_y - player_pos[1]

                distance = math.sqrt(delta_x ** 2 + delta_y ** 2) #a^2+b^2=c^2
                angle = math.atan2(delta_y, delta_x) - math.atan2(player_dir[1], player_dir[0])

                if angle < -math.pi:
                    angle += 2 * math.pi
                elif angle >= math.pi:
                    angle -= 2 * math.pi

                if -math.pi / 3 <= angle <= math.pi / 3:  # Adjusted boundary for rendering enemies
                    enemy_height = (height) / distance   #i think i gotta mess around with the height to get it rendered right
                    # by dividing by 2 it makes the cacodemons look like they float 
                    # just need a better method in general

                    # it turns out its easier to chnage the image size but keep the frame the same. 75% of original image seemed to be fine                
                    # Calculate the angle between player's direction and the vector from player to enemy
                    view_angle = math.atan2(player_dir[1], player_dir[0]) 
                    enemy_angle = angle + view_angle 

                    # Calculate the enemy's screen position based on the current player direction and perspective projection
                    screen_x = int(round((enemy_angle / (math.pi / 2)) * (width ))) + (width ) # changed pi /  to pi / 2 revert if necessary
                    #also changed width / 2 and width // 2 to just width
                    vertical_screen_offset = (height / 2) * math.tan(vertical_angle)
                    screen_y = int(round((height - enemy_height) / 2 + vertical_screen_offset))

                    # Check if it's time to switch the enemy image
                    current_time = pygame.time.get_ticks()
                    if current_time - enemy.image_timer >= 500:  # Switch image every 500 milliseconds
                        enemy.image_index = 1 - enemy.image_index  # Toggle between 0 and 1
                        enemy.image_timer = current_time

                    # Use the current enemy image
                    enemy_sprite_scaled = pygame.transform.scale(enemy.images[enemy.image_index], (int(enemy_height), int(enemy_height)))

                    # Correct sprite position based on the updated player direction
                    sprite_x = enemy.pos_x - player_pos[0] 
                    sprite_y = enemy.pos_y - player_pos[1] 
                    inv_det = 1.0 / (player_plane[0] * player_dir[1] - player_dir[0] * player_plane[1])
                    transform_x = inv_det * (player_dir[1] * sprite_x - player_dir[0] * sprite_y)
                    transform_y = inv_det * (-player_plane[1] * sprite_x + player_plane[0] * sprite_y)

                    sprite_screen_x = int((width / 2) * (1 + transform_x / transform_y)) 
                    sprite_screen_y = screen_y 

                    rendering_data.append({
                        'type': 'enemy',
                        'draw_start': sprite_screen_y ,
                        'draw_end': sprite_screen_y + enemy_height,
                        'tex_column': enemy_sprite_scaled,
                        'x': sprite_screen_x - (enemy_sprite_scaled.get_size()[0] / 2)
                    })
            return rendering_data

    ##        rendering_data.sort(key=lambda data: data['draw_end'], reverse=True)
    ##
    ##        for data in rendering_data:
    ##            draw_start = data['draw_start']
    ##            draw_end = data['draw_end']
    ##            tex_column = data['tex_column']
    ##            x = data['x']
    ##
    ##            screen.blit(tex_column, (x, draw_start))
            #pass

        def combine_rendering_data(walls, enemies):
            combined_data = walls + enemies
            return sorted(combined_data, key=lambda data: data['draw_end'], reverse=True)

        def render(screen, rendering_data, column_width):
            rendering_data.sort(key=lambda data: data['draw_end'], reverse=False)

            for data in rendering_data:
                if data['type'] == 'wall':
                    x = data['x']
                    draw_start = data['draw_start']
                    tex_column = data['tex_column']
                    screen.blit(tex_column, (x * column_width, draw_start))
                elif data['type'] == 'enemy':
                    draw_start = data['draw_start']
                    draw_end = data['draw_end']
                    tex_column = data['tex_column']
                    x = data['x']
                    screen.blit(tex_column, (x, draw_start))

        class Gun:##this is no longer in use, but left as a reference in the code
            def __init__(self, ammo, max_ammo, shoot_images, reload_images, icon,animation_speed):
                self.ammo = ammo
                self.max_ammo = max_ammo
                self.shoot_images = shoot_images
                self.reload_images = reload_images
                self.icon = icon
                self.shooting_animation = AnimationLogic(shoot_images, animation_speed)
                self.reload_animation = AnimationLogic(reload_images, animation_speed)

            def shoot(self):
                if self.ammo > 0 and not self.shooting_animation.running and not self.reload_animation.running:
                    self.shooting_animation.start_animation()
                    self.ammo -= 1
                    hit_detection()
                elif self.ammo == 0 and not self.reload_animation.running:
                    self.reload()

            def reload(self):
                if self.ammo < self.max_ammo and not self.shooting_animation.running and not self.reload_animation.running:
                    self.reload_animation.start_animation()
                    self.ammo = self.max_ammo

            def render(self, screen):
                

                
                gun_image = self.shoot_images[0]
                gun_width, gun_height = gun_image.get_size()
                screen_width, screen_height = screen.get_size()

                
                
                self.shooting_animation.update_animation()
                self.reload_animation.update_animation()
    ##            if weaponselect == 1:
    ##                gun_pos = ((screen_width - gun_width) // 2 + 60, screen_height - gun_height)
    ##            elif weaponselect == 2:
    ##                if gun_width == 190* 2.5:
    ##                    gun_pos = ((screen_width - gun_width) // 2 + 250, screen_height - gun_height)
    ##                else:
    ##                    gun_pos = ((screen_width - gun_width) // 2 , screen_height - gun_height)
                if weaponselect == 3:
                    
                    gun_pos = ((screen_width - gun_width) // 2 + 60, screen_height - gun_height)
                if weaponselect != 3:
                    gun_pos = ((screen_width - gun_width) // 2 , screen_height - gun_height)
                if self.shooting_animation.running:
                    self.shooting_animation.render(screen, gun_pos)
                elif self.reload_animation.running:
                    self.reload_animation.render(screen, gun_pos)
                else:
                    screen.blit(gun_image, gun_pos)
                screen.blit(self.icon, (570, 560))  # Render gun icon
                ammo_text = f"{self.ammo}/{self.max_ammo}"
                
                ammo_surface = CustomFont.render(ammo_text, True, (255, 0, 0))
                screen.blit(ammo_surface, (580,540))  # Render ammo text
            def check_and_reload(self):
                if self.ammo == 0 and not self.reload_animation.running and not self.shooting_animation.running:
                    self.reload()

        #def hit_detection():   if guns ever come back, rename this as same name used for hammer
         #   pass


        #hammer class - very similar to gun class

        # Preload images for Hammer class
        
        
        class Hammer:
            def __init__(self, max_uses):
                self.max_uses = max_uses
                self.current_uses = max_uses
                self.swing_animation = None
                self.swing_images = hammer_images.copy()


                self.hammer_image = hammer_idle
                self.hammer_image = pygame.transform.scale(self.hammer_image, (width,height)).convert_alpha()
                self.hammer_width, self.hammer_height = self.hammer_image.get_size()

            def use(self):
                if self.current_uses > 0 and not self.swing_animation:
                    self.swing_animation = AnimationLogic(self.swing_images, animation_speed)
                    self.swing_animation.start_animation()
                    self.current_uses -= 1
                    

            def render(self, screen):
                if self.swing_animation:
                    self.swing_animation.update_animation()

                    if self.swing_animation.index == 14:
                        hit_detection_walls(player_pos, world_map)
                    
                    self.swing_animation.render(screen, (width // 2 - self.hammer_width // 2, height // 2 - self.hammer_height // 2))

                    if not self.swing_animation.running:
                        self.swing_animation = None
                else:
                    screen.blit(self.hammer_image, (width // 2 - self.hammer_width // 2, height // 2 - self.hammer_height // 2))

        
        
        class Sword(Hammer):  # Inherit from Hammer to reuse its methods
            def __init__(self, max_uses):
                super().__init__(max_uses)
                self.sword_swing_images = sword_swing_images.copy()

                

                self.sword_draw_images = sword_draw_images.copy()
                

                self.hammer_image = sword_idle
                self.hammer_image = pygame.transform.scale(self.hammer_image, (width, height)).convert_alpha()
                self.hammer_width, self.hammer_height = self.hammer_image.get_size()

                self.draw_animation_running = False

            def use(self):
                if self.current_uses > 0 and not self.swing_animation:
                    self.swing_animation = AnimationLogic(self.sword_swing_images, animation_speed)
                    self.swing_animation.start_animation()
                    # self.current_uses -= 1
                # Check if it's the 8th frame of the animation
                if self.swing_animation and self.swing_animation.index == 8:
                    hit_detection_sprites(player_pos, enemies)

            def draw_sword(self):
                nonlocal SwordIndex, Introlast_image_change_time  # Ensure that SwordIndex and Introlast_image_change_time are used globally

                # Check if the sword animation is not running
                if not self.draw_animation_running and SwordIndex != 18:
                    current_time = pygame.time.get_ticks()  # Gets new fps
                    if current_time - Introlast_image_change_time >= animation_speed:
                        SwordIndex += 1  # Cycles next image

                        # Check if it's the 18th frame to stop blitting
                        if SwordIndex != 18:
                            Introlast_image_change_time = current_time

                # If SwordIndex is 18, stop the animation and render the sword
                if SwordIndex == 18:
                    self.draw_animation_running = False
                    self.render(screen)
                else:
                    screen.blit(self.sword_draw_images[SwordIndex], (0, 0))



        def hit_detection_walls(player_pos, world_map):
            # Get the player's map coordinates
            player_x = int(player_pos[0])
            player_y = int(player_pos[1])

            # Create a list to store the coordinates to remove
            coordinates_to_remove = []

            # Check the surrounding area for breakable walls
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x = player_x + dx
                    y = player_y + dy

                    # Check if the coordinates are within the map boundaries
                    if 0 <= y < len(world_map) and 0 <= x < len(world_map[0]):
                        if world_map[y][x] == '2':
                            # Add the coordinates to the list of coordinates to remove
                            coordinates_to_remove.append((x, y))

            # Remove the walls at the specified coordinates in the world_map
            for x, y in coordinates_to_remove:
                world_map[y][x] = '0'

            print(player_pos)


        def hit_detection_sprites(player_pos, enemies):
            nonlocal numberofenemies
            # Get the player's map coordinates
            player_x, player_y = player_pos[0], player_pos[1]

            # Create a list to store the indices of enemies to remove
            indices_to_remove = []

            # Check for sprites nearby
            for i, enemy in enumerate(enemies):
                enemy_x, enemy_y = enemy.pos_x, enemy.pos_y

                # Calculate the Euclidean distance
                if enemy_x > player_x:
                    delta_x = enemy_x - player_x
                elif player_x > enemy_x:
                    delta_x = player_x - enemy_x
                if enemy_y > player_y:
                    delta_y = enemy_y - player_y
                elif player_y > enemy_y:
                    delta_y = player_y - enemy_y
                distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

                if distance < 2.0 :  # Adjust this threshold based on your requirements
                    indices_to_remove.append(i)

            # Remove the enemies at the specified indices in the enemies list
            for i in reversed(indices_to_remove):
                del enemies[i]
                print("Enemy killed")
                numberofenemies -= 1





        
        
        def PlayerMove():
            nonlocal vertical_angle
            # Get mouse movement
            mouse_movement = pygame.mouse.get_rel()
            mouse_x = mouse_movement[0] * mouse_sensitivity
            mouse_y = mouse_movement[1] * mouse_sensitivity

            # Rotate player direction
            old_dir_x = player_dir[0]
            player_dir[0] = player_dir[0] * math.cos(mouse_x) - player_dir[1] * math.sin(mouse_x)
            player_dir[1] = old_dir_x * math.sin(mouse_x) + player_dir[1] * math.cos(mouse_x)
            old_plane_x = player_plane[0]
            player_plane[0] = player_plane[0] * math.cos(mouse_x) - player_plane[1] * math.sin(mouse_x)
            player_plane[1] = old_plane_x * math.sin(mouse_x) + player_plane[1] * math.cos(mouse_x)



            #looking around
            vertical_angle -= mouse_y
            vertical_angle = max(-vertical_range / 2, min(vertical_range / 2, vertical_angle))
            


            # Handle keyboard input for movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                new_pos_x = player_pos[0] + player_dir[0] * move_speed
                new_pos_y = player_pos[1] + player_dir[1] * move_speed
                if world_map[int(new_pos_y)][int(new_pos_x)] == '0':
                    player_pos[0] = new_pos_x
                    player_pos[1] = new_pos_y
            if keys[pygame.K_s]:
                new_pos_x = player_pos[0] - player_dir[0] * move_speed
                new_pos_y = player_pos[1] - player_dir[1] * move_speed
                if world_map[int(new_pos_y)][int(new_pos_x)] == '0':
                    player_pos[0] = new_pos_x
                    player_pos[1] = new_pos_y
            if keys[pygame.K_a]:
                new_pos_x = player_pos[0] - player_plane[0] * move_speed
                new_pos_y = player_pos[1] - player_plane[1] * move_speed
                if world_map[int(new_pos_y)][int(new_pos_x)] == '0':
                    player_pos[0] = new_pos_x
                    player_pos[1] = new_pos_y
            if keys[pygame.K_d]:
                new_pos_x = player_pos[0] + player_plane[0] * move_speed
                new_pos_y = player_pos[1] + player_plane[1] * move_speed
                if world_map[int(new_pos_y)][int(new_pos_x)] == '0':
                    player_pos[0] = new_pos_x
                    player_pos[1] = new_pos_y

        #make guns

    ##    MP7 = Gun(18, 18, MP7ShootImages, MP7ReloadImages, MP7icon, animation_speed)
    ##    Pistol = Gun(1, 1, PistolShootImages, PistolReloadImages, Pistolicon, animation_speed)
    ##    Shotgun = Gun(1, 1, ShotgunShootImages, ShotgunReloadImages, Shotgunicon, 90)

        #makeguns end


        def get_walkable_coordinates(world_map):
            walkable_coordinates = []

            for y, row in enumerate(world_map):
                for x, cell in enumerate(row):
                    if cell == '0':
                        walkable_coordinates.append((x, y))

            return walkable_coordinates

        walkable_coordinates = get_walkable_coordinates(world_map)
        print(walkable_coordinates)

        hammer = Hammer(max_uses)
        sword = Sword(max_uses)
        enemies=spawn_enemies()
        clock = pygame.time.Clock()
        # Game loop
        progressbar = ("\rwaiting.... " + animation[9])
        print(progressbar)
        print("Loading Complete")
        startuptime = int(pygame.time.get_ticks() / 1000 ) 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


                #old gun code leftas a reference
    ##            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
    ##                shooting=True
    ##                
    ##                
    ##            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
    ##                shooting = False
    ##            if event.type == pygame.KEYDOWN:
    ##                if event.key == pygame.K_r:
    ##                    if weaponselect == 3:
    ##                        MP7.reload()
    ##                    if weaponselect == 2:
    ##                        Pistol.reload()
    ##                    if weaponselect == 1:
    ##                        Shotgun.reload()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        weaponselect = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_2:
                        weaponselect = 2
    ##            if event.type == pygame.KEYUP:
    ##                if event.key == pygame.K_3:
    ##                    weaponselect = 3
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Checks for left mouse button click
                    mouse_pos = pygame.mouse.get_pos()
                    if end_buttons:
                        for button in buttongroup:
                            button.check_click(mouse_pos)
                elif event.type == pygame.MOUSEMOTION:  # Checks for mouse motion
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttongroup:
                        button.check_hover(mouse_pos)

            #end of old gun code
                
            
            mouse_x, _ = pygame.mouse.get_pos()
            if end_buttons == False:
                
                if mouse_x > width / 2 + 100:
                    pygame.mouse.set_pos(width / 2, pygame.mouse.get_pos()[1])

                if mouse_x < width / 2 - 100:
                    pygame.mouse.set_pos(width / 2, pygame.mouse.get_pos()[1])

            #pygame.mouse.set_visible(False)

            screen.fill((128, 128, 128))  # Fills floor
            #screen.fill((80, 80, 80), (0, 0, screen.get_width(), screen.get_height() // 2))  # Fills sky

            # Raycasting
            walls=raycast(screen, player_pos, player_dir, player_plane, world_map, textures, width, height, 1)

            enemies_data = render_enemies(screen, player_pos, player_dir, player_plane, enemies)

            combined_data = combine_rendering_data(walls, enemies_data)

            render(screen, combined_data, 1)

            PlayerMove()  # Maybe in the future make it so you can only move after intro done?
            if Hindex == 19:
                if weaponselect == 1:
                    hammer.render(screen)
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        hammer.use()
                if weaponselect == 2:
                    sword.draw_sword()
                    #sword.render(screen)
                    
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        sword.use()
                if len(enemies) == 0:
                    #print("All enemies destroyed")
                    #print("Completed in",time_elapsed,"seconds")
                    if time_elapsed < best_time:
                        #print("New high score")
                        best_time=time_elapsed
                        with open("leaderboard", "w") as f:
                            f.write(str(best_time))
                    #if time_elapsed > best_time:
                        #print("do better")
                    
                        
                    
                    end_buttons=True
                    
                #old gun stuff
    ##            if weaponselect == 3:
    ##                MP7.render(screen)
    ##                MP7.check_and_reload()
    ##                if shooting:
    ##                    MP7.shoot()
    ##            if weaponselect == 2:
    ##                Pistol.render(screen)
    ##                Pistol.check_and_reload()
    ##                if shooting:
    ##                    Pistol.shoot()
    ##            if weaponselect == 1:
    ##                Shotgun.render(screen)
    ##                Shotgun.check_and_reload()
    ##                if shooting:
    ##                    Shotgun.shoot()
                ########
            
            helmet_animation()
            DrawAutoMap()
            display_coordinates(screen, player_pos)
            if end_buttons==True:
                for button in buttongroup:
                    pygame.draw.rect(screen, button.rect_color, button.rect)
                    pygame.draw.rect(screen, WHITE, button.rect, 2)
                    button.draw_text()
            pygame.mouse.set_visible(end_buttons)

            # Update the display
            pygame.display.flip()
            clock.tick(60)
            fps = clock.get_fps()
            fps_text = f"Ray Caster 1.7 - FPS: {int(fps)}"
            pygame.display.set_caption(fps_text)
            time_elapsed= int(pygame.time.get_ticks() / 1000 ) - startuptime
        # Quit the game
        pygame.quit()
    main()


    
        
