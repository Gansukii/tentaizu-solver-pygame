import pygame
import sys
import random
from solver import puzzle_solver
from rect_create import rect_create

def display_grid(given):
    print(given)
    for i in range(7):
        grid_line = []
        for j in range(7):
            pygame.time.delay(10)
            myrect = pygame.Rect((j*(BOX_SIZE)+60), 40 + (i*BOX_SIZE) , BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(surface, L_BLUE, myrect, 3)
            grid_line.append((j*(BOX_SIZE)+60, 40 + (i*BOX_SIZE)))
            if given[i][j] != '.':
                font = pygame.font.SysFont('Comic Sans', 45)
                text_value = font.render(given[i][j], True, (0,0,0))
                surface.blit(text_value,
                             ((j*(BOX_SIZE) + (BOX_SIZE//2)-(text_value.get_rect()[3]//4)) +60 ,
                             10 + (i*BOX_SIZE) + (text_value.get_rect()[2])))
            pygame.display.update()
        line = grid_line.copy()
        grid_coordinates.append(line)
        
f = open("tentaizugiven.txt","r")
puzzle_collection = []
given = []
container = []
counter = 0
for line in f.read():
    if counter == 7:
        counter = 0
        given_append = given.copy()
        puzzle_collection.append(given_append)
        given.clear()
        continue
    if line == '\n':
        container_append = container.copy()
        given.append(container_append)
        container.clear()
        counter+=1
    else:
        container.append(line)

container_append = container.copy()
given.append(container_append)
given_append = given.copy()
puzzle_collection.append(given_append)
f.close()

##254, 228, 64    241, 91, 181

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 600
WHITE =(255,255,255)
L_BLUE = (0, 187, 249)
DARKER = (155, 93, 229)
GRID_SIDE = 420
BOX_SIZE = GRID_SIDE // 7 
enable_generate = True
solve = False
grid_coordinates = []
puzzle = []


pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
surface.fill(WHITE)
rect_create = rect_create(surface)
pygame.display.set_caption("Tentaizu!")
font = pygame.font.Font('Rubik-Medium.ttf', 35) 
title = font.render('TENTAIZU SOLVER', True, (0, 0, 128))
star_img = pygame.image.load("bigstar.png")
surface.blit(star_img,(0,0))
generate_btn = rect_create.create_generate_button()
solver = puzzle_solver(surface,grid_coordinates)


while True:
    surface.blit(title,(125,5))
    rect_create.draw_rect(60,40,GRID_SIDE,GRID_SIDE, L_BLUE, 3) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN and solve:
            solve= False
            if event.key == pygame.K_SPACE:
                font = pygame.font.Font('SourceSansPro-Regular.otf', 20)
                rect_create.draw_rect((SCREEN_WIDTH - font.size("Press 'SPACE' to solve")[0])//2,
                          480, font.size("Press 'SPACE' to solve")[0],
                          font.size("Press 'SPACE' to solve")[1], WHITE, 0)
                solver.initial_check(puzzle)
                solver.solve_puzzle(0,puzzle)
                solver.done = False
                generate_btn = rect_create.create_generate_button()
                enable_generate = True
            
        if event.type == pygame.MOUSEBUTTONDOWN and enable_generate:
            mouse_pos = event.pos
            if generate_btn.collidepoint(mouse_pos):
                rect_create.draw_rect(60, 40, GRID_SIDE, GRID_SIDE, WHITE, 0)
                rect_create.draw_rect(60, 40, GRID_SIDE, GRID_SIDE, L_BLUE, 3)
                rect_create.draw_rect(60, 480, 152, 37, WHITE, 0)
                enable_generate = False
                puzzle = puzzle_collection[random.randint(0,len(puzzle_collection)-1)]
                display_grid(puzzle)
                solve = True
                font = pygame.font.Font('SourceSansPro-Regular.otf', 20)
                solve_txt = font.render("Press 'SPACE' to solve", True, (0, 0, 128))
                surface.blit(solve_txt, ((SCREEN_WIDTH - font.size("Press 'SPACE' to solve")[0])//2,480))

    pygame.display.update()







