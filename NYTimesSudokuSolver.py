import requests
import re
import ast
import time
import sys
from SudokuSolver import displayBoard, solver
from bs4 import BeautifulSoup

# This program will grab the NYTimes Daily Sudoku puzzle and solve it

# Get page
page = requests.get('https://www.nytimes.com/puzzles/sudoku')
if page.status_code != 200:   # 200 = good
  print("Page request failed :(")
else:
  print("Grabbing Today's NYTimes Sudoku Puzzle\n")

# Get content
content = page.content 

# Parse HTML
soup = BeautifulSoup(content, 'html5lib')

# Grab part that has puzzles
results = soup.find_all('script', attrs={'type':'text/javascript'})[0].text 

# Get easy puzzle
split = results.split('"puzzle":',2)[1]   # get part of puzzle after first occurance of 'puzzle'
puzzleEasy = split.split(',"solution"',1)[0]    # get part of puzzle before first occurance of 'solution'

# Get medium puzzle
split = results.split('"medium":',1)[1]
split2 = split.split('"puzzle":',2)[1]
puzzleMedium = split2.split(',"solution"',1)[0]

# Get hard puzzle
split = results.split('"hard":',1)[1]
split2 = split.split('"puzzle":',2)[1]
puzzleHard = split2.split(',"solution"',1)[0]

# Convert strings into lists
puzzleEasyList = ast.literal_eval(puzzleEasy) 
puzzleMediumList = ast.literal_eval(puzzleMedium) 
puzzleHardList = ast.literal_eval(puzzleHard) 

def makeListofLists(quantity, listGiven):
  """
  takes a list and makes it into a list of lists
  :parameter quantity: how many items you want in each list
  :parameter listGiven: list you want to make into list of lists
  !return! list of lists
  """
  i = 0
  newList = []
  while i < len(listGiven):
    newList.append(listGiven[i:i+quantity])
    i += quantity
  return(newList)

def checkQuit(userInput):
  """
  check if user types quit and exit program if so
  :parameter userInput: what user typed
  !return! nothing
  """
  if userInput == 'quit':
    sys.exit(0) 

def getDifficulty(prompt):
  """
  check whether user wants to solve easy, medium, or hard puzzle
  :parameter prompt: difficulty entered
  !return! choice
  """
  while True:
    try:
      value = input(prompt)
      checkQuit(value)     
    except ValueError:
      print("Invalid Selection")
      continue

    if value not in ('easy', 'medium', 'hard'):
      print("Invalid Selection")
      continue
    else:
      break
  return value

################################################################################

if __name__ == "__main__":

  print("NYTimes Sudoku Solver\n")
  print("Please choose a diffulty")
  difficulty = getDifficulty("Type either easy, medium, or hard (type quit to exit): ")

  if difficulty == 'easy':
    board = makeListofLists(9, puzzleEasyList)
  elif difficulty == 'medium':
    board = makeListofLists(9, puzzleMediumList)
  elif difficulty == 'hard':
    board = makeListofLists(9, puzzleHardList)

  print("")
  print("Unsolved Board")
  displayBoard(board)

  startTime = time.time()

  solver(board)

  elapsedTime = time.time() - startTime
  elapsedTime = str(round(elapsedTime, 4))

  print("")
  print("Solved Board")
  displayBoard(board)

  print("")
  print("Time elapsed: ", elapsedTime, " seconds\n")