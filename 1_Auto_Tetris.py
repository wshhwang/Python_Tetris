######################################
#Created by William Hwang
#Posted   https://youtu.be/Y9NYF_b9YTI
######################################
"""
1. create data strucuture (Tetrinos)
2. global variables (Screensize,tetrinos size)
3. function
4. create 10x20 grid
5. draw grid
6. draw window
7. rotating tetrinos in tetris
8. setting up tetris

"""
import pygame
import random

#############################################################
####################global variables#########################
#############################################################
#basic requirment (MUST)
#pygame.init() #Refresh (required)
pygame.font.init() # font init (required)

#set screen size
screen_width = 800 #back ground h
screen_height = 700 # back ground w
game_width = 300 #playing  w
game_height = 600 #playing  h
block_size = 30

top_left_x = (screen_width - game_width) // 2
top_left_y = (screen_height - game_height)
    #screen = pygame.display.set_mode((screen_width, screen_height))

# Tetrinos Format
# includes Possible Rotation
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#indexing tetrinos [0- 6]
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object): 
    def __init__(self, x,y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)] #whenever index shapes will find corresding shape color
        self.rotation = 0 #Rotate tetrinos by adding 1 and deduct 1


def create_grid(locked_pos = {}): #locked_position (dictionary) ex: {(1,1): (255,0,0)}
    grid = [[(0,0,0) for x in range(10)] for x in range(20)] #creat list of (0,0,0 for x in range(10)) in every 20 row in the grid

    for i in range(len(grid)): #grid range = 20
        for j in range(len(grid[i])):
            if (j,i) in locked_pos: 
                c = locked_pos[(j,i)]
                grid [i] [j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions
    #pass

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
    #pass

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False
    #pass

def get_shape():
    return Piece(5,3, random.choice(shapes)) #give random shapes

def draw_text_middle(surface, text, size, color):
    font = pygame.font.FontType(None, size,bold=True)
    label = font.render (text, 1, color)
    surface.blit(label, (top_left_x + game_width /2 - (label.get_width()/2), top_left_y + game_height/2 - label.get_height()/2))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+game_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + game_height))

    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y+i*block_size), 0) #(surface ,color, position, block size, fill the shape)
    pygame.draw.rect (surface, (255,0,0), (top_left_x,top_left_y,game_width,game_height),4) #(surface, color, poisition, boarder size = 4)
    """

def clear_rows(grid, locked):
    
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_next_shape(shape, surface):
   pass

def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    
    return score




def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Auto Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + game_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + game_width + 50
    sy = top_left_y + game_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))

     # credit
    font = pygame.font.SysFont('comicsans', 25)
    credit1 = font.render('By William Hwang', 1, (182,230,29))
    credit2 = font.render('Tetris Python Project', 1, (182,230,29))

    sx = top_left_x + game_width + 50
    sy = top_left_y + game_height/2 - 100

    surface.blit(credit2, (sx + 10, sy + 320))
    surface.blit(credit1, (sx + 10, sy + 350))
 

    # last score
    #label = font.render("High Score: " + last_score, 1, (255,255,255))
    label = font.render("High Score: " , 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 255, 0), (top_left_x, top_left_y, game_width, game_height), 10)

    draw_grid(surface, grid)
    #pygame.display.update()

def main(win):

    last_score= max_score()
    
    locked_positions= {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    
    fall_speed = 0.50
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                #quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1 #move position -1
                    if not valid_space(current_piece, grid): #check valid position
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                
                if event.key == pygame.K_SPACE:
                    # move shape down
                    current_piece.y += 10
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 10

                if event.key == pygame.K_UP:                 
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 #% len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 # % len(current_piece.shape)
        
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "FAIL", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)
        
        #draw_window(win, grid)

def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Enter', 50, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


   
win = pygame.display.set_mode((screen_width, screen_height))
#set screen title
pygame.display.set_caption("Auto Tetris") #game title
main_menu(win)










"""
#FPS
clock = pygame.time.Clock()
#############################################################

#Basic User Interface (UI) Setting (Background, game character image, Coordination, Speed, font, enemy character )

#set background image
background = pygame.image.load("C:\\Users\\wshhw\\Documents\\VisualStudio Project\\Python\\Game Project\\PythonGame1\\PythonGame1\\pygame_basic\\background.png")

#set game character 
character = pygame.image.load("C:\\Users\\wshhw\\Documents\\VisualStudio Project\\Python\\Game Project\\PythonGame1\\PythonGame1\\pygame_basic\\character.png")
character_size = character.get_rect().size #call image size
character_width = character_size[0] 
character_height = character_size[1]
character_x_pos = (screen_width/2)-(character_width/2) #half position of screen
character_y_pos = screen_height-character_height #max position of screen (lowest position)
character_speed = 0.8

#Character Coordination (location to move)
to_x = 0 
to_y = 0

#Assign enemy character
enemy = pygame.image.load("C:\\Users\\wshhw\\Documents\\VisualStudio Project\\Python\\Game Project\\PythonGame1\\PythonGame1\\pygame_basic\\enemy.png")
enemy_size = enemy.get_rect().size #call image size
enemy_width = enemy_size[0] 
enemy_height = enemy_size[1]

enemy_x_pos = random.randrange(0,(screen_width-enemy_width))
enemy_y_pos = 0 #max position of screen (lowest position)
enemy_speed = 3

#assign Font for text
title_font = pygame.font.Font(None,30)
game_font = pygame.font.Font(None, 38) #create(font and size)
point_font = pygame.font.Font(None, 55)
gameover_font = pygame.font.Font(None,100)

#assign Time
total_time = 30

#Start time
start_ticks = pygame.time.get_ticks() #receive tick info

#Life Count
num_life = 3

#Point count
point = 0
 

#Configuration for Run game (Keyboard, Mouse)
running = True
while running: 
    dt = clock.tick(100) #FPS
    
    for event in pygame.event.get(): #check event for loop
        if event.type == pygame.QUIT: #check close screen event
            running = False #game is not running
                          

     #Keyboard movement       
        if event.type == pygame.KEYDOWN: #check status KEYDOWN
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key ==pygame.K_RIGHT:
                to_x += character_speed              

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
       
    character_x_pos +=  to_x *dt
   
    
    #set max X position (prevent out of screen)
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width:
        character_x_pos = screen_width - character_width

    #set max Y position    
    if character_y_pos <0 :
        character_y_pos = 0
    elif character_y_pos > screen_height:
        character_y_pos = screen_height - character_height
  
    #update rect information  
    character_rect= character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos 

    #Print Setting
    timer_title = title_font.render ("Time", False, (0,0,0))
    life_title = title_font.render("Life", False, (0, 0, 0) ) #Yellow
    life_count = game_font.render(str(num_life), False, (255,0,0) ) #Yellow
    
    point_count = point_font.render (str(point),False, (34,177,76))

    #check collison
    if character_rect.colliderect(enemy_rect): # check character collide with enemy
        print("Collide!")
        num_life -= 1
        enemy_y_pos = 0
        enemy_x_pos = random.randrange(0,(screen_width-enemy_width))
        if num_life == 0:
            
            print("Game Over")
            running = False
            

    enemy_y_pos += enemy_speed
    if enemy_y_pos > (screen_height):
        enemy_speed +=0.5
        point += 1
        if (point%5)==0:
            total_time += 20
        enemy_y_pos = 0
        enemy_x_pos = random.randrange(0,(screen_width-enemy_width))

    #Display setting
    #run background image
    screen.blit(background, (0,0)) 

    #run character
    screen.blit(character, (character_x_pos, character_y_pos))
    
    #run enemy
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    #run timer
        #calculated spent time
    elapsed_time = (pygame.time.get_ticks()-start_ticks) / 1000 #convert (ms) to (s) by dividing 1000
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (63, 72, 204))
    screen.blit(timer_title,(screen_width-60,0))
    screen.blit(timer, (screen_width-40,20))

    #Life Count Display
    screen.blit(life_title,(10,0))
    screen.blit(life_count,(15,20))
    
    screen.blit(point_count, ((screen_width/2)+55,5))

    if (total_time - elapsed_time) <= 0:
        print("Time Out!")
        running = False
    #Display Game prompt        
    pygame.display.update() #update run background image


gameover = gameover_font.render("Game Over", False, (255,0,0))
screen.blit(gameover,((screen_width/2)-200,(screen_height/2)-50))
pygame.display.update() #update again for Game over message

#give delay before exit the game
pygame.time.delay(5000) #1000 ms = 1sec

# exit pygame
pygame.quit()
"""