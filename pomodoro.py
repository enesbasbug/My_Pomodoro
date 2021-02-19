
# Import libraries
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import errno
import datetime
import time

# FUNCTIONS

# Countdown
def count(timer):
    global is_break
    global cnt
    global periodCounter

    if timer <= -1:
        subprocess.call(["afplay", "xfairy01.mp3"])
        os.system("afplay xfairty01.mp3")

        # toggle is break
        is_break = not is_break

        # prompt and start new session
        if is_break != 0:
            prompt_answer = messagebox.askquestion("Session Ended!", "Are you ready for a break?", icon='info')
        else:
            prompt_answer = messagebox.askquestion("Time's up!", "Ready for a new session?", icon='info')



        if prompt_answer == 'yes' and is_break:
            #subprocess.call(["afplay", "pom/xfairy01.mp3"])
            count(BREAK)
            
        elif prompt_answer == 'no':
            subprocess.call(["afplay", "xfairy01.mp3"])
            stop_count()
        else:
            subprocess.call(["afplay", "xfairy01.mp3"])
            periodCounter += 1
            count(SESSION)
        return

    # divmod(dividend, divisor)
    #   dividend - A Number. The number you want to divide
    #   divisor	 - A Number. The number you want to divide with
    #       divmod(5, 2) ---> (2,1)

    m, s = divmod(timer, 60)
    time_label.configure(text='{:02d}:{:02d}'.format(m, s))
    if is_break:
        cnt_label.configure(text='BREAK!')
    else:
        cnt_label.configure(text='Streak: {}'.format(periodCounter))
    cnt = root.after(1000, count, timer - 1)

def write_to_txt(session_time):

    # windows = name = os.path.join('C:\Users\YourUser\Desktop', name)
    # os      = os.chdir('C:\Users\YourUser\Desktop')
    
    filename = '/Users/senesbasbug/Desktop/pomodoro.txt'

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))

        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    current_time = datetime.datetime.now()
    now = current_time.strftime("%H:%M:%S")
    today = current_time.strftime("%A")
    date = current_time.strftime("%d/%m/%Y")

    total_time = 50*int(session_time)
    total_hours = (total_time / 60)

    with open(filename, "a") as f:
            f.write("You've studied {} minutes, in {} period - Date: {}, Day: {}, Time: {} \n".format(total_time, session_time, date, today, now))
            f.close()

# stops the countdown and resets the counter
def stop_count():
    global periodCounter
    global is_break
    write_to_txt(str(periodCounter))
    time_label.configure(text='{:02d}:{:02d}'.format(0, 0))
    periodCounter = 0
    is_break = False
    
    cnt_label.configure(text='Streak: {}'.format(0))
    start_btn.configure(text="Start", command=lambda: start())
    root.destroy()



# starts counting loop
def start():
    global SESSION
    global periodCounter
    
    periodCounter += 1
    start_btn.configure(command=tk.DISABLED)
    count(SESSION)


#_________________________________________________________________________________________________________
BREAK = 60*10
SESSION = 60*50 

# session counter
periodCounter = 0

# tells the program if the next session is going to be a break or not
is_break = False


# TKINTER SETTINGS

# root & title
root = tk.Tk()
root.title('Pomodoro 50x10')
root.geometry('200x90')

# labels
# main label area
main_label = tk.Frame(root)
main_label.grid(row=3, column=3, padx='15', pady='15')

# _________________________________________________________________________________________________________________________

# time label
time_label = tk.Label(main_label, text='00:00')
time_label.grid(row=2, column=1, columnspan=1)

# placeholder label
placeholder_label = tk.Label(main_label, text=' | | ')
placeholder_label.grid(row=2, column=2)

# counter label
cnt_label = tk.Label(main_label, text='Streak: 0')
cnt_label.grid(row=2, column=3, columnspan=1)

# buttons
start_btn = tk.Button(main_label, text="Start", command=start)
start_btn.grid(row=3, column=1)
stop_btn = tk.Button(main_label, text="Exit", command=root.destroy)
# stop_btn = tk.Button(main_label, text="Stop", command=stop_count)
stop_btn.grid(row=3, column=3)
root.resizable(False, False)
# MAINLOOP
root.mainloop()