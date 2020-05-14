import requests
import re
import ast
import tkinter as tk
import tkinter.ttk as ttk
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

boardEasy = makeListofLists(9, puzzleEasyList)
boardMedium = makeListofLists(9, puzzleMediumList)
boardHard = makeListofLists(9, puzzleHardList)

def openEasySolutionWindow():
    """
    creates window for easy solution
    """
    openEasySolutionWindow = tk.Toplevel(window)
    openEasySolutionWindow.title("Sudoku - Easy Solution")
    openEasySolutionWindow.configure(bg='black')
    displayBoardGUI(boardEasy, openEasySolutionWindow)

def openMediumSolutionWindow():
    """
    creates window for medium solution
    """
    openMediumSolutionWindow = tk.Toplevel(window)
    openMediumSolutionWindow.title("Sudoku - Medium Solution")
    openMediumSolutionWindow.configure(bg='black')
    displayBoardGUI(boardMedium, openMediumSolutionWindow)

def openHardSolutionWindow():
    """
    creates window for hard solution
    """
    openHardSolutionWindow = tk.Toplevel(window)
    openHardSolutionWindow.title("Sudoku - Hard Solution")
    openHardSolutionWindow.configure(bg='black')
    displayBoardGUI(boardHard, openHardSolutionWindow)

def displayBoardGUI(board, window):
    """
    creates label for window to display solution
    :parameter board: board to use (easy, medium, or hard) 
    :parameter window: window to use (easy, medium, or hard)
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            tk.Label(window, text = board[i][j], width = "10", height = "4").grid(row = i, column = j, padx = 1, pady = 1)
            if i % 3 == 0 and i != 0:
                tk.Label(window, text = board[i][j], width = "10", height = "4").grid(row = i, column = j, padx = 1, pady = (15,1))
            if j % 3 == 0 and j != 0:
                tk.Label(window, text = board[i][j], width = "10", height = "4").grid(row = i, column = j, padx = (15,1), pady = 1)

################################################################################

if __name__ == "__main__":

    # Create main window
    window = tk.Tk()
    window.title("Sudoku")
    window.geometry("+700+300")     # Set positioning of window

    tk.Label(text = 'Welcome to NYTimes Sudoku Solver').grid(row = 0, column = 1, columnspan = 1, pady = 20)

    solveButton = tk.Button(
        text = 'Easy Solution',
        width = 20,
        height = 3,
        command = openEasySolutionWindow
        )
    solveButton.grid(row = 1, column = 0, padx = (2,0), pady = 5)

    solveButton = tk.Button(
        text = 'Medium Solution',
        width = 20,
        height = 3,
        command = openMediumSolutionWindow
        )
    solveButton.grid(row = 1, column = 1, pady = 5)

    solveButton = tk.Button(
        text = 'Hard Solution',
        width = 20,
        height = 3,
        command = openHardSolutionWindow
        )
    solveButton.grid(row = 1, column = 2, padx = (0,2), pady = 5)

    # Get all solutions (Can cause program to take a second to load the GUI)
    # These can be placed in the openSolutionWindow functions, but it can cause the solution to take a second to appear after clicking the button
    solver(boardEasy)
    solver(boardMedium)
    solver(boardHard)
    
    window.mainloop()       # runs tkinter event loop (needed to display window)
