# raycaster.py
import pygame
import math

def RayCaster(screen,rot_r, xpos, ypos, fov, raycastwindow_width,raycastwindow_height,world_map, raycaster_x, raycaster_y):
    #global rot_r, xpos, ypos, fov, raycastwindow_width,raycastwindow_height
    for i in range(fov):
        rot_d = rot_r + math.radians(i - fov / 2)
        x, y = (xpos, ypos)
        sin, cos = (0.02 * math.sin(rot_d), 0.02 * math.cos(rot_d))
        j = 0
        while True:
            x, y = (x + cos, y + sin)
            j += 1
            if 0 <= int(x) < len(world_map[0]) and 0 <= int(y) < len(world_map):
                if world_map[int(y)][int(x)] != 0:
                    d = j
                    e = j
                    height = (10 / j * 1500)
                    break

        #orange version
        #pygame.draw.line(screen, (255 - e / 2, 128 - d / 2, 0),
        #(raycaster_x + i * (raycastwindow_width / fov), raycaster_y + (raycastwindow_height / 2) + height),
        #(raycaster_x + i * (raycastwindow_width / fov), raycaster_y + (raycastwindow_height / 2) - height), int(raycastwindow_width / fov))


        #red version
        pygame.draw.line(screen, (255 - e / 2, 0, 0),
        (raycaster_x + i * (raycastwindow_width / fov), raycaster_y + (raycastwindow_height / 2) + height),
        (raycaster_x + i * (raycastwindow_width / fov), raycaster_y + (raycastwindow_height / 2) - height), int(raycastwindow_width / fov))



        #rot_r += 0.0001
        if d/2 > 128:
            d = 256
        if e/2 > 90:
            e = 180
