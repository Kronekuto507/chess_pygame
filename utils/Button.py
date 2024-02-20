import pygame
import sys

class Button():
    main_font = pygame.font.SysFont("cambria",50)
    def __init__(self,x_pos,y_pos,text,main_surface):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text
        self.text = Button.main_font.render(self.text_input,True,'white')
        self.text_rect = self.text.get_rect(center = (self.x_pos,self.y_pos))
        self.main_surface = main_surface
    
    def draw_button(self):
        pass