from tkinter import *

DARK_RED = "#6D0303"
GREEN = "green"
WHITE = "white"

root = Tk()
root.state('zoomed')
# root.attributes("-zoomed", True)
root.config(bg=DARK_RED)
root.resizable(False, False)
root.title("Casino")

hist_frame = Frame(root, bg=DARK_RED, width=500, height=950)
hist_frame.place(relx=0.7, rely=0.02)

hist_frame_case = Frame(hist_frame, bg=WHITE, highlightbackground=GREEN, highlightthickness=10, width=500, height=750)
hist_frame_case.place(relx=0, rely=0.15)

hist_lbl_title = Label(hist_frame, text="HISTORY", bg=DARK_RED, fg=WHITE, font=("Arial", 50))
hist_lbl_title.place(relx=0.5, rely=0.07, anchor=CENTER)

money_frame = Frame(root, bg=DARK_RED, highlightbackground=GREEN, highlightthickness=3, width=1930, height=80)
money_frame.place(relx=0.5, rely=0.95, anchor=CENTER)

with open("Graphic/ressources/money.txt", "r") as m:
    money = m.read()
money_txt = StringVar()
money_lbl = Label(money_frame, text="", bg=DARK_RED, fg="light_blue", font=("Arial", 30))
money_lbl.config(text=money + "$")
money_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

# root.bind("<F11>", root.toggle_fullscreen)
# root.tk.bind("<Escape>", root.end_fullscreen)
root.bind('<Escape>', quit)

root.mainloop()