from tkinter import Frame
from window import Window
from button import CalculatorButton, frame_colour, do


# keypad entry for application
standard_disposition = [
	[('Integrate', 'func', (0, 241)), 	('Differentiate', 'func', (93, 241)), ('Sketch', 'func', (186, 241)), ('Factorise', 'func', (279, 241))	], 
	[('Solve', 'oper', (0, 268)), 	('CE', 'oper', (93, 268)), 	  ('C', 'oper', (186, 268)), 	  ('DEL', 'oper', (279, 268))		], 
	[('{', 'oper', (0, 335)), 		('}', 'oper', (93, 335)), 	  ('^', 'oper', (186, 335)), 	  ('/', 'oper', (279, 335))			], 
	[('7', 'num', (0, 400)), 		('8', 'num', (93, 400)), 	  ('9', 'num', (186, 400)), 	  ('*', 'oper', (279, 400))			], 
	[('4', 'num', (0, 465)), 		('5', 'num', (93, 465)), 	  ('6', 'num', (186, 465)), 	  ('-', 'oper', (279, 465))			], 
	[('1', 'num', (0, 531)), 		('2', 'num', (93, 531)), 	  ('3', 'num', (186, 531)), 	  ('+', 'oper', (279, 531))			], 
	[('0', 'num', (0, 597)), 		('.', 'oper', (93, 597)), 	  ('X', 'num', (186, 597)),	  ('=', 'oper', (279, 597))			]
]

keycodes = {
	8  : 'del',
	46 : 'del',
	73 : 'integrate',
	68 : 'differentiate',
	83 : 'sketch',
	70 : 'factorise',
	82 : 'solve',
	88 : 'var x',
	80 : '^',
	69 : 'ce',
	57 : '{',
	48 : '}',
	219: '{',
	221: '}',
	13 : '='
}
class Keypad(Frame):
	def __init__(self, master, screen=None, width=376, height=430, bg=frame_colour, **kwargs):
		super().__init__(master, width=width, height=height, bg=frame_colour, **kwargs)
		self.widgets = {}
		self.screen = screen
		self.create(standard_disposition)
		
	def islinked(self):
		pass
	def ispro(self):
		pass
	def is_standard(self):
		pass

	def create(self, standard_disposition):
		for i in range(len(standard_disposition)):
			for j in range(len(standard_disposition[i])):
				self.widgets[standard_disposition[i][j][0].upper()] = CalculatorButton(self, text=standard_disposition[i][j][0], button_type=standard_disposition[i][j][1])
				#widgets[i][j].place(x=standard_disposition[i][j][2][0], y=standard_disposition[i][j][2][1])
				self.widgets[standard_disposition[i][j][0].upper()].place(x=standard_disposition[i][j][2][0]-8, y=standard_disposition[i][j][2][1]-245)

	def action_key(self, event):
		key = event.char if not isinstance(event, str) else event
		key = key.upper()
		if key in [k.upper() for k in self.widgets.keys()]:
			self.widgets[key].animate()
			self.widgets[key].configure(image=self.widgets[key].im_on)
			if self.screen:
				self.screen.treat_key(key)
			else: print('No screen')
			#rself.widgets[key].invoke()
			#self.widgets[key].configure(image=self.widgets[key].im)
		else:
			if event.keycode in keycodes.keys():
				self.action_key(keycodes[event.keycode])
				if self.screen: 
					self.screen.treat_key(keycodes[event.keycode])
				else: print('No screen')
			else:
				print(type(event.keycode), event.keycode)



				


def main():
    root = Window()
    #root.configure(bg = frame_colour)
    root.geometry('376x671+450+15')
    root.wm_attributes('-transparentcolor', '#ab23ff')
    root.resizable(width=False, height=False)
    #root.bind('<Configure>', lambda x: print(root.geometry()))
    """button = CalculatorButton(root, 'Sketch', button_type='oper', command= lambda: print('it is ok'))
                print(button['text'])
                button.pack()"""
    pad = Keypad(root, borderwidth=9, bg=frame_colour, width=376, height=422, padx=0, pady=-1)
    root.bind('<Key>', pad.action_key)
    pad.place(x=standard_disposition[0][0][2][0], y=standard_disposition[0][0][2][1])
    #pad.place(x=0, y=0)
    root.mainloop()

if __name__ == '__main__':
    main()
