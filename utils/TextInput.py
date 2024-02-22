import pygame
import sys

class TextInput():
    base_font = pygame.font.Font(None,32)
    max_text_size = 160
    def __init__(self,pos_x,pos_y,screen):

        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.input_rect = pygame.Rect(self.pos_x,self.pos_y,160,40)

        self.color_selected = pygame.Color('lightskyblue3')
        self.color_unselected = pygame.Color('gray15')
        self.color = self.color_selected
        self.is_selected = False

        self.text = ''

    def get_text(self,unicode_character):
        self.text += unicode_character

    def render_text_input(self):
        pygame.draw.rect(self.screen,self.color,self.rect,2)

        text_surface = TextInput.base_font.render(self.text,True,(255,255,255))
        self.screen.blit(text_surface,(self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(TextInput.max_text_size,self.text.get_width() + 10)

    def delete_char(self):
        self.text = self.text[:-1]
    
    def select_text_input(self,mouse_position,pressed):
        if (mouse_position[0] in range(self.input_rect.left,self.input_rect.right)
        and mouse_position[1] in range(self.input_rect.top,self.input_rect.bottom) 
        and pressed == 1):
            self.is_selected = True
        
        self.is_selected = False


        