import tkinter.messagebox
from tkinter import *
from playsound import playsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
reps = 0
timer = ""


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    root.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
# Starts timer for the first time after start button is clicked
# and prevents subsequent clicks of start button from affecting the ongoing timer
def start_timer_first():
    global reps

    if reps:
        tkinter.messagebox.showwarning(title="Already running", message="Timer already started")
        return

    start_timer()


def start_timer():
    global reps
    reps += 1

    work_seconds = int(WORK_MIN * 60)
    short_break_seconds = int(SHORT_BREAK_MIN * 60)
    long_break_seconds = int(LONG_BREAK_MIN * 60)

    if reps % 8 == 0:
        count_down(long_break_seconds)
        timer_label.config(text="Break", fg=RED)
        playsound("long_alarm.wav")
    elif reps % 2 == 0:
        count_down(short_break_seconds)
        timer_label.config(text="Break", fg=PINK)
        playsound("short_alarm.wav")
    else:
        if reps > 1:
            playsound("long_alarm.wav")
        else:
            playsound("short_alarm.wav")
        count_down(work_seconds)
        timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global reps

    canvas.itemconfig(timer_text, text=f"{count // 60}:{count % 60:02}")

    if count > 0:
        global timer
        timer = root.after(1000, count_down, count - 1)
    else:
        start_timer()
        if (reps // 2) < 8:
            if reps % 2 == 0:
                checkmark_label.config(text=CHECK_MARK * (reps // 2))
        else:
            print(reps // 2)
            print("Hi")
            reset_timer()


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Pomodoro")
root.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 138, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", command=start_timer_first)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(column=2, row=2)

checkmark_label = Label(bg=YELLOW, fg="green", font=(FONT_NAME, 30, "bold"))
checkmark_label.grid(column=1, row=3, pady=20)

root.mainloop()
