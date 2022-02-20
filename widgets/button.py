# I want to create a button with an image
# capa\ble of entrying a text inside the input frame

# importing built-in classes
from tkinter import Button
from PIL import Image, ImageTk, ImageDraw, ImageFont
from _thread import start_new_thread as snt
# User defined modules
from window import Window

# funtion to pass multiple expressions to lamda
def do(*kwargs):
    pass
# The button images 
buttons = {
    'oper'   : Image.open('widgets/images/button_oper.png'), # 'oper' stands for 'operator'
    'func'   : Image.open('widgets/images/button_func.png'),
    'num'    : Image.open('widgets/images/button_white.png'),
    'oper_on': Image.open('widgets/images/button_oper_on.png'), # 'oper' stands for 'operator'
    'func_on': Image.open('widgets/images/button_func_on.png'),
    'num_on' : Image.open('widgets/images/button_white_on.png'),
    'out'    : Image.open('widgets/images/output_screen.png'),
    'in'     : Image.open('widgets/images/temp_screen.png'),
    'out_on' : Image.open('widgets/images/output_screen.png'),
    'in_on'  : Image.open('widgets/images/temp_screen.png'),
    'mask'   : Image.open('widgets/images/mask_group.png'),
    'menu'   : Image.open('widgets/images/menu.png')
}

# The sizes associated to button type 
sizes = {
    'oper' : 13,
    'func' : 9,
    'num'  : 12,
    'out' : 43,
    'in'  : 20
}

# A fonts dictionnary to ease retrieval
fonts = {
    'segoe_ui_regular'  : lambda size : ImageFont.truetype("fonts/segoe/Segoe UI.ttf", size),
    'segoe_ui_semibold' : lambda size : ImageFont.truetype("fonts/segoe/Segoe UI Semibold.ttf", size),
    'segoe_ui_bold'     : lambda size : ImageFont.truetype("fonts/segoe/Segoe UI Bold.ttf", size)
}

# Buttons for fonts
button_fonts = {
    'oper' : 'segoe_ui_semibold',
    'func' : 'segoe_ui_bold',
    'num'  : 'segoe_ui_bold',
    'out'  : 'segoe_ui_bold',
    'in'   : 'segoe_ui_semibold' 
}

# Colors
text_colour = {
    'oper' : '#000000',
    'func' : '#000000',
    'num'  : '#000000',
    'oper_on' : '#000000',
    'func_on' : '#ffffff',
    'num_on'  : '#000000',
    'out' : '#1A1A1A',
    'in'  : '#707070',
    'out_on' : '#1A1A1A',
    'in_on'  : '#707070'
    }

frame_colour = '#f9f9f9'

# Animated Button
class AnimatedButton(Button):
    def __init__(self, master, **kwargs):
        action = kwargs.get('command', None)             # We have to create a tempory instance of then command 
        kwargs['command'] = lambda: self.animate(action) # in order to use it in animate
        super().__init__(master, **kwargs)

    def animate(self, action=None, depth=5):
        count, size= 0, 0
        self.configure(text='          ')
        def expand():
            nonlocal count, size
            if count < depth:
                size += 1
                #self.config(font=('Helvetica',size))
                x = self.place_info()['x']
                y = self.place_info()['y']
                self.place_configure(y=int(y)-size)
                count += 1
                self.master.after(10, expand)
            else : contract()

        def contract():
            nonlocal count, size
            if count > 0:
                #self.config(font=('Helvetica',size))
                x = self.place_info()['x']
                y = self.place_info()['y']
                self.place_configure(y=int(y)+size)
                count -= 1
                self.master.after(10, contract)
                size -=1
        expand(); 
        # Actioning the button
        if action is not None: 
            #action()
            pass
        else:
            print(f'Button {id(self)} has no action')


# Button used in the calculator
class CalculatorButton(AnimatedButton):
    def __init__(self, master, text, widget=None, button_type = 'oper', **kwargs):
        # Initialise the superclass constructor
        super().__init__(master, borderwidth=0.2, bg = frame_colour, **kwargs)
        # Initialising our button attributes
        self.__initbut__(widget, text, button_type)
        self.configure(command=lambda: do(self.animate(), master.action_key(str(self.text))))
        
    def __initbut__(self, widget, text, button_type):
        # Our self defined attributes
        if button_type not in buttons.keys(): 
            raise Exception(
                f'{button_type} is an invalid button type. Button types are {list(buttons.keys())}'
            )
        self.button_type = button_type
        self.text = text
        self.font = button_fonts[button_type]
        self.im = None
        self.im_on = None
        # Initialise the images
        self.__initimages__(self.button_type)
        # Bindings
        self.bindings()
        # Command
        #self.configure(command=self.animate)
        
    def bindings(self):
        # binding events for color swap
        #self.bind('<Enter>', lambda x: self.configure(image=self.im_on, bg='#ececec', borderwidth=0))
        #if self.button_type != 'func': self.bind('<Enter>', lambda x: do(self.animate(depth=3)))
        if self.button_type != 'func': self.bind('<Enter>', lambda x: do(self.configure(image=self.im_on, borderwidth=0), self.animate(depth=3)))
        else : self.bind('<Enter>', lambda x: do(self.animate(depth=2), self.configure(image=self.im_on, borderwidth=0)))
        
        self.bind('<Leave>', lambda x: snt(self.after, (15, self.configure(image=self.im, bg =frame_colour))))
        self.bind('<MouseWheel>', lambda x: self.__initimages__('num'))
    
    def __initimages__(self, button_type):
        # I take an image an place the associated text
        im = buttons[button_type].copy()
        im_on = buttons[f'{button_type}_on'].copy()
        # draw the text on im
        draw = ImageDraw.Draw(im)
        draw.text((im.size[0]//2, im.size[1]//2), self.text, fill=text_colour[button_type], anchor="mm", font=fonts[self.font](sizes[button_type]))
        # draw the text on im_on
        draw = ImageDraw.Draw(im_on)
        draw.text((im_on.size[0]//2, im_on.size[1]//2), self.text, fill=text_colour[f'{button_type}_on'], anchor="mm", font=fonts[self.font](sizes[button_type]))
        # initialise object << im, im_on >>
        self.im = ImageTk.PhotoImage(im)
        self.im_on = ImageTk.PhotoImage(im_on)
        # place image on widget
        self.configure(image=self.im)
        
def main():
    root = Window()
    root.configure(bg = frame_colour)
    root.geometry('376x663+450+15')
    root.bind('<Configure>', lambda x: print(root.geometry()))
    button = CalculatorButton(root, 'Sketch', button_type='oper', command= lambda: print('it is ok'))
    button.place(x=100, y=100)
    button1 = CalculatorButton(root, '  -  ', button_type='oper', command= lambda: print('it is ok'))
    button1.place(x=100, y=300)
    root.mainloop()

if __name__ == '__main__':
    main()
