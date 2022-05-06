import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class ChessBoard(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 8
		for k in range(8):
			for v in range(8):
				if ((k + v) % 2) == 0:
					self.add_widget(
						Button(
							background_normal = '',
							background_down = '',
							text = key_to_str[board[k][v]],
							font_size = 32,
							color = (1, 0, 0, 1),
							background_color = (1, 1, 1, 1)))

				else:
					self.add_widget(
						Button(
							background_normal = '',
							background_down = '',
							text = key_to_str[board[k][v]],
							font_size = 32,
							color = (1, 0, 0, 1),
							background_color = (0, 0, 0, 1)))

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
		-3 : "k",
		-4 : "b",
		-5 : "q",
		-6 : "k",
		0 : " ",
		1 : "P",
		2 : "R",
		3 : "K",
		4 : "B",
		5 : "Q",
		6 : "K",	
	}

def initBoard():
	global board
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

def moveRook(y,x,yy,xx):
	if (x == xx and y != yy) or (y == yy and x != xx): 
		yCoords = sortVal(y,yy)
		xCoords = sortVal(x,xx)
		for i in range(xCoords[0] + 1, (xCoords[1] - 1)): #we do not want to check the initial or final positions for occupied pieces, hence the +1/-1
			if getPiece(yy, i) != 0:
				return 0
		for i in range(yCoords[0] + 1, (yCoords[1] - 1)):
			if getPiece(xx, i) != 0:
				return 0		
		return 1

def moveBishop(y,x,yy,xx): #TODO: check piece hopping
	if (abs(xx - x) == abs(yy - y)) and (y != yy and x != xx):
		return 1

def checkMoveValid(y,x,yy,xx): #checks ONLY for movement shape validity;
	piece = abs(getPiece(y,x))
	#have this stupid ass elif tree because python 3.10 does not support win7 and python got switch statements A WEEK AGO
	if piece == 1: #pawn
		return (yy - y) == 1 * -getPiece(y,x) #TODO: check for 2 space move from initial position; check if next place is blocks; check for diagonal capture

	elif piece == 2: #rook
		return moveRook(y,x,yy,xx)

	elif piece == 3: #knight
		if ((abs(xx - x) == 1) and (abs(yy - y) == 2)) or ((abs(xx - x) == 2) and (abs(yy - y) == 1)):
			return 1

	elif piece == 4: #bishop
		return moveBishop(y,x,yy,xx)

	elif piece == 5: #queen
		if moveBishop(y,x,yy,xx) or moveRook(y,x,yy,xx):
			return 1

	elif piece == 6: #king
		if abs(xx - x) == 1 or abs(yy - y) == 1:
			return 1
	return 0

def updateBoard(y,x,yy,xx): #update board position and clean out previous position on board
	board[yy][xx] = board[y][x] 
	board[y][x] = 0
	#TODO: check for gamestates (e.g check, checkmate, etc)

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
	print(str(getPiece(y,x)))
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

	"""
	play = True
	while play == True:
		if shellInterface() == False:
			play = False
	
	return
"""

if __name__ == '__main__': main()