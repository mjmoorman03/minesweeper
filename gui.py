import tkinter as tk
import os

noGuess = False


def setGuess():
    global noGuess
    noGuess = not noGuess
    return


def play(numMines : int, numRows : int, numCols : int, notGuessing : bool):
    r = os.fork()
    if r == 0:
        os.execvp("python3.10", ["python3.10", "games.py", str(numMines), str(numRows), str(numCols), str(notGuessing)])    


def main():
    window = tk.Tk()
    window.title("Minesweeper")
    window.geometry("800x600")
    # no guess mode
    noguessing = tk.Checkbutton(window, text="No Guess?", command=lambda: setGuess())
    noguessing.grid(row=0, column=2)

    # ask for difficulty
    label = tk.Label(window, text="Choose difficulty")
    label.grid(row=0, column=0)
    easy = tk.Button(window, text="Easy", width=10, height=2, command=lambda: play(10, 9, 9, noGuess))
    easy.grid(row=1, column=0)
    medium = tk.Button(window, text="Medium", width=10, height=2, command=lambda: play(40, 16, 16, noGuess))
    medium.grid(row=2, column=0)
    hard = tk.Button(window, text="Hard", width=10, height=2, command=lambda: play(99, 30, 16, noGuess))
    hard.grid(row=3, column=0)
    # ask for custom difficulty
    label = tk.Label(window, text="Custom difficulty")
    label.grid(row=0, column=1)
    label = tk.Label(window, text="Number of mines")
    label.grid(row=1, column=1)
    numMines = tk.Entry(window)
    numMines.grid(row=2, column=1)
    label = tk.Label(window, text="Number of rows")
    label.grid(row=3, column=1)
    numRows = tk.Entry(window)
    numRows.grid(row=4, column=1)
    label = tk.Label(window, text="Number of columns")
    label.grid(row=5, column=1)
    numCols = tk.Entry(window)
    numCols.grid(row=6, column=1)
    custom = tk.Button(window, text="Custom", width=10, height=2, command=lambda: play(int(numMines.get()), int(numRows.get()), int(numCols.get()), noGuess))
    custom.grid(row=7, column=1)
    window.mainloop()


if __name__ == "__main__":
    main()