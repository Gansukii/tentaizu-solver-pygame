import pygame
import sys
from itertools import combinations

class puzzle_solver:
    def __init__(self,surface,grid_coordinates):
        self.surface = surface
        self.grid_coordinates = grid_coordinates
        
    GRID_SIDE = 420
    BOX_SIZE = GRID_SIDE // 7 
    puzzle = []
    skips = set({})
    taken = set({})
    done = False

    def check(self,i,j):
        if i == 0 and j==0:
            return [(0,1),(1,0),(1,1)]
        elif i == 0 and j == 6:
            return [(0,5),(1,6),(1,6)]
        elif i == 6 and j == 0:
            return [(5,0),(5,1),(6,1)]
        elif i == 6 and j == 6:
            return [(5,5),(5,6),(6,5)]
        elif i == 0:
            return [(0,j-1),(0,j+1),(1,j-1),(1,j),(1,j+1)]
        elif i == 6:
            return [(5,j-1),(5,j),(5,j+1),(6,j-1),(6,j+1)]
        elif j == 0:
            return [(i-1,0),(i+1,0),(i-1,1),(i,1),(i+1,1)]
        elif j == 6:
            return [(i-1,6),(i+1,6),(i-1,5),(i,5),(i+1,5)]
        else:
            return [(i-1,j-1),(i-1,j),(i-1,j+1),
                    (i,j-1),(i,j+1),
                    (i+1,j-1),(i+1,j),(i+1,j+1)]

    def initial_check(self,given):
        self.puzzle = given.copy()
        self.skips = set({})
        self.taken = set({})
        for i in range (7):
            for j in range(7):
                if given[i][j] == '0':
                    zeros = self.check(i, j)
                    for x in zeros:
                        self.taken.add(x)
                    self.taken.add((i, j))
                elif given[i][j] != '.':
                    self.taken.add((i,j))

    def print_given(self,given):
        for i in range (7):
            print('-----------------------------')
            for j in range(7):
                if j == 0:
                    print("|",end = ' ')
                if given[i][j] == '.':
                    print("  |", end = ' ')
                    continue
                print(given[i][j],"|",end=' ')
            print()
        print('-----------------------------')

    def add_taken(self,arr):
        for i in arr:
            self.taken.add(i)
        
    def modify_taken(self,arr):
        newarr = arr.copy()
        for x in arr:
            if x in self.taken:
                newarr.remove(x)
        return newarr

    def remove_taken(self,arr):
        for i in arr:
            if i in self.taken:
                self.taken.remove(i)

    def draw_star(self,x,y):
        star_img = pygame.image.load("star.png")
        self.surface.blit(star_img,
                    (self.grid_coordinates[x][y][0]+((self.BOX_SIZE-star_img.get_rect().width)//2),
                    self.grid_coordinates[x][y][1]+(self.BOX_SIZE-star_img.get_rect().height)//2))

    def remove_star(self,x,y):
        rect = pygame.Rect(self.grid_coordinates[x][y][0]+6,
                           self.grid_coordinates[x][y][1]+6,
                           48,48)
        pygame.draw.rect(self.surface, (255,255,255), rect)
        

    def solve_puzzle(self,stars,given):
        pygame.event.get()
        global done
        for i in range(7):
            for j in range(7):
                ijcoord = (i, j)
                if ijcoord in self.skips:
                    continue
                if given[i][j] == '0':
                    continue
                if given[i][j] != '.' and given[i][j] != '*':
                    clue = int(given[i][j])
                    arr = self.check(i,j)
                    for item in arr:
                        if given[item[0]][item[1]] == '*':
                            clue -= 1
                            if clue < 0:
                                return
                    newarr = self.modify_taken(arr)
                    newarrpos = list(combinations(newarr,clue))
                    if clue == 0:
                        self.add_taken(newarr)
                        self.skips.add((i,j))
                        self.solve_puzzle(stars,given)   
                        self.remove_taken(newarr)
                        self.skips.remove((i, j))
                        return
                    if clue > 0:
                        if len(newarrpos) == 0:
                            return
                        for x in newarrpos:
                            for coord in x:
                                given[coord[0]][coord[1]] = '*'
                                if not self.done:
                                    self.draw_star(coord[0],coord[1])                            
                            if not self.done:
                                pygame.display.update()
                                pygame.time.delay(200)
                            stars += clue
                            if stars > 10:
                                for coord in x:
                                    given[coord[0]][coord[1]] = '.'
                                    if not self.done:
                                        self.remove_star(coord[0],coord[1])                                
                                if not self.done:
                                    pygame.display.update()
                                    pygame.time.delay(200)
                                return
                            self.add_taken(newarr)
                            self.skips.add((i,j))
                            self.solve_puzzle(stars,given)
                            stars -= clue
                            for coord in x:
                                given[coord[0]][coord[1]] = '.' 
                                if not self.done:
                                    self.remove_star(coord[0],coord[1])        
                            if not self.done:
                                pygame.display.update()
                                pygame.time.delay(200)
                        self.remove_taken(newarr)
                        self.skips.remove((i, j))
                        return

        self.done = True

