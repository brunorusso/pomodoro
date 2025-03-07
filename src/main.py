import time
import os
import tkinter as tk
from threading import Thread

def pomodoro(work_duration, break_duration, cycles, update_ui):
    for cycle in range(cycles):
        for remaining in range(work_duration * 60, 0, -1):
            mins, secs = divmod(remaining, 60)
            update_ui(f"Cycle {cycle + 1} - Work for {mins:02d}:{secs:02d} minutes.")
        for remaining in range(break_duration * 60, 0, -1):
            mins, secs = divmod(remaining, 60)
            update_ui(f"Cycle {cycle + 1} - Break for {mins:02d}:{secs:02d} minutes.")
            time.sleep(1)
    update_ui("Pomodoro session complete!")
    time.sleep(1)
    duration = 1  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

def start_pomodoro():
    work_duration = int(work_duration_entry.get())
    break_duration = int(break_duration_entry.get())
    cycles = int(cycles_entry.get())
    Thread(target=pomodoro, args=(work_duration, break_duration, cycles, update_ui)).start()

def update_ui(message):
    status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pomodoro Timer")

    tk.Label(root, text="Work Duration (minutes):").pack()
    work_duration_entry = tk.Entry(root)
    work_duration_entry.pack()

    tk.Label(root, text="Break Duration (minutes):").pack()
    break_duration_entry = tk.Entry(root)
    break_duration_entry.pack()

    tk.Label(root, text="Number of Cycles:").pack()
    cycles_entry = tk.Entry(root)
    cycles_entry.pack()

    start_button = tk.Button(root, text="Start Pomodoro", command=start_pomodoro)
    start_button.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    root.mainloop()