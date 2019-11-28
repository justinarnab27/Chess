import cv2              #import OpenCV
import numpy as np      #import numpy

d = 60                  #The dimension of each square.
	
                        #We are using 60*60 pixel images for each square
dark =[0.235,0.529,0.709]
light = [0.54,0.79,0.949]

def d_or_l(px,py):
	'''Returns if (px,py) in light square or dark
	Return "light" or "dark" '''
	r,c = which_square(px,py)
	if((r+c)%2==0):
		return 'light'
	else:
		return 'dark'

def create_board():
	'''Creates the initial board. Returns (d*8)*(8*d) image of board'''
	img = np.zeros((8*d,8*d,3))
	for i in range(8):
		for j in range(8):
			for k in range(d):
				for l in range(d):
					val = dark
					if (i+j)%2 == 0:
					 val = light
					img[i*d+k][j*d+l] = val
	return img

def conv(img1,img2,r,c):
	'''Takes image img1,img2.
	Pastes img2 on img1 such that left-upper corner of img2
	is at (r,c) of img1
	Returns the modified img1'''
	r -= 1
	c -= 1
	for i in range(d):
		for j in range(d):
			for k in range(3):
				if img2[i][j][3] == 255:
					img1[d*r+i][d*c+j] = img2[i][j][:-1]
	return img1

def selected(board,board_rep,x,y,pieces,reverse):
	'''turns selected square red if reverse=False
	else unselects if reverse=True'''
	piece = board_rep[x-1][y-1]
	x -= 1
	y -= 1
	val = []
	if (x+y)%2 == 0:
		val = light
	else:
		val = dark
	for i in range(d):
		for j in range(d):
			if reverse == False:
				board[d*x+i][d*y+j] = [0,0,255]
			else:
				board[d*x+i][d*y+j] = val
	conv(board,pieces[piece],x+1,y+1)


def turn_color(turn):
	'''Returns the color of the player which moves this turn'''
	if(turn%2==0):
		return 'd'
	else:
		return 'l'

def empty(img1,px,py):
	'''Removes image of piece from square (px,py)'''
	if(d_or_l(px,py)=='dark'):
		val = dark;
	else:
		val = light

	r,c = which_square(px,py)
	r -= 1
	c -= 1
	for i in range(d):
		for j in range(d):
			img1[d*r+i][d*c+j] = val

def load_pieces():
	'''Loads the images of chess pieces.
	Returns a dictionary of images having keys consisting
	of two characters xy where x denoted the piece e.g. k for king 
	and y is color of piece l = light and d = dark'''
	pieces = {}

	for i in ['k','q','b','n','r','p']:
		for j in ['l','d']:
			img1 = cv2.imread("img/Chess_{a}{b}t60.png".format(a=i,b=j),-1)
			pieces[i+j] = img1
	return pieces

def which_square(px,py):
	'''Takes the pixel coordinates (px,py) which are int and 
	returns the square currently on as a 2-tuple.'''
	rx = px%d
	qx = (px - rx)/d
	ry = py%d
	qy = (py - ry)/d

	return (int(qy+1),int(qx+1))

def initialize(board,pieces):
	'''Initializes the chess pieces at their starting positions.
	Returns the image of the initialized board'''
	conv(board,pieces["rl"],1,1)
	conv(board,pieces["nl"],1,2)
	conv(board,pieces["bl"],1,3)
	conv(board,pieces["ql"],1,4)
	conv(board,pieces["kl"],1,5)
	conv(board,pieces["bl"],1,6)
	conv(board,pieces["nl"],1,7)
	conv(board,pieces["rl"],1,8)
	conv(board,pieces["rd"],8,1)
	conv(board,pieces["nd"],8,2)
	conv(board,pieces["bd"],8,3)
	conv(board,pieces["qd"],8,4)
	conv(board,pieces["kd"],8,5)
	conv(board,pieces["bd"],8,6)
	conv(board,pieces["nd"],8,7)
	conv(board,pieces["rd"],8,8)

	for i in range(1,9):
		conv(board,pieces["pl"],2,i)
		conv(board,pieces["pd"],7,i)

	return board

def initialize_board_rep():
	'''Returns and numpy array with cells containing pieces
	present in the cell. Contains 00 if no piece is present
	at theat cell'''
	board_rep = []
	for i in range(8):
		row = []
		for j in range(8):
			row.append('00')
		board_rep.append(row)


	board_rep[0][0] = "rl"
	board_rep[0][1] = "nl"
	board_rep[0][2] = "bl"
	board_rep[0][3] = "ql"
	board_rep[0][4] = "kl"
	board_rep[0][5] = "bl"
	board_rep[0][6] = "nl"
	board_rep[0][7] = "rl"
	board_rep[7][0] = "rd"
	board_rep[7][1] = "nd"
	board_rep[7][2] = "bd"
	board_rep[7][3] = "qd"
	board_rep[7][4] = "kd"
	board_rep[7][5] = "bd"
	board_rep[7][6] = "nd"
	board_rep[7][7] = "rd"

	for i in range(8):
		board_rep[1][i] = 'pl'
		board_rep[6][i] = 'pd'

	return board_rep

def select(event,px,py,flags,param):
	'''Mouse event. Makes character dissapear when clicked'''
	board = param[0]
	clicked = param[1]
	board_rep = param[2]
	turn = param[3]
	turn_col = turn_color(turn[0])
	pos = param[4]
	pieces = param[5]

	if event == cv2.EVENT_LBUTTONDOWN:
		x,y = which_square(px,py)
		if clicked[0] == False and board_rep[x-1][y-1][1] == turn_col:
			selected(board,board_rep,x,y,pieces,False)
			pos[0],pos[1] = px,py
			clicked[0] = True

		elif clicked[0] == True and board_rep[x-1][y-1][1] == turn_col:
			selected(board,board_rep,x,y,pieces,False)
			pos[0],pos[1] = which_square(pos[0],pos[1])
			selected(board,board_rep,pos[0],pos[1],pieces,True)
			pos[0],pos[1] = px,py
			clicked[0] = True

		elif clicked[0] == True and board_rep[x-1][y-1] == '00':
			empty(board,pos[0],pos[1])
			pos[0],pos[1] = which_square(pos[0],pos[1])
			conv(board,pieces[board_rep[pos[0]-1][pos[1]-1]],x,y)
			board_rep[x-1][y-1] = board_rep[pos[0]-1][pos[1]-1]
			board_rep[pos[0]-1][pos[1]-1] = '00'
			turn[0] += 1
			clicked[0] = False

		# else:
		# 	print("Invalid Move!")


board = create_board()     #Creates the board
board_rep = initialize_board_rep() #Create a representation of the board
pieces = load_pieces()     #Loads the pieces
img = initialize(board,pieces)     #Initializes the pieces
initialize_board_rep()
clicked = [False]
turn = [1]
pos = [0,0]

cv2.namedWindow("Image")
cv2.setMouseCallback("Image",select,param=[img,clicked,board_rep,turn,pos,pieces])

while(1):
	cv2.imshow("Image",img)         #Shows images
	key = cv2.waitKey(100);               #waits for infinite time
	if key == 27:
		break
	if key == ord("d"):
		break

cv2.destroyAllWindows()       #Closes all windows
