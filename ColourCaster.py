import pygame
from pygame.locals import *
import math
import MainMenuIteration11
ScreenSizePlayerSpeed=(800,600,1)
def main():
    
    # Read automap data from file
    with open("ColourMap") as f:
        minimap = f.read().split("\n")

    world_map = []
    for row in minimap:   #rewrite mapcreation to do this , this is a waste of cpu
        map_row = []
        for value in row:
            if value == '1':
                map_row.append(1)
                
            else:
                map_row.append(0)
        world_map.append(map_row)

    pygame.init()

    try:
        dmfont = "dmfont.ttf"
        button_font = pygame.font.Font(dmfont, 24)
    except:
        dmfont = None
        button_font = pygame.font.Font(dmfont, 24)
    
    screen_width = 1200
    screen_height = 900

    screen_width, screen_height, SpeedMultiplier =(ScreenSizePlayerSpeed)
    
    fov = 80         # adjusting fov changes the amount of the rays, experiment with this
    xpos, ypos = (5, 4)
    rot_r = 0      #rotation angle in radians

    PURPLE = (155, 0, 255)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # Button dimensions
    button_width = 125
    button_height = 50

    # Default button colors
    default_color = RED
    hovered_color = PURPLE
    selected_color = WHITE

    # Button text
    button_text_color = WHITE

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ray Caster")

    show_map = True  # decides if map should be visible

    class Button(pygame.sprite.Sprite):
        def __init__(self, x, start_y, target_pos, text):
            super().__init__()

            self.rect = pygame.Rect(x - button_width // 2, start_y, button_width, button_height)
            self.start_y = start_y
            self.speed = 5  # Falling speed
            self.target_pos = target_pos
            self.text = text
            self.rect_color = default_color  # Added attribute

            all_sprites.add(self)
            buttongroup.add(self)

        def check_click(self, mouse_pos):
            if self.rect.collidepoint(mouse_pos):
                print("Button clicked:", self.text)
                if self.text == "Exit":
                    print("exit")
                    pygame.quit()
                    MainMenuIteration11.main()

        def check_hover(self, mouse_pos):
            if self.rect.collidepoint(mouse_pos):
                self.rect_color = hovered_color
            else:
                self.rect_color = default_color

        def update(self):
            if self.rect.y < self.target_pos[1]:
                self.rect.y += self.speed

        def draw_text(self):
            text_surface = button_font.render(self.text, True, button_text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def DrawAutoMap():   # make this more tidy its not tidy
        square_size = 20
        red_color = (255, 0, 0)
        purple_color=(155,0,255)
        light_grey_color = (200, 200, 200)
        BLACK = (0, 0, 0)
        outline_thickness = 2

        if show_map:
            for j, row in enumerate(world_map):
                for i, value in enumerate(row):
                    if value == 1:
                        #pygame.draw.rect(screen, BLACK, (i * square_size, j * square_size, square_size, square_size))
                        pygame.draw.rect(screen, WHITE, (i * square_size, j * square_size, square_size, square_size),
                                         outline_thickness)
                    else:
                        #pygame.draw.rect(screen, BLACK, (i * square_size, j * square_size, square_size, square_size))
                        pygame.draw.rect(screen, BLACK, (i * square_size, j * square_size, square_size, square_size),
                                         outline_thickness)
            #player location
            player_pos_x = int(xpos * square_size) + square_size  //8
            player_pos_y = int(ypos * square_size) + square_size // 8
            pygame.draw.circle(screen, PURPLE, (player_pos_x, player_pos_y), square_size // 4)
        
            #player direction
            line_length = square_size // 2
            direction_x = player_pos_x + int(line_length * math.cos(rot_r))
            direction_y = player_pos_y + int(line_length * math.sin(rot_r))
            pygame.draw.line(screen, WHITE, (player_pos_x, player_pos_y),(direction_x, direction_y), 2)
        
    def RayCaster():            #this is bad rewrite this cuz its bad doesnt work not good
        for i in range(fov): #i is the ray number, so the first ray generated is i = 1
            rot_d = rot_r + math.radians(i - fov / 2)  #rot_r but accounts for depth
            x, y = (xpos, ypos)
            sin, cos = (0.02 * math.sin(rot_d), 0.02 * math.cos(rot_d))
            j = 0
            while True:
                x, y = (x + cos, y + sin)
                j += 1
                if 0 <= int(x) < len(world_map[0]) and 0 <= int(y) < len(world_map):
                    if world_map[int(y)][int(x)] != 0:
                        d=j
                        height = (10 / j * 1500)
                        break
            if d/2 > 255:
                d=510             #this makes the fog effect but this is bad so redo it aswell
##            pygame.draw.line(screen, (255, 0, 0), (i * (screen_width / fov), (screen_height / 2) + height),
##                             (i * (screen_width / fov), (screen_height / 2) - height),
##                             width=int(screen_width / fov))  #line to use if using a version of pygame higher than 1.9
            pygame.draw.line(screen, (255, 255-d/2, 0+d/40), (i * (screen_width / fov), (screen_height / 2) + height),
                             (i * (screen_width / fov), (screen_height / 2) - height),int(screen_width / fov))

    clock = pygame.time.Clock()

    
    all_sprites = pygame.sprite.Group()
    buttongroup = pygame.sprite.Group()

    exit_button = Button(screen_width - 100 , -100, (screen_width, 50), "Exit")
    move_speed=0.05 #starting value
    move_speed = move_speed * SpeedMultiplier
    print("Width",screen_width,"Height",screen_height, "Player Speed=",move_speed)
    previous_mouse_x = 0
    done = False
    while not done:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                show_map = not show_map  # Toggles the visibility of the map
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Checks for left mouse button click
                mouse_pos = pygame.mouse.get_pos()
                if show_map:
                    for button in buttongroup:
                        button.check_click(mouse_pos)
            elif event.type == pygame.MOUSEMOTION:  # Checks for mouse motion
                mouse_pos = pygame.mouse.get_pos()
                for button in buttongroup:
                    button.check_hover(mouse_pos)

        mouse_x, _ = pygame.mouse.get_pos()

        # Check if the mouse moved left
        if mouse_x < previous_mouse_x:
            rot_r -= 0.04    #0.04 seems a safe option but depends on mouse dpi
        if mouse_x > previous_mouse_x:
            rot_r += 0.04  # may need to be adjusted
        previous_mouse_x = mouse_x


        #move ## if this ends up breaking its cuz you took it from astroids
        #should have just did it from scratch
        # re do the collision system its awful, you collide with the midpoint, rather than the edge
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_xpos = xpos + move_speed * math.cos(rot_r)
            new_ypos = ypos + move_speed * math.sin(rot_r)
            if world_map[int(new_ypos)][int(new_xpos)] == 0:
                xpos = new_xpos
                ypos = new_ypos
        if keys[pygame.K_s]:
            new_xpos = xpos - move_speed * math.cos(rot_r)
            new_ypos = ypos - move_speed * math.sin(rot_r)
            if world_map[int(new_ypos)][int(new_xpos)] == 0:
                xpos = new_xpos
                ypos = new_ypos
        if keys[pygame.K_d]:
            new_xpos = xpos - move_speed * math.sin(rot_r)
            new_ypos = ypos + move_speed * math.cos(rot_r)
            if world_map[int(new_ypos)][int(new_xpos)] == 0:
                xpos = new_xpos
                ypos = new_ypos
        if keys[pygame.K_a]:
            new_xpos = xpos + move_speed * math.sin(rot_r)
            new_ypos = ypos - move_speed * math.cos(rot_r)
            if world_map[int(new_ypos)][int(new_xpos)] == 0:
                xpos = new_xpos
                ypos = new_ypos
        
        
        RayCaster()
        DrawAutoMap()

        for sprite in all_sprites:
            sprite.update()

        if show_map:
            
            for button in buttongroup:
                pygame.draw.rect(screen, button.rect_color, button.rect)
                pygame.draw.rect(screen, WHITE, button.rect, 2)
                button.draw_text()
        if show_map == False:
            if mouse_x > screen_width/2 + 100 :
                pygame.mouse.set_pos(screen_width / 2, pygame.mouse.get_pos()[1])
        
            if mouse_x < screen_width/2 - 100 :
                pygame.mouse.set_pos(screen_width / 2, pygame.mouse.get_pos()[1])
        pygame.mouse.set_visible(show_map)
        pygame.display.flip()
        clock.tick(60)
        fps = clock.get_fps()
        fps_text = f"Ray Caster 1.7 - FPS: {int(fps)}"
        pygame.display.set_caption(fps_text)


    pygame.quit()
    #performance becomes awful - redo the ray caster
    #at 1200,900 , the lines between drawn lines dissappear - some sort of error that makes it better in some ways
    # actually redo the ray caster dont put it off
if __name__ == "__main__":
    main()
