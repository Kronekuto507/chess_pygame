import pygame
import sys

class Button():
    main_font = pygame.font.SysFont("cambria",50)
    height = 35
    width = 100
    def __init__(self,x_pos,y_pos,text,main_surface,base_color,hovering_color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        #Atirbuto que representa la superficie del boton
        self.surface_color = pygame.Surface((Button.width,Button.height),pygame.SRCALPHA)
        #Coordenadas de la superficie
        self.rect = self.surface_color.get_rect(center = (self.x_pos,self.y_pos))

        self.text_input = text
        self.text = Button.main_font.render(self.text_input,True,'white')
        self.text_rect = self.text.get_rect(center = (self.x_pos,self.y_pos))
        self.main_surface = main_surface
        self.base_color = base_color
        self.hovering_color = hovering_color

    def draw_button(self):
        #Inicializar superficie transparente
        
        alpha_value = 100
        color = (0,0,0) + (alpha_value,)
        self.surface_color.fill(color)
        #Crear coordenadas rectangulares
        
        #Dibujar boton
        self.main_surface.blit(self.surface_color,self.rect)
        self.main_surface.blit(self.text,self.text_rect)
    
    def check_input(self,position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            return True
        return False

    def hover(self, position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            self.text = Button.main_font.render(self.text_input,True,self.hovering_color)
        else:
            self.text = Button.main_font.render(self.text_input,True,self.base_color)