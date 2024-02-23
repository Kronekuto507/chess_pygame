from widgets.Button import Button

class SubmitButton(Button):
    def __init__(self,x_pos,y_pos,text,main_surface,base_color,hovering_color):
        super().__init__(x_pos,y_pos,text,main_surface,base_color,hovering_color)
    
    def get_from_text_input(self,*args,**kwargs):
        text_from_inputs = []
        for text_input in args:
            text_from_inputs.append(text_input.get_text())
            text_input.text = ''
        return text_from_inputs[0] if int(len(text_from_inputs)) < 2 else text_from_inputs
