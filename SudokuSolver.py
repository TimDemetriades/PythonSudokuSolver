import time

board = [               # Sudoku Board
 [9,0,0,0,0,0,5,1,0],   # 1
 [0,7,0,0,8,0,0,0,9],   # 2
 [5,0,0,1,0,9,2,7,8],   # 3
 [2,5,0,0,0,7,8,0,1],   # 4
 [1,0,0,0,5,0,0,0,0],   # 5
 [3,0,0,0,9,0,0,0,0],   # 6
 [0,0,0,3,1,5,0,4,0],   # 7
 [0,0,0,0,0,0,0,0,0],   # 8
 [7,1,4,0,2,0,0,8,0]    # 9
]

def displayBoard(board):
  """
  prints the board
  :parameter board: 2d list of integers
  :return: None
  """

  for i in range(len(board)):   # rows
    if i % 3 == 0 and i != 0:
      print("-------------------------")  # horiontal lines

    for j in range(len(board[0])):    # columns
      if j % 3 == 0 and j != 0:
        print(" | "+ ' ', end = '')    # vertical lines (end = '' is used to not end with newline (\n))

      if j == 8:    # last value in row
        print(board[i][j])
      else:
        print(str(board[i][j]) + ' ', end = '')   # str is so we can add the space

def findZero(board):
  """
  finds a zero in the board
  :parameter board: partially complete board
  :return: (integer, integer) row column
  """

  for row in range(len(board)):
    for column in range(len(board[0])):
      if board[row][column] == 0: 
        return(row, column)    # row, column

  return None   # needed since otherwise wil return position of zero

def validNumber(board, number, position):
  """
  checks if number is valid in board
  :parameter board: 2d list of integers
  :parameter number: integer
  :parameter position: position of number (row, column)
  :return: bool
  """

  # First check row
  for i in range(9):
    if board[position[0]][i] == number and i != position[1]:    # check if equal in row and not position we just entered number
      return False

  # Then check column
  for i in range(9):
    if board[i][position[1]] == number and i != position[1]:   # check if equal in column and not position we just entered number
      return False

  # Finally, check square
  square_x = position[1] // 3   # floor division (will give 0, 1, or 2)
  square_y = position[0] // 3   # floor division (will give 0, 1, or 2)

  for i in range(square_y * 3, square_y * 3 + 3):   # from beginning to end of square row
    for j in range(square_x * 3, square_x * 3 + 3):   # from beginning to end of square column
      if board[i][j] == number and (i, j) != position:
        return False

  return True   # if all 3 tests do not return false, return true since number is valid

def solver(board):
  """
  solves sudoku board using backtracking
  :parameter board: 2d list of integers
  :return: solution
  """

  # Base case of recusion, checks if any zeroes are left
  find = findZero(board)   # checks for zeroes
  if find != None:    # found zero
    row, column = find    # find is a tuple e.g. (x, y)
  else:   # no zeroes left; find is none
    return True    # board is done

  for number in range(1,10):   # tries numbers 1 to 9
    if validNumber(board, number, (row, column)) is True:   # if number valid
      board[row][column] = number   # inserts number

      if solver(board) is True:   # if no zeroes left
        return True  # board is solved

      else:   # zeroes found
        board[row][column] = 0    # board not solved, reset number to zero 
        continue
    
    else:   # if number not valid
      continue


if __name__ == "__main__":
  print("Un-solved Board")
  displayBoard(board)

  startTime = time.time()

  solver(board)

  elapsedTime = time.time() - startTime
  elapsedTime = str(round(elapsedTime, 4))

  print("")
  print("Solved Board")
  displayBoard(board)

  print("")
  print("Time elapsed: ", elapsedTime, " seconds")
