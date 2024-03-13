import random



def generate_random_maze(MapSize,NumberOfGeneratedBlocks):
    #use this for if we need maps without 2 walls.
    width,height=MapSize
    maze = [['1' for _ in range(width)] for _ in range(height)]

    def carve_maze(x, y):
        maze[y][x] = '0'

        directions = [(x-2, y), (x, y+2), (x+2, y), (x, y-2)]
        random.shuffle(directions)

        for dx, dy in directions:
            if 0 <= dx < width and 0 <= dy < height and maze[dy][dx] == '1':
                maze[(y + dy) // 2][(x + dx) // 2] = '0'
                carve_maze(dx, dy)

    carve_maze(1, 1)

    # Add border walls
    for i in range(width):
        maze[0][i] = '1'
        maze[height - 1][i] = '1'
    for i in range(height):
        maze[i][0] = '1'
        maze[i][width - 1] = '1'
    maze[1][1]="0"
    maze[2][2]="0"
    print (maze)
    with open('ColourMap', 'w') as f:
        for row in maze:
            f.write(''.join(row))
            f.write('\n')


##def generate_alt_maze(MapSize,NumberOfGeneratedBlocks):
##    width, height = MapSize
##    maze = [['1' for _ in range(width)] for _ in range(height)]
##
##    def carve_maze(x, y):
##        maze[y][x] = '0'
##
##        directions = [(x-2, y), (x, y+2), (x+2, y), (x, y-2)]
##        random.shuffle(directions)
##
##        for dx, dy in directions:
##            if 0 <= dx < width and 0 <= dy < height and maze[dy][dx] == '1':
##                maze[(y + dy) // 2][(x + dx) // 2] = '0'
##                carve_maze(dx, dy)
##
##    # Carve main maze
##    carve_maze(1, 1)
##
##    # Create breakable blocks
##    num_blocks = NumberOfGeneratedBlocks
##    for _ in range(num_blocks):
##        
##        x = random.randint(1, width - 2)
##        y = random.randint(1, height - 2)
##        
##        maze[y][x] = '2'
##        
##            
##                
##        
##
##    # Add border walls
##    for i in range(width):
##        maze[0][i] = '1'
##        maze[height - 1][i] = '1'
##    for i in range(height):
##        maze[i][0] = '1'
##        maze[i][width - 1] = '1'
##    print(maze)
##
##    with open('RandomMaze', 'w') as f:
##        for row in maze:
##            f.write(''.join(row))
##            f.write('\n')



def generate_alt_maze(MapSize, NumberOfGeneratedBlocks):
    x,y = MapSize
    x+=2
    y+=2
    maze = [['1' for _ in range(x)] for _ in range(y)]  # Initialize maze with all walls
    #print("making start of maze")
    #print(maze)
    def generate_paths(cx, cy):
        directions = [(2, 0), (-2, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < x -1  and 0 < ny < y - 1 and maze[ny][nx] == '1':
                maze[cy + dy // 2][cx + dx // 2] = '0'
                maze[ny][nx] = '0'
                generate_paths(nx, ny)

    start_x = random.randrange(1, x - 1, 2)
    start_y = random.randrange(1, y - 1, 2)
    maze[start_y][start_x] = '0'
    generate_paths(start_x, start_y)

    num_blocks = NumberOfGeneratedBlocks
    for row in maze:
        for i in range(len(row)):
            if row[i] == '0' and num_blocks != 0:
                chance = random.randint(1, 4)
                if chance == 1:
                    row[i] = '2'
                    num_blocks -= 1
    #format = maze(y,x)
    maze[1][1]="0"
    maze[2][2]="0"
    #print("go")
    #print(maze)
    for n in range(1,y-1):
        
        maze[n][x-2]="0"
    #return maze
    with open('automap', 'w') as f:
        for row in maze:
            f.write(''.join(row))
            f.write('\n')

### Example usage:
##x = 12
##y = 6
##maze = generate_maze(x, y)
##
### Print the generated maze
##for row in maze:
##    print(row)
