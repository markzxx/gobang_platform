import random
import re

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0

#don't change the class name
class AI(object):
	def __init__(self, chessboard_size, color, time_out):
		self.chessboard_size = chessboard_size
		self.color = color
		self.time_out = time_out #time limit.
		self.candidate_list = []

	def go(self, chessboard):
		self.candidate_list.clear()
	#=========================================
			
		def retrieve_chess_string(pos, x_direct, y_direct, radius, fill_color):
			chess_string = ''
			x, y = pos[0], pos[1]
			if fill_color == COLOR_BLACK:
				fill = 'B'
			elif fill_color == COLOR_WHITE:
				fill = 'W'
			else:
				fill = 'x' 

			if x_direct == 1 and y_direct == 0:
				for i in range(max(0, x-radius), x):
					if chessboard[i][y] == COLOR_BLACK:
						chess_string += 'B'
					elif chessboard[i][y] == COLOR_WHITE:
						chess_string += 'W'
					else:
						chess_string += 'x'
				chess_string += fill
				for i in range(x+1, min(x+radius+1, self.chessboard_size)):
					if chessboard[i][y] == COLOR_BLACK:
						chess_string += 'B'
					elif chessboard[i][y] == COLOR_WHITE:
						chess_string += 'W'
					else:
						chess_string += 'x'

			if x_direct == 0 and y_direct == 1:
				for i in range(max(0, y-radius), y):
					if chessboard[x][i] == COLOR_BLACK:
						chess_string += 'B'
					elif chessboard[x][i] == COLOR_WHITE:
						chess_string += 'W'
					else:
						chess_string += 'x'
				chess_string += fill
				for i in range(y+1, min(y+radius+1, self.chessboard_size)):
					if chessboard[x][i] == COLOR_BLACK:
						chess_string += 'B'
					elif chessboard[x][i] == COLOR_WHITE:
						chess_string += 'W'
					else:
						chess_string += 'x'

			if x_direct == y_direct:
				if(x > y):
					for i in range(max(x-radius, x-y), x):
						if chessboard[i][y-x+i] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][y-x+i] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
					chess_string += fill
					for i in range(x+1, min(x+radius+1, self.chessboard_size)):
						if chessboard[i][i-x+y] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][i-x+y] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
				else:
					for i in range(max(0, x-radius), x):
						if chessboard[i][i-x+y] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][i-x+y] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
					chess_string += fill
					for i in range(x+1, min(x-y+self.chessboard_size, x+radius+1)):
						if chessboard[i][i-x+y] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][i-x+y] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'

			if x_direct == -y_direct:
				if(y < -x + self.chessboard_size - 1):
					for i in range(max(0, x-radius), x):
						if chessboard[i][x+y-i] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][x+y-i] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
					chess_string += fill
					for i in range(x+1, min(x+radius+1, x+y+1)):
						if chessboard[i][x+y-i] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][x+y-i] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
				else:
					for i in range(max(x+y-self.chessboard_size+1, x-radius), x):
						if chessboard[i][x+y-i] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][x+y-i] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
					chess_string += fill
					for i in range(x+1, min(x+radius+1, self.chessboard_size)):
						if chessboard[i][x+y-i] == COLOR_BLACK:
							chess_string += 'B'
						elif chessboard[i][x+y-i] == COLOR_WHITE:
							chess_string += 'W'
						else:
							chess_string += 'x'
			return chess_string
	#=========================================

		def evaluate(pos):
			value = 0
			black_state = {'connect-5': 0, 'live-4':0, 'flush-4':0, 'connect-flush-4':0, 'jump-flush-4':0, 'live-3':0, 'connect-live-3':0, 'jump-live-3':0, 'sleep-3':0, 'live-2':0}
			white_state = {'connect-5': 0, 'live-4':0, 'flush-4':0, 'connect-flush-4':0, 'jump-flush-4':0, 'live-3':0, 'connect-live-3':0, 'jump-live-3':0, 'sleep-3':0, 'live-2':0}
			for direction in [[1,0], [0,1], [1,1], [1,-1]]:
				chess_str_4_black = retrieve_chess_string(pos, direction[0], direction[1], 4, COLOR_BLACK)
				#connect-5
				if re.search('BBBBB', chess_str_4_black):
					black_state['connect-5'] += 1
				#live-4
				elif re.search('xBBBBx', chess_str_4_black):
					black_state['live-4'] += 1
				#flush-4
				elif re.search('WBBBBx', chess_str_4_black) or re.search('xBBBBW', chess_str_4_black):
					black_state['connect-flush-4'] += 1
					black_state['flush-4'] += 1	
				elif re.search('BBBxB', chess_str_4_black) or re.search('BBxBB', chess_str_4_black) or re.search('BxBBB', chess_str_4_black):
					black_state['jump-flush-4'] += 1
					black_state['flush-4'] += 1
				#live-3
				elif re.search('xBBBxx', chess_str_4_black) or re.search('xxBBBx', chess_str_4_black):
					black_state['connect-live-3'] += 1
					black_state['live-3'] += 1
				#jump-3
				elif re.search('xBBxBx', chess_str_4_black) or re.search('xBxBBx', chess_str_4_black):
					black_state['jump-live-3'] += 1
					black_state['live-3'] += 1
				#sleep-3
				elif re.search('WBBBxx', chess_str_4_black) or re.search('xxBBBW', chess_str_4_black):
					black_state['sleep-3'] += 1
				#live-2
				elif re.search('xBBxxx', chess_str_4_black) or re.search('xxBBxx', chess_str_4_black) or re.search('xxxBBx', chess_str_4_black):
					black_state['live-2'] += 1


				chess_str_4_white = retrieve_chess_string(pos, direction[0], direction[1], 4, COLOR_WHITE)
				#connect-5
				if re.search('WWWWW', chess_str_4_white):
					white_state['connect-5'] += 1
				#live-4
				elif re.search('xWWWWx', chess_str_4_white):
					white_state['live-4'] += 1
				#flush-4
				elif re.search('BWWWWx', chess_str_4_white) or re.search('xWWWWB', chess_str_4_white):
					white_state['connect-flush-4'] += 1
					white_state['flush-4'] += 1
				elif re.search('WWWxW', chess_str_4_white) or re.search('WWxWW', chess_str_4_white) or re.search('WxWWW', chess_str_4_white):
					white_state['jump-flush-4'] += 1
					white_state['flush-4'] += 1
				#live-3
				elif re.search('xWWWxx', chess_str_4_white) or re.search('xxWWWx', chess_str_4_white):
					white_state['connect-live-3'] += 1
					white_state['live-3'] += 1
				#jump-3
				elif re.search('xWWxWx', chess_str_4_white) or re.search('xWxWWx', chess_str_4_white):
					white_state['jump-live-3'] += 1
					white_state['live-3'] += 1
				#sleep-3
				elif re.search('BWWWxx', chess_str_4_white)  or re.search('xxWWWB', chess_str_4_white):
					white_state['sleep-3'] += 1
				#live-2
				elif re.search('xWWxxx', chess_str_4_white) or re.search('xxWWxx', chess_str_4_white) or re.search('xxxWWx', chess_str_4_white):
					white_state['live-2'] += 1
			
			
			if self.color == COLOR_BLACK:
				attack_state = black_state
				defend_state = white_state
			else:
				attack_state = white_state
				defend_state = black_state
			
			##########definately best##########
			if attack_state['connect-5'] >= 1:
				value += 1 << 26
				pass
			elif defend_state['connect-5'] >= 1:
				value += 1 << 25
				pass
			elif attack_state['live-4'] >= 1 or attack_state['flush-4'] >= 2:
				value += 1 << 24
				pass
			elif defend_state['live-4'] >= 1 or defend_state['flush-4'] >= 2:
				value += 1 << 23
				pass
			###################################
			#########very approach best########
			elif attack_state['flush-4'] >= 1 and attack_state['live-3'] >= 1:
				value += 1 << 22
			elif defend_state['flush-4'] >= 1 and defend_state['live-3'] >= 1:
				value += 1 << 21
			elif attack_state['live-3'] >= 2:
				value += 1 << 20
			elif defend_state['live-3'] >= 2:
				value += 1 << 19
			else:
				value += attack_state['flush-4'] * (1<<10) + attack_state['live-3'] * (1<<9) + defend_state['flush-4'] * (1<<8) + defend_state['live-3'] * (1<<7) +\
						 attack_state['live-2'] * (1<<6) + defend_state['live-2'] * (1<<5) 
			pos_val = 7 - max(abs(pos[0] - 7), abs(pos[1] - 7))
			value += pos_val		
			return value
			###################################

	#==============Find new pos===============
		
		max_val = float("-inf")
		for i in range(self.chessboard_size):
			for j in range(self.chessboard_size):
				eva = evaluate([i, j])
				if chessboard[i][j] == 0:
					if eva > max_val:
						max_val = eva
						self.candidate_list.append([i, j])
					elif eva == max_val and random.randint(0, 1) == 0:
						self.candidate_list.append([i, j])
						

				
										











