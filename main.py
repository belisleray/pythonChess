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
							background_color = (1, 1, 1, 1)))

				else:
					self.add_widget(
						Button(
							background_normal = '',
							background_down = '',
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

def moveRook(y,x,yy,xx):
	if (x == xx and y != yy) or (y == yy and x != xx): #TODO: check if hopping over piece (for i in range(a,b) will not run if a > b, so write function to swap these if moving to a lower indice)
		return 1

def moveBishop(y,x,yy,xx): #TODO: check piece hopping
	if (abs(xx - x) == abs(yy - y)) and (y != yy and x != xx):
		return 1

def checkMoveValid(y,x,yy,xx): #checks ONLY for movement shape validity;
	piece = abs(getPiece(y,x))
	#have this stupid ass elif tree because python 3.10 does not support win7 and python got switch statements A WEEK AGO
	if piece == 0: #empty
		return 0

	elif piece == 1: #pawn
		return (yy - y) == 1 * -piece #TODO: check for 2 space move from initial position

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
	if not (checkMoveValid(y,x,yy,xx)):
		return False
	elif (getPiece(y,x) > 0 and getPiece(yy,xx) > 0) or (getPiece(y,x) < 0 and getPiece(yy,xx) < 0): #checks if piece captures its own team
		return False
	else:
		return True
		

def shellInterface():
	for i in range(len(board)):
			print(board[i])
	y = int(input("move from row: "))
	x = int(input("move from column: "))
	print(str(getPiece(y,x)))
	yy = int(input("move to row: "))
	xx = int(input("move to column: "))
	if checkMoveValid(y,x,yy,xx) == 0:
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

	'''
	play = True
	while play == True:
		if shellInterface() == False:
			play = False
	'''
	return


if __name__ == '__main__': main()