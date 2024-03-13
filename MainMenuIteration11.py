import pygame
import sys
from miniraycastdemoscreen import RayCaster
import time
from MazeCreation import generate_alt_maze, generate_random_maze
import RaycasterV1701
import ColourCaster
def main():
    
    clock = pygame.time.Clock()

    RedShade = (197, 16, 16)    # Red
    White = (255, 255, 255)     # White
    Black = (0, 0, 0)           # Black
    SilveryWhite = (192, 192, 192)  # Silvery White
    Blue = (0, 0, 255)
    GreenBlue=(0,204,204)
    Yellow = (255,255,0)
    global MapSize, NumberOfGeneratedBlocks, ScreenSizePlayerSpeed
    MapSize=(12,6)
    NumberOfGeneratedBlocks=5
    ScreenSizePlayerSpeed=(800,600,1)
    # Screen settings
    screen_width = 1000
    screen_height = 600

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    PlayClicked = False
    SettingsClicked = False


    ##stuff for raycast demo
    rot_r = 0  # rotation angle in radians
    raycastwindow_width = 300
    raycastwindow_height = 500

    fov = 40  # adjusting fov changes the amount of the rays, experiment with this 150 is max around30 pfs
    # note for when implementing minicaster to menu, fov may need to go to 40 ish if fps bad (40 givesaround stable 60fps)
    #100 gives stable 50fps

    xpos, ypos = (3.5, 3.5)

    world_map = ([1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 0, 1, 1, 1],
                 [1, 1, 0, 0, 0, 1, 1],
                 [1, 0, 0, 0, 0, 0, 1],
                 [1, 1, 0, 0, 0, 1, 1],
                 [1, 1, 1, 0, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1])


    #################


    def SetDefault():
        global MapSize, NumberOfGeneratedBlocks, ScreenSizePlayerSpeed
        MapSize = (12,6)
        NumberOfGeneratedBlocks = 5
        ScreenSizePlayerSpeed=(800,600,1)
        print(MapSize)
        print(NumberOfGeneratedBlocks)
        print(ScreenSizePlayerSpeed)
        

    #it sets values but doesnt set elcted button and text in play window - fix this
        #now it resets buttons and actual variables but not text in play window
        #for some reason redefining function in here doesnt work?
        


    class Button:
        def __init__(self, x, y, width, height, label, color=SilveryWhite, highlight_color=RedShade,
                     border_color=Black, border_width=3, corner_radius=10):
            self.original_rect = pygame.Rect(x, y, width, height)
            self.rect = self.original_rect.copy()
            self.label = label
            self.color = color
            self.highlight_color = highlight_color
            self.border_color = border_color
            self.border_width = border_width
            self.corner_radius = corner_radius
            self.is_highlighted = False
            self.is_pressed = False

        def update_size(self):
            if self.is_pressed:
                self.rect = self.original_rect.inflate(-10, -10)
            else:
                self.rect = self.original_rect.copy()


    class PrimaryButton(Button):
        def draw(self, screen):
            # Draw button background or highlighted color
            if self.is_pressed:
                pygame.draw.rect(screen, self.highlight_color, self.rect, border_radius=self.corner_radius)
            elif self.is_highlighted:
                pygame.draw.rect(screen, self.highlight_color, self.rect, border_radius=self.corner_radius)
            else:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)

            # Draw button border
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.corner_radius)
            
            font_size = 36 if not self.is_pressed else 32
            font = pygame.font.Font(None, font_size)
            text = font.render(self.label, True, Black)  # Text color set to Black for visibility
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect.move(primary_window_rect.topleft))


    class SecondaryButton(Button):
        def draw(self, screen):
            # Draw button background or highlighted color
            if self.is_pressed:
                pygame.draw.rect(screen, self.highlight_color, self.rect, border_radius=self.corner_radius)
            elif self.is_highlighted:
                pygame.draw.rect(screen, self.highlight_color, self.rect, border_radius=self.corner_radius)
            else:
                pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)

            # Draw button border
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.corner_radius)
            if self.label == "1000x800:2" or self.label == "800x600:1" or self.label =="600x400:0.5":
                font_size = 18 if not self.is_pressed else 14
            else:
                font_size = 30 if not self.is_pressed else 28
            font = pygame.font.Font(None, font_size)
            text = font.render(self.label, True, Black)  # Text color set to Black for visibility
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)


    class TextBox:
        def __init__(self, x, y, text, font_size=24, text_color=White):
            self.text = text
            self.font_size = font_size
            self.text_color = text_color
            self.font = pygame.font.Font(None, self.font_size)
            self.update_rect(x, y)

        def update_rect(self, x, y):
            text_surface = self.font.render(self.text, True, self.text_color)
            self.rect = text_surface.get_rect(center=(x, y))

        def draw(self, screen, screen_type="Primary"):
            if screen_type == "Primary":
                window_rect = primary_window_rect
            elif screen_type == "Secondary":
                window_rect = secondary_window_rect
            else:
                raise ValueError("Invalid screen_type. Must be 'Primary' or 'Secondary'.")

            text_surface = self.font.render(self.text, True, self.text_color)
            screen.blit(text_surface, self.rect.move(window_rect.topleft))

        def set_font_size(self, font_size):
            self.font_size = font_size
            self.font = pygame.font.Font(None, self.font_size)


    class Title(TextBox):
        def __init__(self, x, y, text, text_color=RedShade):
            super().__init__(x, y, text, font_size=60, text_color=RedShade)


    class Subtitle(TextBox):
        def __init__(self, x, y, text, text_color=White):
            super().__init__(x, y, text, font_size=40, text_color=White)


    class SubtitleSecondary(TextBox):
        def __init__(self, x, y, text, font_size,text_color=Black):
            super().__init__(x, y, text, font_size, text_color=text_color)

        def draw(self, screen, screen_type="Primary"):
            if screen_type == "Primary":
                window_rect = primary_window_rect
            elif screen_type == "Secondary":
                window_rect = secondary_window_rect
            else:
                raise ValueError("Invalid screen_type. Use 'Primary' or 'Secondary'.")

            text_surface = self.font.render(self.text, True, self.text_color)
            screen.blit(text_surface, self.rect.topleft)


    class RoundedRectangle:
        def __init__(self, x, y, width, height, color, border_color, border_width=2, corner_radius=25):
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.border_color = border_color
            self.border_width = border_width
            self.corner_radius = corner_radius

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.corner_radius)
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.corner_radius)


    # Create primary window surface - this is where the main buttons appear
    primary_window_width = 600
    primary_window = pygame.Surface((primary_window_width, screen_height))
    primary_window_rect = primary_window.get_rect()
    primary_midpoint_x = primary_window_rect.width // 2
    primary_midpoint_y = primary_window_rect.height // 2

    # Create secondary window surface  -  this will be where the settings appear
    secondary_window_width = screen_width - primary_window_width
    secondary_window = pygame.Surface((secondary_window_width, screen_height))
    secondary_window_rect = secondary_window.get_rect(topleft=(primary_window_width, 0))
    secondary_midpoint_x = secondary_window_rect.width // 2
    secondary_midpoint_y = secondary_window_rect.height // 2

    # Create button instances for primary window
    exit_button = PrimaryButton(
        x=50,
        y=(screen_height + 300) // 2,
        width=150,
        height=50,
        label="Exit",
        border_color=White  # Specify the border color
    )

    restart_button = PrimaryButton(
        x=50,
        y=(screen_height + 150) // 2,
        width=150,
        height=50,
        label="Restart",
        border_color=White  # Specify the border color
    )

    refresh_button = PrimaryButton(
        x=50,
        y=(screen_height) // 2,
        width=150,
        height=50,
        label="Refresh",
        border_color=White  # Specify the border color
    )

    settings_button = PrimaryButton(
        x=50,
        y=(screen_height - 150) // 2,
        width=150,
        height=50,
        label="Settings",
        border_color=White  # Specify the border color
    )

    play_button = PrimaryButton(
        x=50,
        y=(screen_height - 300) // 2,
        width=150,
        height=50,
        label="Play",
        border_color=White  # Specify the border color
    )

    buttons = [settings_button, play_button, refresh_button, restart_button, exit_button]

    title_text = Title(x=primary_midpoint_x - 175, y=50, text="Raycasting", text_color=RedShade)
    subtitle_text = Subtitle(x=primary_midpoint_x, y=120, text="Subtitle Text", text_color=White)
    textbox_text = TextBox(x=primary_midpoint_x, y=200, text="TextBox Text", text_color=White)

    text_boxes = [title_text, subtitle_text, textbox_text]

    # Create subtitle instances for the secondary window
    Play_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x,
        y=50,  # Adjust the y-coordinate as needed
        text="Play",
        text_color=Black,
        font_size=40   # Specify the text color if needed
    )

    Settings_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x,
        y=50,  # Adjust the y-coordinate as needed
        text="Settings",
        text_color=Black , # Specify the text color if needed
        font_size=40
    )


    MapSizeText_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x,
        y=120,  # Adjust the y-coordinate as needed
        text="MapSize:",
        text_color=Black,  # Specify the text color if needed
        font_size=40
    )

    GenBlocksText_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x,
        y=220,  # Adjust the y-coordinate as needed
        text="Number of Generated Blocks:",
        text_color=Black,  # Specify the text color if needed
        font_size = 35
    )

    ScreenSize_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x,
        y=320,  # Adjust the y-coordinate as needed
        text="Screen Size and player Speed:",
        text_color=Black,  # Specify the text color if needed
        font_size = 35
    )

    ButtonTitleText=[MapSizeText_subtitle_secondary, GenBlocksText_subtitle_secondary,ScreenSize_subtitle_secondary]



    #####display settings in play window
    #genrate button
    secondary_generate_button = SecondaryButton(
        x=secondary_midpoint_x -120 ,
        y=350,
        width=240,
        height=50,
        label="Generate(Enemy Mode)",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_colour_button = SecondaryButton(
        x=secondary_midpoint_x -120 ,
        y=425,
        width=240,
        height=50,
        label="Generate(Colour Mode)",
        color=Yellow,
        border_color=White  # Specify the border color
    )
    secondary_generation_buttons=[secondary_generate_button, secondary_colour_button]
    ####
    
    #map size text
    ##uncoment if bad - uncommented
    CurrentMapSizeVariable_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x +55,
        y=100,  # Adjust the y-coordinate as needed
        text=(str(MapSize)),
        text_color=Black,  # Specify the text color if needed
        font_size=40
    )
    CurrentMapSizeText_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x -55,
        y=100,  # Adjust the y-coordinate as needed
        text=("MapSize:"),
        text_color=Black,  # Specify the text color if needed
        font_size=40
    )

    ##
    #block text

    CurrentBlocksVariable_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x +55,
        y=194,  # Adjust the y-coordinate as needed
        text=(str(NumberOfGeneratedBlocks)),
        text_color=Black , # Specify the text color if needed
        font_size=40
    )


    CurrentBlocks1Text_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x - 10,
        y=150,  # Adjust the y-coordinate as needed
        text=("Number Of"),
        text_color=Black , # Specify the text color if needed
        font_size=40
    )
    CurrentBlocks2Text_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x - 5,
        y=172,  # Adjust the y-coordinate as needed
        text=("Generated "),
        text_color=Black , # Specify the text color if needed
        font_size=40
    )
    CurrentBlocks3Text_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x -10,
        y=194,  # Adjust the y-coordinate as needed
        text=("Blocks: "),
        text_color=Black,  # Specify the text color if needed
        font_size=40
    )


    ###
    #screen size and player speed text
    CurrentScreenSizePlayerSpeedText1_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x + 5,
        y=266,  # Adjust the y-coordinate as needed
        text=("ScreenSize and "),
        text_color=Black , # Specify the text color if needed
        font_size=35
    )
    CurrentScreenSizePlayerSpeedText2_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x + 5,
        y=288,  # Adjust the y-coordinate as needed
        text=("Player Speed:"),
        text_color=Black , # Specify the text color if needed
        font_size=35
    )
    CurrentScreenSizePlayerSpeed_subtitle_secondary = SubtitleSecondary(
        x=secondary_midpoint_x ,
        y=310,  # Adjust the y-coordinate as needed
        text=(str(ScreenSizePlayerSpeed)),
        text_color=Black , # Specify the text color if needed
        font_size=40
    )
    #####################

    # Create rounded rectangle instance for the secondary window
    rounded_rectangle = RoundedRectangle(
        x=secondary_midpoint_x - 187,
        y=secondary_midpoint_y - 287,
        width=375,
        height=575,
        color=SilveryWhite,
        border_color=RedShade
    )

    # Create button instances for secondary window
    #mapsize
    secondary_12x6_button = SecondaryButton(
        x=secondary_midpoint_x - 175,
        y=secondary_midpoint_y - 150,
        width=70,
        height=50,
        label="12x6",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_10x5_button = SecondaryButton(
        x=secondary_midpoint_x - 25,
        y=secondary_midpoint_y - 150,
        width=70,
        height=50,
        label="10x5",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_8x4_button = SecondaryButton(
        x=secondary_midpoint_x + 105 ,
        y=secondary_midpoint_y - 150,
        width=70,
        height=50,
        label="8x4",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondaryMapSize_settings_buttons = [secondary_12x6_button, secondary_10x5_button, secondary_8x4_button]
    ###

    #number of generated block
    secondary_5blocks_button = SecondaryButton(
        x=secondary_midpoint_x - 175,
        y=secondary_midpoint_y - 50,
        width=70,
        height=50,
        label="5",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_10blocks_button = SecondaryButton(
        x=secondary_midpoint_x - 25,
        y=secondary_midpoint_y - 50,
        width=70,
        height=50,
        label="10",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_15blocks_button = SecondaryButton(
        x=secondary_midpoint_x + 105 ,
        y=secondary_midpoint_y - 50,
        width=70,
        height=50,
        label="15",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondaryBlocks_settings_buttons = [secondary_5blocks_button, secondary_10blocks_button, secondary_15blocks_button]
    ####
    #screensize player speed

    secondary_05sizespeed_button = SecondaryButton(
        x=secondary_midpoint_x - 175,
        y=secondary_midpoint_y + 50,
        width=70,
        height=50,
        label="600x400:0.5",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_1sizespeed_button = SecondaryButton(
        x=secondary_midpoint_x - 25,
        y=secondary_midpoint_y + 50,
        width=70,
        height=50,
        label="800x600:1",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondary_2sizespeed_button = SecondaryButton(
        x=secondary_midpoint_x + 105,
        y=secondary_midpoint_y + 50,
        width=70,
        height=50,
        label="1000x800:2",
        color=GreenBlue,
        border_color=White  # Specify the border color
    )

    secondaryScreenSpeed_settings_buttons=[secondary_05sizespeed_button,secondary_1sizespeed_button,secondary_2sizespeed_button]

    ###



    AllSecondaryButtons=(secondaryMapSize_settings_buttons) + (secondaryBlocks_settings_buttons)+ (secondaryScreenSpeed_settings_buttons)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("MapSize=",MapSize)
                pygame.quit()
                sys.exit()

            for button in buttons:
                if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                    button.is_pressed = True
                    button.update_size()
                    print(f"Button '{button.label}' clicked!")
                    if button.label == "Play":
                        PlayClicked = True
                        SettingsClicked = False
                    elif button.label == "Settings":
                        PlayClicked = False
                        SettingsClicked = True
                    else:
                        PlayClicked = False
                        SettingsClicked = False
                        if button.label == "Exit":
                            print("MapSize=",MapSize)
                            pygame.quit()
                            sys.exit()
                        if button.label =="Restart":
                            print("Restarting - this may take a moment")
                            pygame.quit()
                            main()
                            print("Restarted")
                        if button.label =="Refresh":
                            SetDefault()
                            #for some reason these dont work in the function set default but work here?
                            CurrentMapSizeVariable_subtitle_secondary = SubtitleSecondary(
                                x=secondary_midpoint_x +55,
                                y=100,  # Adjust the y-coordinate as needed
                                text=(str(MapSize)),
                                text_color=Black , # Specify the text color if needed
                                font_size=40
                            )
                            CurrentBlocksVariable_subtitle_secondary = SubtitleSecondary(
                                x=secondary_midpoint_x +55,
                                y=194,  # Adjust the y-coordinate as needed
                                text=(str(NumberOfGeneratedBlocks)),
                                text_color=Black , # Specify the text color if needed
                                font_size=40
                            )
                            CurrentScreenSizePlayerSpeed_subtitle_secondary = SubtitleSecondary(
                                x=secondary_midpoint_x ,
                                y=310,  # Adjust the y-coordinate as needed
                                text=(str(ScreenSizePlayerSpeed)),
                                text_color=Black , # Specify the text color if needed
                                font_size=40
                            )

                elif event.type == pygame.MOUSEBUTTONUP:
                    button.is_pressed = False
                    button.update_size()

            # Check events for secondary buttons
            if SettingsClicked:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_in_secondary = (mouse_pos[0] - secondary_window_rect.left, mouse_pos[1] - secondary_window_rect.top)

                #mapsize selection

                for button in secondaryMapSize_settings_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(mouse_pos_in_secondary):
                        button.is_pressed = True
                        button.update_size()
                        print(f"Secondary Button '{button.label}' clicked!")
                        if button.label == "12x6":
                            MapSize=(12,6)
                            
                        if button.label == "10x5":
                            MapSize=(10,5)
                            
                        if button.label == "8x4":
                            MapSize=(8,4)
                        CurrentMapSizeVariable_subtitle_secondary = SubtitleSecondary(
                            x=secondary_midpoint_x +55,
                            y=100,  # Adjust the y-coordinate as needed
                            text=(str(MapSize)),
                            text_color=Black , # Specify the text color if needed
                            font_size=40
                        )

                        
                    elif event.type == pygame.MOUSEBUTTONUP:
                        button.is_pressed = False
                        button.update_size()
                for button in secondaryMapSize_settings_buttons:
            
                    if MapSize==(8,4)and button.label == ("8x4"):

                        button.border_color = RedShade
                    elif MapSize==(10,5) and button.label == ("10x5"):
                        button.border_color = RedShade
                    elif MapSize==(12,6)and button.label == ("12x6"):
                        button.border_color = RedShade
                        
                    else:
                        button.border_color = White

                        
                ###
                #number o fgenrated blocks
                for button in secondaryBlocks_settings_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(mouse_pos_in_secondary):
                        button.is_pressed = True
                        button.update_size()
                        print(f"Secondary Button '{button.label}' clicked!")
                        if button.label == "5":
                            NumberOfGeneratedBlocks=5
                            
                        if button.label == "10":
                            NumberOfGeneratedBlocks=10
                            
                        if button.label == "15":
                            NumberOfGeneratedBlocks=15
                            
                        CurrentBlocksVariable_subtitle_secondary = SubtitleSecondary(
                            x=secondary_midpoint_x +55,
                            y=194,  # Adjust the y-coordinate as needed
                            text=(str(NumberOfGeneratedBlocks)),
                            text_color=Black , # Specify the text color if needed
                            font_size=40
                        )


                    elif event.type == pygame.MOUSEBUTTONUP:
                        button.is_pressed = False
                        button.update_size()
                for button in secondaryBlocks_settings_buttons:
            
                    if NumberOfGeneratedBlocks==5 and button.label == ("5"):

                        button.border_color = RedShade
                    elif NumberOfGeneratedBlocks==10 and button.label == ("10"):
                        button.border_color = RedShade
                    elif NumberOfGeneratedBlocks==15 and button.label == ("15"):
                        button.border_color = RedShade
                        
                    else:
                        button.border_color = White



                #######
                #screen size player speed
                for button in secondaryScreenSpeed_settings_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(mouse_pos_in_secondary):
                        button.is_pressed = True
                        button.update_size()
                        print(f"Secondary Button '{button.label}' clicked!")
                        if button.label == "600x400:0.5":
                            ScreenSizePlayerSpeed=(600,400,0.5)
                            
                        if button.label == "800x600:1":
                            ScreenSizePlayerSpeed=(800,600,1)
                            
                        if button.label == "1000x800:2":
                            ScreenSizePlayerSpeed =(1000,800,2)
                            
                        CurrentScreenSizePlayerSpeed_subtitle_secondary = SubtitleSecondary(
                            x=secondary_midpoint_x ,
                            y=310,  # Adjust the y-coordinate as needed
                            text=(str(ScreenSizePlayerSpeed)),
                            text_color=Black , # Specify the text color if needed
                            font_size=40
                        )


                    elif event.type == pygame.MOUSEBUTTONUP:
                        button.is_pressed = False
                        button.update_size()
                for button in secondaryScreenSpeed_settings_buttons:
            
                    if ScreenSizePlayerSpeed==(600,400,0.5) and button.label == ("600x400:0.5"):

                        button.border_color = RedShade
                    elif ScreenSizePlayerSpeed==(800,600,1) and button.label == ("800x600:1"):
                        button.border_color = RedShade
                    elif ScreenSizePlayerSpeed==(1000,800,2) and button.label == ("1000x800:2"):
                        button.border_color = RedShade
                        
                    else:
                        button.border_color = White

            ################
                                

        # Check if mouse is over any button - primary only
        for button in buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.is_highlighted = True
            else:
                button.is_highlighted = False

        # Check if mouse is over any secondary button(highlight system)
        if SettingsClicked:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos_in_secondary = (mouse_pos[0] - secondary_window_rect.left, mouse_pos[1] - secondary_window_rect.top)

            for button in secondaryMapSize_settings_buttons:
                if button.rect.collidepoint(mouse_pos_in_secondary):
                    button.is_highlighted = True
                else:
                    button.is_highlighted = False
            for button in secondaryBlocks_settings_buttons:
                if button.rect.collidepoint(mouse_pos_in_secondary):
                    button.is_highlighted = True
                else:
                    button.is_highlighted = False
            for button in secondaryScreenSpeed_settings_buttons:
                if button.rect.collidepoint(mouse_pos_in_secondary):
                    button.is_highlighted = True
                else:
                    button.is_highlighted = False

        # Update primary window
        primary_window.fill(Black)

        # Draw the buttons on the primary window
        for button in buttons:
            button.draw(primary_window)

        # Draw the text boxes on the primary window
        for text_box in text_boxes:
            text_box.draw(primary_window, screen_type="Primary")

        for button in buttons:
            if button.label == "Play" and PlayClicked:
                button.border_color = RedShade
            elif button.label == "Settings" and SettingsClicked:
                button.border_color = RedShade
            else:
                button.border_color = White

        # Update secondary window
        secondary_window.fill(Black)  # Fill with the desired color

        # Draw rounded rectangle for the background on the secondary window
        rounded_rectangle.draw(secondary_window)

        # Draw "Settings" subtitle on the secondary window
        if PlayClicked:
            Play_subtitle_secondary.draw(secondary_window, screen_type="Secondary")

            ##is this bad? I assume its infinitely rewriting the variable?
            #moved over to under buttons
    ##        CurrentMapSizeVariable_subtitle_secondary = SubtitleSecondary(
    ##            x=secondary_midpoint_x +55,
    ##            y=100,  # Adjust the y-coordinate as needed
    ##            text=(str(MapSize)),
    ##            text_color=Black  # Specify the text color if needed
    ##        )
            ##end of bad
            
            CurrentMapSizeVariable_subtitle_secondary.draw(secondary_window, screen_type="Secondary")
            CurrentMapSizeText_subtitle_secondary.draw(secondary_window, screen_type="Secondary")

            CurrentBlocksVariable_subtitle_secondary.draw(secondary_window, screen_type="Secondary")
            CurrentBlocks1Text_subtitle_secondary.draw(secondary_window, screen_type="Secondary")
            CurrentBlocks2Text_subtitle_secondary.draw(secondary_window, screen_type="Secondary")
            CurrentBlocks3Text_subtitle_secondary.draw(secondary_window, screen_type="Secondary")

            CurrentScreenSizePlayerSpeedText1_subtitle_secondary.draw(secondary_window, screen_type="Secondary")
            CurrentScreenSizePlayerSpeedText2_subtitle_secondary.draw(secondary_window, screen_type="Secondary")

            CurrentScreenSizePlayerSpeed_subtitle_secondary.draw(secondary_window, screen_type="Secondary")

            
            secondary_generate_button.draw(secondary_window)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos_in_secondary = (mouse_pos[0] - secondary_window_rect.left, mouse_pos[1] - secondary_window_rect.top)
            if secondary_generate_button.rect.collidepoint(mouse_pos_in_secondary):
                secondary_generate_button.is_highlighted = True
                if event.type == pygame.MOUSEBUTTONDOWN :
                    secondary_generate_button.is_pressed = True
                    secondary_generate_button.update_size()
                    print(f"Button '{button.label}' clicked!")
                    print("Generating...")
                if event.type == pygame.MOUSEBUTTONUP:
                    secondary_generate_button.is_pressed = False
                    secondary_generate_button.update_size()
                    generate_alt_maze(MapSize, NumberOfGeneratedBlocks)
                    print("Generated Map")
                    print("Loading...")
                    RaycasterV1701.ScreenSizePlayerSpeed=ScreenSizePlayerSpeed
                    RaycasterV1701.main()
                    RaycasterV1701.ScreenSizePlayerSpeed=ScreenSizePlayerSpeed
            else:
                secondary_generate_button.is_highlighted = False

            secondary_colour_button.draw(secondary_window)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos_in_secondary = (mouse_pos[0] - secondary_window_rect.left, mouse_pos[1] - secondary_window_rect.top)
            if secondary_colour_button.rect.collidepoint(mouse_pos_in_secondary):
                secondary_colour_button.is_highlighted = True
                if event.type == pygame.MOUSEBUTTONDOWN :
                    secondary_colour_button.is_pressed = True
                    secondary_colour_button.update_size()
                    print(f"Button '{button.label}' clicked!")
                    print("Generating...")
                if event.type == pygame.MOUSEBUTTONUP:
                    secondary_colour_button.is_pressed = False
                    secondary_colour_button.update_size()
                    generate_random_maze(MapSize, NumberOfGeneratedBlocks)
                    print("Generated Map")
                    print("Loading...")
                    ColourCaster.ScreenSizePlayerSpeed=ScreenSizePlayerSpeed
                    ColourCaster.main()
                    ColourCaster.ScreenSizePlayerSpeed=ScreenSizePlayerSpeed
            else:
                secondary_colour_button.is_highlighted = False
                
                

            
        if SettingsClicked:
            # Draw secondary settings text only when SettingsClicked is True
            Settings_subtitle_secondary.draw(secondary_window, screen_type="Secondary")
            # Draw secondary settings buttons only when SettingsClicked is True

            for text in ButtonTitleText:
                text.draw(secondary_window, screen_type="Secondary")

            
            for button in AllSecondaryButtons:
                button.draw(secondary_window)

        if SettingsClicked == False and PlayClicked == False:
            raycaster_x = (secondary_window_rect.width - raycastwindow_width) // 2
            raycaster_y = (secondary_window_rect.height - raycastwindow_height) // 2

            rot_r += 0.005


            RayCaster(secondary_window, rot_r, xpos, ypos, fov, raycastwindow_width, raycastwindow_height, world_map, raycaster_x, raycaster_y)

        # Update main display
        screen.blit(primary_window, primary_window_rect)
        screen.blit(secondary_window, secondary_window_rect)


        clock.tick(60)
        fps = clock.get_fps()
        fps_text = f"Menu - FPS: {int(fps)}"
        pygame.display.set_caption(fps_text)
        pygame.display.flip()

if __name__ == '__main__':
    main()
