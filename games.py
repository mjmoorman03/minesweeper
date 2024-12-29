import tkinter as tk
import random 
import sys
import tools

mines = []
buttonList = []
rows = 0
cols = 0
numBombs = 0
placedCount = 0
board = []
noGuess = False

def buttons(mines : list, numBoard : list):
    buttons = []
    for y in range(len(mines)):
        for x in range(len(mines[0])):
            # color according to number
            buttons.append(tk.Button(window, text = '', width = 2, height = 1, bg="gray", fg="white"))
            buttons[-1].grid(row = y, column = x, sticky = "nsew")
    return buttons


def revealBombs():
    global buttonList
    for i, but in enumerate(buttonList):
        if mines[i//len(mines[0])][i%len(mines[0])] == 1:
            but["text"] = "\U0001F4A3"


def leftClick(event):
    # chord
    x = int(event.widget.grid_info()["row"])
    y = int(event.widget.grid_info()["column"])
    if event.widget["fg"] == "black" and event.widget["text"] != "\U0001F6A9":
        num = board[x][y]
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if event.widget.grid_info()["row"]+i < 0 or event.widget.grid_info()["row"]+i >= len(mines) or event.widget.grid_info()["column"]+j < 0 or event.widget.grid_info()["column"]+j >= len(mines[0]):
                    continue
                if buttonList[(event.widget.grid_info()["row"]+i)*len(mines[0])+event.widget.grid_info()["column"]+j]["text"] == "\U0001F6A9":
                    count += 1
        if count == num:
            for i, j in tools.neighborsOfCoord((x, y), len(board[0]), len(board)):
                recursiveReveal(i, j)
        return
    event.widget["fg"] = "black"
    if mines[x][y] == 1:
        revealBombs()
        return
    # empty, so reveal adjacent
    if board[x][y] == 0:
        event.widget["text"] = "-"
        for i, j in tools.neighborsOfCoord((x, y), len(board[0]), len(board)):
            recursiveReveal(i, j)
    if board[x][y] != 0:
        event.widget["text"] = str(board[x][y])
        return


def recursiveReveal(i, j):
    global buttonList
    if i < 0 or i >= len(mines) or j < 0 or j >= len(mines[0]):
        return
    # if already revealed, return
    if buttonList[i*len(mines[0])+j]["text"] == "\U0001F6A9":
        return
    if mines[i][j] == 1:
        revealBombs()
    if board[i][j] == 0 and buttonList[i*len(mines[0])+j]["text"] != "-":
        buttonList[i*len(mines[0])+j]["text"] = "-"
        for x, y in tools.neighborsOfCoord((i, j), len(mines[0]), len(mines)):
            recursiveReveal(x, y)
    else:
        buttonList[i*len(mines[0])+j]["fg"] = "black"
        buttonList[i*len(mines[0])+j]["text"] = str(board[i][j]) if str(board[i][j]) != "0" else "-"
        return


def win():
    for but in buttonList:
        if but["text"] == "\U0001F6A9":
            but["bg"] = "green"
            but["fg"] = "green"
    # show win message at bottom   
    label = tk.Label(window, text="You win!")
    label.grid(row=rows+1, column=0, columnspan=cols)

                
def rightClick(event):
    global placedCount 
    if event.widget["text"] == "\U0001F6A9":
        event.widget["text"] = '' #str(board[event.widget.grid_info()["row"]][event.widget.grid_info()["column"]]) if mines[event.widget.grid_info()["row"]][event.widget.grid_info()["column"]] == 0 else "\U0001F4A3"
        #event.widget["fg"] = "white"
        placedCount -= 1
        return
    event.widget["text"] = "\U0001F6A9" 
    placedCount += 1
    if placedCount == numBombs:
        win()


def reset(event):
    if event.char == " ":
        window.destroy()
        play(numBombs, rows, cols, noGuess)


def play(numMines : int, sizeX : int, sizeY : int, noGuessing : bool):
    global window
    global rows
    global cols
    global numBombs
    global placedCount
    global board
    global noGuess
    noGuess = noGuessing
    placedCount = 0
    rows = sizeX
    cols = sizeY
    numBombs = numMines
    window = tk.Tk()
    window.title("Minesweeper")
    window.geometry("800x600")
    window.resizable(False, False)
    global mines
    mines = tools.generateMinefield(numMines, sizeX, sizeY) if not noGuess else tools.generateNoGuess(numMines, sizeX, sizeY)
    board = tools.generateNumbers(mines)
    countLeft = tk.Label(window, text=str(numBombs - placedCount))
    countLeft.grid(row=0, column=1)
    global buttonList
    print(mines)
    print(board)
    buttonList = buttons(mines, board)
    for but in buttonList:
        but.bind("<Button-1>", leftClick, add="+")
        but.bind("<Button-2>", rightClick, add="+")
    window.bind("<KeyPress>", reset, add="+")
    window.resizable(True, True) 
    window.mainloop()



if __name__ == "__main__":
    play(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), eval(sys.argv[4]))