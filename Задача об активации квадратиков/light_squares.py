from tkinter import *

N, M = 5, 6
bools = [[False for j in range(M)] for i in range(N)]
prod = N * M

def butfunc(i, j):
    def func():
        A = [(i, j)]
        if i > 0:
            A.append((i-1, j))
        if j > 0:
            A.append((i, j-1))
        if i < N-1:
            A.append((i+1, j))
        if j < M-1:
            A.append((i, j+1))
        for tup in A:
            bools[tup[0]][tup[1]] = not bools[tup[0]][tup[1]]
            if bools[tup[0]][tup[1]]:
                buttons[tup[0]][tup[1]]["bg"] = "lightblue"
            else:
                buttons[tup[0]][tup[1]]["bg"] = "darkblue"
        if sum(map(sum, bools)) == prod:
            win_button.grid()
    return func

root = Tk()
root.geometry("600x600")

Label(text="Активируй все квадратики", font=("Arial", 20)).grid(row=0, column=0, columnspan=M)
buttons = [[Button(width=3, height=3, bg="darkblue", command=butfunc(i, j)) for j in range(M)] for i in range(N)]
for i in range(N):
    for j in range(M):
        buttons[i][j].grid(row=i+1, column=j, sticky="NSEW", padx=1, pady=1)
win_button = Button(text="You Win! Click to exit", width=30, height=3, command=root.destroy)
win_button.grid(row=N+1, column=0, columnspan=M)
win_button.grid_remove()
col_count, row_count = root.grid_size()
for row in range(1, row_count):
    root.grid_rowconfigure(row, minsize=100)
for col in range(col_count):
    root.grid_columnconfigure(col, minsize=100)

root.mainloop()