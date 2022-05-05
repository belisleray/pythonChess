"""
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ChessGame(Widget):
	pass


class ChessApp(App):
	def build(self):
		return ChessGame()
"""


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
	if (x == xx and y != yy) or (y == yy and x != xx):
		return 1

def moveBishop(y,x,yy,xx):
	if (abs(xx - x) == abs(yy - y)) and (y != yy and x != xx):
		return 1

def movePiece(y,x,yy,xx): #have this stupid ass elif tree because python 3.10 does not support win7 and python got switch statements A WEEK AGO
	piece = getPiece(y,x)
	if piece == 0: #empty
		return 0

	elif piece == 1: #pawn
		return (yy - y) == 1 * -piece

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

def main():
	#test
	return

if __name__ == '__main__': main()