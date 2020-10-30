#!/usr/local/bin/python3

#https://github.com/dotPrivate/sudokusolve

import sys
import time

class Grid():
	#initiates the board

	def __init__(self):
		#self.grid = [[0 for column in range(9)] for row in range(9)]
		self.cols = [[],[],[],[],[],[],[],[],[]]
		self.boxes = [[],[],[],[],[],[],[],[],[]]
		
		#temp boards for debugging
		#boards are from sudoku.com
		
		'''
		#Easy board
		self.grid = [
			[8,2,0,3,0,0,0,4,5],
			[5,0,3,0,0,0,0,0,9],
			[0,7,4,0,0,5,3,0,0],
			[0,9,0,0,2,3,0,8,0],
			[0,0,8,0,7,1,0,0,3],
			[0,3,7,0,0,0,0,5,2],
			[0,4,0,0,0,0,8,7,0],
			[1,0,0,0,3,0,0,9,4],
			[0,8,0,9,0,0,2,0,1]
		]
		'''
		'''
		#Medium board
		self.grid = [
			[9,0,0,0,0,8,1,0,5],
			[0,8,5,0,2,0,0,7,0],
			[0,7,4,0,0,1,0,9,0],
			[0,0,6,0,0,0,0,1,0],
			[2,0,8,0,0,5,9,0,6],
			[0,5,0,0,0,0,0,2,4],
			[0,0,1,0,0,4,0,0,2],
			[6,0,0,0,0,0,3,8,0],
			[8,0,7,0,0,0,0,0,0]
		]
		'''
		#Hard board
		self.grid = [
			[0,0,5,0,0,0,0,0,0],
			[0,6,2,0,0,0,0,3,0],
			[3,7,0,0,2,0,0,0,0],
			[0,0,0,2,0,0,0,0,0],
			[0,1,8,0,9,0,5,0,4],
			[4,0,6,0,0,0,0,8,0],
			[0,3,0,6,0,0,0,9,0],
			[0,0,0,0,0,0,0,2,0],
			[0,0,7,5,0,9,3,6,0]
		]
		'''
		#Expert board
		self.grid = [
			[5,6,0,0,0,0,0,0,1],
			[0,0,0,0,5,0,0,6,0],
			[0,0,7,8,3,0,4,0,0],
			[0,0,5,3,0,1,0,0,0],
			[7,0,0,0,0,0,2,0,6],
			[2,0,0,0,0,7,0,5,0],
			[0,0,0,0,0,0,5,3,0],
			[0,5,1,4,0,0,0,0,0],
			[4,0,0,0,0,2,0,0,0]
		]
		'''

		#x is each row in the grid
		#i is each item in the row
		for x in range(len(self.grid)):
			for i in range(len(self.grid[x])):
				#Adds each value in each column to a 2D array
				self.cols[i].append(self.grid[x][i])

				self.boxes[(x//3)*3+i//3].append(self.grid[x][i])
		
				#i//3 divides the rows into 3 sections
				#x//3 divides the columns into 3 sections
				#x//3 is multiplied by 3 as an offset for the next rows

				#offset is added to the 3 sections for each row
				#to find the index for 'boxes' to put values into

				# final indices
				#
				# 000 111 222
				# 000 111 222
				# 000 111 222
				#
				# 333 444 555
				# 333 444 555
				# 333 444 555
				#
				# 666 777 888
				# 666 777 888
				# 666 777 888
				
		#performs the board checks
		if (self.checkvalid(self.grid) and self.checkvalid(self.cols) and self.checkvalid(self.boxes)):
			print("Valid board")
	
	#prints the board
	def out(self):
		for i in range(len(self.grid)):
			print(self.grid[i])

	def checkvalid(self, arr):
		#Every column checked for repeat values
		#Every row checked for repeat values
		#Every box checked for repeat values

		for x in range(len(arr)):
			#stores encountered values for each
			enc = []

			for i in range(len(arr[x])):
				#If value already encountered, the board is invalid
				if arr[x][i] in enc:
					return 0

				# If cell not empty, add to the array	
				if arr[x][i] != 0:
					enc.append(arr[x][i])

		return 1

	def check_possible(self,row,i):
		possible = [1,2,3,4,5,6,7,8,9]

		for x in self.grid[row]:
			#Removes any numbers appearing in the same row from possible nums
			if x in possible:
				possible.remove(x)
		for y in self.cols[i]:
			#Removes any numbers appearing in the same col from possible nums
			if y in possible:
				possible.remove(y)
		for z in self.boxes[(row//3)*3+i//3]:
			#Removes any numbers appearing in the same box from possible nums
			if z in possible:
				possible.remove(z)

		return possible

	def solve(self):
		startTime = time.time()
		
		solved = 0

		while not solved:
			solved = 1
			for row in range(len(self.grid)):
				for i in range(len(self.grid[row])):
					#going through each empty cell

					if self.grid[row][i] == 0:
						solved = 0

						possible = self.check_possible(row,i)

						if len(possible) == 1:
							#Replace cells with only one possible number with that number
							self.grid[row][i] = possible[0]
							self.cols[i][row] = possible[0]
							self.boxes[row//3*3+i//3][i%3+row%3*3] = possible[0]
							continue
						else:
							for num in possible:
								#Check other empty cells in the same box for their possible numbers
								#If num not present in the rest, replace cell with num
								for z in range(9):
									confirm = 1
									
									# box indices
									# [0,1,2,3,4,5,6,7,8]
									# [0,1,2,0,1,2,0,1,2] column z%3 + i//3*3
									# [0,0,0,1,1,1,2,2,2] row    z//3 + row//3*3
									
									# box column offset: i//3
									# box row offset:    row//3

									#Don't include the current cell
									if z%3 + i//3*3 == i and z//3 + row//3*3 == row:
										continue
									else:
										#Rest of empty cells in the same box
										if self.boxes[row//3*3+i//3][z] == 0:
											tempossible = self.check_possible(z//3 + row//3*3, z%3 + i//3*3)
										
											if num in tempossible:
												confirm = 0
												break

								#print(row, i, possible,z//3 + row//3*3, z%3 + i//3*3, tempossible, num, c)
								if confirm:
									self.grid[row][i] = num
									self.cols[i][row] = num
									self.boxes[row//3*3+i//3][i%3+row%3*3] = num
			
		grid.out()
		print(f"Program completed in {time.time()-startTime} seconds.")

		#print(empty)

	def solveable(self):

		# to check for a solvable board there are a few ways:
		#
		# 1. try to solve a board for a certain number of time
		#	if at least one solution within that time, solvable
		#	else, not solvable
		#
		# 2. have a set of rules to determine if the board is solvable
		#	i.e. at least 17 cells have to be filled for a board to be solvable
		#
		# 3. use both
		#	i.e. first check if there are at least 17 cells filled, if check is passed,
		#	attempt to solve

		pass

def main():
	#user inputs an option they want

	print("\033[1;32mSUDOKU")
	print("\033[m\033[32m(1) Auto-solve a board")
	print("(2) Check if a board is solvable")
	print("(3) Solve a randomly generated solvable board")
	print("(4) Exit\033[m")
	choice = input("Enter your option: ")

	if choice == "1":
		grid.solve()
	elif choice == "2":
		pass
	elif choice == "3":
		pass
	elif choice == "4":
		sys.exit()
	else:
		print("Invalid option, please try again.")
		main()

if __name__ == "__main__":
	grid = Grid()
	main()

	
