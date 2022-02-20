# importing buit-in modules
from tkinter import Frame, Canvas
from window import Window
from button import frame_colour, AnimatedButton, fonts, CalculatorButton, buttons, sizes, do
from PIL import ImageDraw, Image, ImageTk
from keypad import Keypad
from polynomialparser import evaluate as eval

screen = {
	'out' : Image.open('widgets/images/output_screen.png'),
	'in'  : Image.open('widgets/images/temp_screen.png')
}

# Output class to show text on screen
class TextAjustingButton(CalculatorButton):
	def __init__(self, master, text=' ', button_type='out', maximum=None, **kwargs):
		assert button_type in screen.keys() and (isinstance(maximum, int) or  maximum is None)
		self.maximum = maximum
		# Initialising the super class attributes
		super().__init__(master, text, button_type = button_type, **kwargs)
		self.configure(command=lambda: do(self.animate(), self.imsys.show()))
      
	def bindings(self):
		pass

	def delete(self):
		if self.text != '':
			self.become(self.text[-1])

	def erase(self):
		self.become('')

	def add(self, char):
		self.become(self.text+str(char))

	def become(self, text):
		if text == '': text = ' '
		if not self.maximum :
			self.maximum = sizes[self.button_type]
		self.text = text 
		image = screen[self.button_type].copy()
		draw = ImageDraw.Draw(image)
		fontsize = 1  # starting font size
		W, H = image.size
		# portion of image width you want text width to be
		blank = Image.new('RGB',(W, H))
		font = fonts['segoe_ui_regular'](fontsize)

		while (font.getsize(self.text)[0] < blank.size[0]) and (font.getsize(self.text)[1] < blank.size[1]) and fontsize<self.maximum:
		    # iterate until the text size is just larger than the criteria
		    fontsize += 1
		    font = fonts['segoe_ui_regular'](fontsize)
		# optionally de-increment to be sure it is less than criteria
		fontsize -= 1
		font = fonts['segoe_ui_regular'](fontsize)

		w, h = draw.textsize(self.text, font=font)
		draw.text(((W-w),(H-h)/2), self.text, font=font, fill="black") # put the text on the image
		blank = blank.resize((W*2, H*2))
		drawb = ImageDraw.Draw(blank)
		drawb.text(((W-w),(H-h)/2), self.text, font=font, fill="white")
		self.imsys = blank
		self.im = ImageTk.PhotoImage(image)
		self.im_on = ImageTk.PhotoImage(image)
		self.configure(image=self.im)

	def __initimages__(self, button_type):
		self.become(self.text)

	def get(self):
		return self.text

class ImageCan(Canvas):
	def __init__(self, master, image_name, borderwidth=0, **kwargs):
		self.image = buttons[image_name]
		self.width = self.image.size[0]
		self.height = self.image.size[1]
		self.image = self.image.resize((self.width//2, self.height//2))
		self.width = self.image.size[0]
		self.height = self.image.size[1]
		self.image = ImageTk.PhotoImage(self.image)
		super().__init__(master, width=self.width, height=self.height, borderwidth=borderwidth, **kwargs)
		self.create_image(self.width/2, self.height/2, image=self.image)
		
class Screen(Frame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		self.expression = ''
		self.list_exp = []
		self.__initUI__()

		# for writing inside attributes
		index = 0
		self.erase = 1

	def __initUI__(self):

		self.output = TextAjustingButton(self, text='0', button_type='out')
		self.output.erase()
		self.input= TextAjustingButton(self, text='0', button_type='in')
		#self.expression = TextAjustingButton(self, text='Expression', button_type='in', maximum=11)
		self.tIndication = TextAjustingButton(self, 'Your expression will show up here', 'in', maximum=12)
		self.bIndication = TextAjustingButton(self, ' ', 'in', maximum=12)
		self.mask = ImageCan(self, 'mask', bg=frame_colour)
		self.menu_image = ImageTk.PhotoImage(buttons['menu'])
		self.menu = AnimatedButton(self, image=self.menu_image, borderwidth=0, bg=frame_colour)
		# Placing the widgets

	def treat_key(self, key):
		if self.erase:
			self.expression = ''
			self.output.erase()
			self.input.erase()
			self.erase = 0
		if key == 'DEL':
			if self.expression != '':
				self.expression = self.expression[:-1]
				self.list_exp = self.split(self.expression)
				self.input.become(''.join(self.list_exp[:-1]))
				#self.output.become(''.join(self.list_exp[-1]))
				self.output.become(self.list_exp[-1])
			#self.output.become(self.expression)
		elif key.isdigit() or key in '}{.^/*+-X':
			if (key in '-+') and ('{' not in self.list_exp[-1]) and False:
				if len(self.expression):
					self.expression = str(eval(self.expression))
					self.input.become(self.expression)
					self.output.become(self.expression)
			self.expression += key
			self.list_exp = self.split(self.expression)
			print(self.list_exp)
			if len(self.list_exp) !=1 : self.input.become(' '.join(self.list_exp[:-1]))
			self.output.become(''.join(self.list_exp[-1]))
		elif key == 'C':
			if len(self.list_exp) !=0:
				self.list_exp = self.list_exp[:-1]
				self.expression = ' '.join(self.list_exp)
				if  len(self.list_exp):
					self.input.become(' '.join(self.list_exp[:-1]))
					self.output.become(''.join(self.list_exp[-1]))
				else:
					self.input.become('')
					self.output.become('')
		elif key == 'CE':
			self.expression = ''
			self.list_exp = self.split(self.expression)
			self.input.become('')
			self.output.become('')
		elif key == '=':
			self.expression = str(eval(self.expression))
			self.list_exp = self.split(self.expression)
			self.input.become('')
			self.output.become(self.expression)
		elif key == 'SOLVE':
			self.expression = str(eval(self.expression).roots())
			self.input.become('')
			self.output.become(self.expression)
		elif key == 'FACTORISE':
			self.expression = str(eval(self.expression).factorise())
			self.input.become('')
			self.output.become(self.expression)
		elif key == 'INTEGRATE':
			self.expression = str(eval(self.expression).integrate())
			self.input.become('')
			self.output.become(self.expression)
		elif key == 'DIFFERENTIATE':
			self.expression = str(eval(self.expression).differentiate())
			self.input.become('')
			self.output.become(self.expression)
			
	def split(self, expression):
		output = expression[::]
		for char in set(expression):
			if char in '+-' : 
				output = output.replace(char, f' {char} ')
				output = output.replace('  ', ' ')
		return output.split(' ')

	def pack(self, **kwargs):
		self.input.pack()
		self.output.pack()
		super().pack(**kwargs)
	
		"""#self.output.place(x=100, y=106))
								#self.input.place(x=100, y=83)"""
	def place(self, **kwargs):
		self.output.place(x=10, y=106)
		self.input.place(x=10, y=83)
		self.tIndication.place(x=10, y=65)
		self.mask.place(x=325, y=170)
		self.menu.place(x=25, y=27)
		#self.menu.pack()
		super().place(**kwargs)

def main():
    root = Window()
    root.configure(bg=frame_colour)
    #root.configure(bg = frame_colour)
    root.geometry('376x671+450+15')
    root.resizable(width=False, height=False)
    #root.bind('<Configure>', lambda x: print(root.geometry()))
    screen = Screen(root, width=376, height=240, bg=frame_colour)
    screen.place(x=0, y=0)
    pad = Keypad(root, screen=screen, borderwidth=9, padx=0, pady=0)
    pad.place(x=0, y=241)
    root.bind('<Key>', pad.action_key)
    
    
    root.mainloop()

if __name__ == '__main__':
	main()
