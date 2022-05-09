import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class ChessBoard(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 8

		def callback(instance):
			global numCellSelected
			global coordSelected
			global coordDestination
			global buttonArray

			numCellSelected += 1

			if numCellSelected == 1:
				coordSelected = (instance.by, instance.bx)
				instance.color = (0, 1, 0, 1)
			elif numCellSelected == 2:
				coordDestination = (instance.by, instance.bx)
				if not movePiece(coordSelected[0], coordSelected[1], coordDestination[0], coordDestination[1]):
					print("invalid move")
				else:
					updateBoard(coordSelected[0], coordSelected[1], coordDestination[0], coordDestination[1])
					buttonArray[coordDestination[0]][coordDestination[1]].text = buttonArray[coordSelected[0]][coordSelected[1]].text
					buttonArray[coordSelected[0]][coordSelected[1]].text = ""
				buttonArray[coordSelected[0]][coordSelected[1]].color = (1, 0, 0, 1)
				numCellSelected = 0
				


		global buttonArray
		buttonArray = [[0 for i in range(8)] for i in range(8)]

		for i in range(8):
			for j in range(8):
				b = Button()
				b.by = i
				b.bx = j
				
				b.bind(on_press = callback)

				#b.background_normal = 'resource/image/block.png'
				b.background_down = ''
				b.text = key_to_str[board[i][j]]
				b.font_size = 32
				b.color = (1, 0, 0, 1)
				b.background_color = (1, 1, 1, 1)
				if ((i + j) % 2):
					b.background_color = (0.3, 0.3, 0.3, 1)
				self.add_widget(b)
				buttonArray[i][j] = b

		#print(self.children)
		
				
				
						

class MainWidget(Widget):
	pass

class ChessApp(App):
	pass

### PIECE VALUES ###
# 0          !EMPTY#
# 1            PAWN#
# 2            ROOK#
# 3          KNIGHT#
# 4          BISHOP#
# 5           QUEEN#
# 6            KING#
# ---------------- #
# POLARITY DECIDES #
#   PIECE  COLOR   # 
####################

key_to_str = {
		-1 : "p",
		-2 : "r",
		-3 : "n",
		-4 : "b",
		-5 : "q",
		-6 : "k",
		0 : " ",
		1 : "P",
		2 : "R",
		3 : "N",
		4 : "B",
		5 : "Q",
		6 : "K",	
	}

def initBoard():
	global board
	global numCellSelected
	global coordSelected
	global coordDestination

	numCellSelected = 0
	coordSelected = (0,0)
	coordDestination = (0,0)

	board = [2,3,4,5,6,4,3,2],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,3,4,5,6,4,3,2]
	
	#[2,3,4,5,6,4,3,2], --black--
	#[1,1,1,1,1,1,1,1],
	#[0,0,0,0,0,0,0,0],
	#[0,0,0,0,0,0,0,0],
	#[0,0,0,0,0,0,0,0],
	#[0,0,0,0,0,0,0,0],
	#[1,1,1,1,1,1,1,1],
	#[2,3,4,5,6,4,3,2]  --white--

	

	for i in range(2):
		for j in range(8):
			board[i][j] *= -1

def getPiece(y,x):
	return board[y][x]


def sortVal(a,b):
	if a > b:
		return (b,a)
	else:
		return (a,b)

def oppositeSigns(a, b):
    return ((a ^ b) < 0)

def moveRook(y,x,yy,xx):
	if (x == xx and y != yy) or (y == yy and x != xx):
		yCoords = sortVal(y,yy)
		xCoords = sortVal(x,xx)

		for i in range(xCoords[0] + 1, xCoords[1]): #we do not want to check the rook itself for occupied pieces, hence the +1
			if getPiece(yy, i) != 0:
				return 0
		for i in range(yCoords[0] + 1, yCoords[1]):
			if getPiece(i, xx) != 0:
				return 0
		return 1

def moveBishop(y,x,yy,xx): #TODO-mid: check piece hopping
	if (abs(xx - x) == abs(yy - y)) and (y != yy and x != xx):
		yCoords = sortVal(y,yy)
		xCoords = sortVal(x,xx)
		yUp = (((y < yy) * 2) - 1)
		xUp = (((x < xx) * 2) - 1)

		for i in range(1, xCoords[1] - xCoords[0]): #using x or y is arbitary, this just gets the difference in movement
			if getPiece(y + (i * yUp), x + (i * xUp)) != 0:
				return 0
		return 1

def checkMoveValid(y,x,yy,xx): 
	piece = abs(getPiece(y,x))
	#have this stupid ass elif tree because python 3.10 does not support win7 and python got switch statements A WEEK AGO
	if piece == 1: #pawn
		if (yy - y) == 1 * -getPiece(y,x): #only check if verticality is correct
			if (xx == x) and (getPiece(yy,xx) == 0):
				return 1
			elif ((xx - x == 1 or x - xx == 1) and getPiece(yy,xx) != 0) and (oppositeSigns(getPiece(y,x), getPiece(yy,xx))): #diagonal capture
				return 1
		elif (yy - y) == 2 * -getPiece(y,x) and y == 3.5 + (2.5 * getPiece(y,x)): #move 2 from start position
			return 1

	elif piece == 2: #rook
		return moveRook(y,x,yy,xx)

	elif piece == 3: #knight
		if ((abs(xx - x) == 1) and (abs(yy - y) == 2)) or ((abs(xx - x) == 2) and (abs(yy - y) == 1)):
			return 1

	elif piece == 4: #bishop
		return moveBishop(y,x,yy,xx)

	elif piece == 5: #queen
		return (moveRook(y,x,yy,xx) or moveBishop(y,x,yy,xx))

	elif piece == 6: #king
		if abs(xx - x) == 1 or abs(yy - y) == 1:
			return 1
	return 0

def updateBoard(y,x,yy,xx): #update board position and clean out previous position on board
	board[yy][xx] = board[y][x] 
	board[y][x] = 0
	#TODO-low: check for gamestates (e.g check, checkmate, etc)

def movePiece(y,x,yy,xx):
	if not checkMoveValid(y,x,yy,xx):
		return False
	elif (getPiece(y,x) > 0 and getPiece(yy,xx) > 0) or (getPiece(y,x) < 0 and getPiece(yy,xx) < 0): #checks if piece captures its own team
		return False
	else:
		return True
		

def shellInterface():
	for i in range(len(board)):
			print(board[i])
	y = int(input("move from y pos: "))
	x = int(input("move from x pos: "))
	print(key_to_str[getPiece(y,x)])
	yy = int(input("move to y pos: "))
	xx = int(input("move to x pos: "))
	if not movePiece(y,x,yy,xx):
		print("invalid move")
	else:
		updateBoard(y,x,yy,xx)

	if int(input("continue playing?: \n1 = yes 0 = no\n")) == 0:
		return False
	else:
		return True

def main():
	initBoard()

	ChessApp().run()

	debug = False
	if debug:
		play = True
		while play == True:
			if shellInterface() == False:
				play = False
	
	return


if __name__ == '__main__': main()