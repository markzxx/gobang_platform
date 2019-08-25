import numpy as np
import random
import time
import queue as q

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)

class AI(object):
	"""docstring for AI"""
	def __init__(self, chessboard_size, color, time_out):
		self.chessboard_size = chessboard_size
		self.color = color
		self.time_out = time_out
		self.candidate_list = []
		self.myqilist = []

	def inBoard(self, chessboard, point):
		x = point[0]
		y = point[1]
		if x < 0 or y < 0 or x >= self.chessboard_size or y >= self.chessboard_size:
			return False
		else:
			return True

	def valid_move(self, chessboard, point):
		x = point[0]
		y = point[1]
		return self.inBoard(chessboard, point) and chessboard[x, y] == 0

	def color_list(self, chessboard, color):
		if color == COLOR_BLACK:
			black_idx = np.where(chessboard == COLOR_BLACK)
			black_idx = list(zip(black_idx[0], black_idx[1]))
			return black_idx
		elif color == COLOR_WHITE:
			white_idx = np.where(chessboard == COLOR_WHITE)
			white_idx = list(zip(white_idx[0], white_idx[1]))
			return white_idx
		elif color == COLOR_NONE:
			kong_idx = np.where(chessboard == COLOR_NONE)
			kong_idx = list(zip(kong_idx[0], kong_idx[1]))
			return kong_idx

	# It includes the position itself
	def checkPath(self, color, chessboard, position, p_position, counter):
		x = position[0]
		y = position[1]
		px = p_position[0]
		py = p_position[1]
		if counter < 0 or not self.inBoard(chessboard, position) or chessboard[x, y] != color:
			return 0
		return 1 + (self.checkPath(color, chessboard, (x+px, y+py), (px, py), counter-1) \
			if self.inBoard(chessboard, (x+px, y+py)) else 0)

	def isWin(self, chessboard):
		color = self.color
		if len(self.myqilist):
			pos = self.myqilist[-1]
		else:
			return False
		checklist = []
		depth = 4
		for move in ((0, 1), (1, 0), (1, 1), (-1, 1)):
			opp = tuple(map(lambda x: -x, move))
			checklist.append(self.checkPath(color, chessboard, pos, move, depth) + \
							 self.checkPath(color, chessboard, pos, opp, depth) - 1)
		if 5 in checklist:
			return True
		else:
			return False

	def go(self, chessboard):
		self.candidate_list.clear()
		start = time.time()
		# My AI algorithm----------------------------
		if len(self.color_list(chessboard, COLOR_NONE)) == self.chessboard_size * self.chessboard_size:
			new_pox = (7, 7)
		else:
			# new_pox = self.move_list(chessboard, 3)[0][1]
			new_pox = self.next_move(chessboard, self.time_out)
			# self.myqilist.append(self.move_list(chessboard, 3)[0][1])
			self.myqilist.append(self.next_move(chessboard, self.time_out))
		# -------------------------------------------
		run_time = (time.time() - start)
		# assert chessboard[new_pox[0], new_pox[1]] == COLOR_NONE
		self.candidate_list.append(new_pox)
		# print(self.candidate_list)

	def move_list(self, chessboard, limit):
		pq = q.PriorityQueue()
		points = []
		for i in range(len(chessboard)):
			for j in range(len(chessboard[i])):
				if self.valid_move(chessboard, (i, j)):
						value = self.evaluate_position(chessboard, (i, j))
						pq.put((-value, (i, j)))
		for i in range(limit):
			points.append(pq.get())
		return points

	def evaluate(self, chessboard, position, attack):
		(x, y) = position
		color = self.color if attack else -self.color
		score = 0
		for pair in ((0, 1), (1, 0), (1, 1), (-1, 1)):
			(dx, dy) = pair
			pathlist = [0]
			for s in (-1, 1):
				for i in range(1, 5):
					py = y+dy*i*s
					px = x+dx*i*s
					if not self.inBoard(chessboard, (px, py)) or chessboard[px, py] == -color \
					or (i + 1 == 5 and self.inBoard(chessboard, (px+dx*s, py+dy*s)) \
					and chessboard[px+dx*s, py+dy*s] == color):
						break
					if s > 0:
						pathlist.append(chessboard[px, py])
					if s < 0:
						pathlist.insert(0, chessboard[px, py])
			path_num = len(pathlist) - 5 + 1
			if path_num > 0:
				for i in range(path_num):
					value = pathlist[i:i+5].count(color)
					if self.color == COLOR_BLACK:
						score += value**(5 if attack else 4.9) if value != 4 else 100**(9 if attack else 8)
					elif self.color == COLOR_WHITE:
						score += value**5 if value != 4 else 100**(9 if attack else 8)
		return score
		
	def evaluate_position(self, chessboard, position):
		if self.valid_move(chessboard, position):
			return self.evaluate(chessboard, position, True) + self.evaluate(chessboard, position, False)
		else:
			return 0

	def attackArea(self, position):
		x = position[0]
		y = position[1]
		area = []
		for pair in ((0, 1), (1, 0), (1,1), (-1, 1)):
			(dx, dy) = pair
			for s in (-1, 1):
				for i in range(1,5):
					px = x+dx*i*s
					py = y+dy*i*s
					area.append((px, py))
		return area

	# def top_positions(self, chessboard, limit):
	# 	pq = q.PriorityQueue()
	# 	spots = set()
	# 	for t in self.color_list(chessboard, COLOR_BLACK) + self.color_list(chessboard, COLOR_WHITE):
	# 		print(t)
	# 		for m in self.attackArea(t):
	# 			if self.inBoard(chessboard, m):
	# 				spots.add(m)
	# 	for r in spots:
	# 		pq.put(self.evaluate_position(chessboard, r) * (-1), r)
	# 	toplist = []
	# 	for x in range(limit):
	# 		toplist.append(pq.get())
	# 	for i in len(toplist):
	# 		toplist[i][1][0] = -toplist[i][1][0]
	# 	return toplist

	def juetBestMove(self, chessboard, limit):
		toplist = self.move_list(chessboard, limit)
		topval = toplist[0][0]
		bestlist = []
		for atom in toplist:
			(val, move) = atom
			if val == topval:
				bestlist.append(move)
		return bestlist

	def turn(self, chessboard):
		if len(self.color_list(chessboard, COLOR_BLACK)) == len(self.color_list(chessboard, COLOR_WHITE)):
			return -1
		else:
			return 1

	def move(self, chessboard, position):
		x = position[0]
		y = position[1]
		chessboard[x, y] = self.turn(chessboard)

	def next_move(self, chessboard, time, dive=2):
		checkTOP = 3
		checkDEPTH = 3
		atoms = self.move_list(chessboard, checkTOP)
		mehlist = []
		bahlist = []
		for atom in atoms:
			# print(atom)
			(val, move) = atom
			board = chessboard
			self.move(board, move)
			if self.isWin(board):
				return move
			if dive == 1:
				score = -self.dive1(board, checkDEPTH - 1)
			elif dive == 2:
				score = -self.dive2(board, checkDEPTH - 1)

			if score == 1:
				return move
			elif score == 0:
				mehlist.append((score, move))
			elif score > -1:
				bahlist.append((score, move))
		if len(mehlist):
			return mehlist[0][1]
		elif len(bahlist):
			bahlist.sort()
			return bahlist[-1][1]
		else:
			return atoms[0][1]

	def dive1(self, chessboard, depth):
		bestmove = self.move_list(chessboard, 1)[0][1]
		board = chessboard
		self.move(board, bestmove)
		if self.isWin(board):
			return 1
		elif not depth:
			return 0
		else:
			return -self.dive1(board, depth - 1)

	def dive2(self, chessboard, depth):
		bestmoves = self.juetBestMove(chessboard, 5)
		overall = 0.0
		split_factor = 1.0/len(bestmoves)
		for bmove in bestmoves:
			board = chessboard
			self.move(board, bmove)
			if self.isWin(board):
				return 1
			elif not depth:
				continue
			else:
				score = -self.dive2(board, depth - 1)
				if score == 1:
					return 1
				else:
					overall += split_factor * score
		return overall


		
# def input(x, y, z, chessboard):
# 	chessboard[x, y] = z

# def loaddata(path, chessboard):
# 	# normal path is 'D:/study/AI/lab/chess_log.txt'
# 	file = open(path)
# 	while True:
# 		line = file.readline()
# 		if not line:
# 			break
# 		input(int(line.split(',')[0]), int(line.split(',')[1]), int(line.split(',')[2]), chessboard)

# if __name__ == '__main__':
# 	ai = AI(15, COLOR_BLACK, 1)
# 	chessboard = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], \
# 					  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
# 	loaddata('D:/study/AI/lab/chess_log.txt', chessboard)
# 	chessboard = np.ones((15, 15))
# 	chessboard[:, ::2] = -1
# 	for i in range(0, 15, 4):
# 		chessboard[i] = -chessboard[i]
# 	x, y = np.random.choice(15, 2)
# 	chessboard[x, y] = 0
	# chessboard = np.zeros((15, 15), dtype=np.int)
	# chessboard[0, 0:4] = -1
	# chessboard[1, 0:4] = 1
	# chessboard = np.zeros((15, 15), dtype=np.int)
	# chessboard[0, 0:2] = -1
	# chessboard[0, 7] = -1
	# chessboard[1, 1:4] = 1
	# NOW THERE IS A PORBLEM WITH DOUBLE THREE
	# ----------------------------------------------------
	# chessboard = np.zeros((15, 15), dtype=np.int)
	# chessboard[1, 1:3] = -1
	# chessboard[2:4, 3] = -1
	# chessboard[1, 6:8] = 1
	# chessboard[2:4, 8] = 1
	# ----------------------------------------------------
	# chessboard = np.zeros((15, 15), dtype=np.int)
	# chessboard[0, 0:2] = -1
	# chessboard[0:2, 15-1] = -1
	# chessboard[1, 6:8] = 1
	# chessboard[2:4, 8] = 1
	# chessboard[7, 7] = COLOR_BLACK
	# ai.myqilist.append((1,1))
	# ai.myqilist.append((1,2))
	# ai.myqilist.append((2,3))
	# ai.myqilist.append((3,3))
	# print(chessboard)
	# ai.go(chessboard)
