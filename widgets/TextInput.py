import pygame
import sys

class TextInput():
    base_font = pygame.font.SysFont("Arial",32)
    def __init__(self,pos_x,pos_y,screen,text_input_id, width,hide_text = False):

        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text_input_id = text_input_id
        self.width = width
        self.input_rect = pygame.Rect(self.pos_x,self.pos_y,160,40)

        self.color_selected = pygame.Color('lightskyblue3')
        self.color_unselected = pygame.Color('gray15')
        self.color = self.color_selected
        self.is_selected = False
        self.screen = screen
        self.text = ''
        self.hide_text = hide_text

    def get_text(self,unicode_character):
        self.text += unicode_character

    def render(self):
        pygame.draw.rect(self.screen,self.color,self.input_rect,2)
        
        showable_text = ''

        if self.hide_text:
            showable_text = ''
            for _ in range(int(len(self.text))):
                showable_text += '*'
        else:
            showable_text = self.text
                
        #Mostrar en pantalla cuando se agrega al text input
        text_surface = TextInput.base_font.render(showable_text,True,(255,255,255))
        self.screen.blit(text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(self.width,text_surface.get_width() + 10)

    def delete_char(self):
        self.text = self.text[:-1]
    
    def select_text_input(self,mouse_position):
        if (mouse_position[0] in range(self.input_rect.left,self.input_rect.right) and mouse_position[1] 
        in range(self.input_rect.top,self.input_rect.bottom)):
            self.is_selected = True
            self.color = self.color_selected
            return self.is_selected
        
        self.is_selected = False
        self.color = self.color_unselected
        return self.is_selected

    def return_text(self):
        return self.text
    
    def return_id(self):
        return self.text_input_id
    
    def restart_text(self):
        self.text = ''


        