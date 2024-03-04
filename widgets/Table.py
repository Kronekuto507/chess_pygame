import pygame

class Table:
    dx = 50
    dy = 10
    def __init__(self,screen,no_of_rows,no_of_cols,width,height,x0,y0,division = None):
        self.screen = screen
        self.no_of_rows = no_of_rows
        self.no_of_cols = no_of_cols
        self.width = width
        self.height = height
        self.x0 = x0
        self.y0 = y0
        self.division = division
        self.blocks = None
    
    def render(self):
        blocks = []
        limit =  0
        difference = 0

        last_x0 = 0
        last_y0 = 0
        #Si existe un limite, construir en base a tal limite
        if self.division != None:
            limit = self.division
            difference = self.no_of_cols = limit
        else:
            limit = self.no_of_cols

        for row in range(self.no_of_rows):
            for col in range(limit):
                last_x0 = self.x0 + col*Table.dx
                last_y0 = self.y0 + row *Table.dy
                rect = pygame.Rect(last_x0,last_y0,self.width,self.height)
                blocks.append(rect)
        
        if self.division != None:
            for col in range(difference):
                rect = pygame.Rect(last_x0 + col*Table.dx,last_y0,self.width,self.height*2)
                blocks.append(rect)
        
        for rect in blocks:
            pygame.draw.rect(self.screen,(255,255,255),rect)
        
        self.blocks = blocks

