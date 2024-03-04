import pygame
from pygame import locals

WIDTH = 600
HEIGHT = 600

SCREEN_CENTER = WIDTH/2

VERDE = pygame.Color(118,150,86) #Verde
CREMA = pygame.Color(238,238,210) #Crema
ROWS,COLS = 8,8
SIZE = WIDTH//COLS
DIM_GREY= (189,195,199,0.7)
TRANSPARENT_GREEN = (0,255,0)
TRANSPARENT_BLUE = (30,144,255)
TRANSPARENT_RED= (255,0,0)
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
BG_1 = pygame.image.load(r".\images\chess_bg.jpg").convert_alpha()
primary_database = "user_info.sqlite"


