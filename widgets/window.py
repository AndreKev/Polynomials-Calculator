# Interactive window

# Importing built-in modules
from tkinter import Tk
from time import time
import _thread
class Window(Tk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    """    self.__initUI__()
                    
                        def __initUI__(self):
                            self.overrideredirect(True)
                            self.bind('<Motion>', self.show_move_titlebar)
                    
                        def show_move_titlebar(self, event):
                            show = False if event.y < 3 else True
                            self.overrideredirect(show)
                    """        
#root = Window()
