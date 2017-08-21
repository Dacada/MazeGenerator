#!/usr/bin/python3

from PIL import Image
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Generate a random maze and show it or save it to a file",
        epilog = """
        The x and y coordinates are the size of the longes possible corridor in units. These coordinates must always be odd. If they are even the longes possible corridor in either direction will be of that size minus 1.
        This size isn't necessarily in pixels. Each "unit" in the maze can be set to be N x N pixels by setting the -p option.
        It defaults to 5, so a value of x = 20 and y = 25 will create a 19 units per 25 units maze,
        which will translate into 19*5+2 x 25*2+2  or  97 x 127 pixels (adding a border of unit size).
        """
    )
    parser.add_argument(
        'x',
        type = int,
        help = "X coordinate of the size of the maze."
    )
    parser.add_argument(
        'y',
        type = int,
        help = "Y coordinate of the size of the maze."
    )
    parser.add_argument(
        '-f', '--file',
        type = argparse.FileType('wb'),
        help = "Save the generated maze to the given file instead of showing it."
    )
    parser.add_argument(
        '-p', '--pixel',
        type = int,
        default = 5,
        help = "Size of a square unit in pixels."
    )
    parser.add_argument(
        '-s', '--seed',
        type = int,
        help = "Random seed to base the maze on. The same seed will generate the same maze. "
    )
    return parser.parse_args()

def generate_maze(x_size, y_size):
    maze = [0]*(x_size)
    maze = [maze[::] for __ in range(y_size)]
    
    x = 0
    y = 0
    last_coords = []
    
    while True:
        maze[y][x] = 1
        
        directions = []
        if y-2 >= 0 and maze[y-2][x] == 0:
            directions.append('n')
        if y+2 < y_size and maze[y+2][x] == 0:
            directions.append('s')
        if x-2 >= 0 and maze[y][x-2] == 0:
            directions.append('w')
        if x+2 < x_size and maze[y][x+2] == 0:
            directions.append('e')
            
        #print(directions,(x,y))
        #print_maze(maze)
        #input()

        if not directions and x == 0 and y == 0:
            break
        elif not directions:
            x,y = last_coords.pop()
            continue
            
        last_coords.append((x,y))
        direction = random.choice(directions)
        if direction == 'n':
            y -= 1
            maze[y][x] = 1
            y -= 1
        elif direction == 's':
            y += 1
            maze[y][x] = 1
            y += 1
        elif direction == 'w':
            x -= 1
            maze[y][x] = 1
            x -= 1
        elif direction == 'e':
            x += 1
            maze[y][x] = 1
            x += 1

    return maze

def print_maze(maze):
    for l in maze:
        for n in l:
            print(n, end='')
        print()

def create_maze_image(maze, unit_pixels):
    maze = [[0] + l + [0] for l in maze]
    wall = [0]*len(maze[0])
    maze = [wall] + maze + [wall]
    
    im = Image.new('1', (len(maze[0]), len(maze)))
    im.putdata(sum(maze, []))
    im = im.resize((len(maze[0])*unit_pixels, len(maze)*unit_pixels))
    return im
        
def show_maze(maze, unit_pixels):
    create_maze_image(maze, unit_pixels).show()

def save_maze(maze, unit_pixels, filename):
    create_maze_image(maze, unit_pixels).save(filename)
    
def main():
    args = parse_args()
    if args.x % 2 == 0:
        args.x -= 1
    if args.y % 2 == 0:
        args.y -= 1
        
    random.seed(args.seed)
    maze = generate_maze(args.x, args.y)
    
    if args.file is None:
        show_maze(maze, args.pixel)
    else:
        save_maze(maze, args.pixel, args.file)

if __name__ == "__main__":
    main()
