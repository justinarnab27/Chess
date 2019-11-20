import cv2
import numpy as np 

d = 60

def create_board():
	img = np.zeros((8*d,8*d,3))
	for i in range(8):
		for j in range(8):
			for k in range(d):
				for l in range(d):
					val = (0,0,255)
					if (i+j)%2 == 0:
					 val = (100,100,0)
					img[i*d+k][j*d+l] = val
	return img

def conv(img1,img2,r,c):
	r -= 1
	c -= 1
	for i in range(d):
		for j in range(d):
			for k in range(3):
				if img2[i][j][3] == 255:
					img1[d*r+i][d*c+j] = img2[i][j][:-1]
	return img1

def load_pieces():
	pieces = {}

	for i in ['k','q','b','n','r','p']:
		for j in ['l','d']:
			img1 = cv2.imread("img/Chess_{a}{b}t60.png".format(a=i,b=j),-1)
			pieces[i+j] = img1
	return pieces

def initialize(board,pieces):
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
board = create_board()
pieces = load_pieces()
img = create_board()
img = initialize(board,pieces)

cv2.imshow("image",img)

cv2.waitKey(0);
cv2.destroyAllWindows()
