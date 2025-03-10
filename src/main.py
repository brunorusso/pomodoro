import time
import os
import tkinter as tk
from threading import Thread
import webbrowser
import pystray
from PIL import Image, ImageDraw, ImageTk

# Variável global para controlar o estado de execução
running = False

def pomodoro(work_duration, break_duration, cycles, update_ui):
    global running
    for cycle in range(cycles):
        if not running:
            break
        for remaining in range(work_duration * 60, 0, -1):
            if not running:
                break
            mins, secs = divmod(remaining, 60)
            update_ui(f"Cycle {cycle + 1} - Work for {mins:02d}:{secs:02d} minutes.")
            time.sleep(1)
        if not running:
            break
        play_sound()
        for remaining in range(break_duration * 60, 0, -1):
            if not running:
                break
            mins, secs = divmod(remaining, 60)
            update_ui(f"Cycle {cycle + 1} - Break for {mins:02d}:{secs:02d} minutes.")
            time.sleep(1)
        if not running:
            break
        play_sound()
    update_ui("Pomodoro session complete!" if running else "Pomodoro session stopped!")

def play_sound():
    duration = 1  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

def start_pomodoro():
    global running
    running = True
    work_duration = int(work_duration_entry.get())
    break_duration = int(break_duration_entry.get())
    cycles = int(cycles_entry.get())
    Thread(target=pomodoro, args=(work_duration, break_duration, cycles, update_ui)).start()

def stop_pomodoro():
    global running
    running = False
    update_ui("Pomodoro session stopped!")
    work_duration_entry.delete(0, tk.END)
    break_duration_entry.delete(0, tk.END)
    cycles_entry.delete(0, tk.END)

def update_ui(message):
    status_label.config(text=message)

def open_about_page():
    webbrowser.open("https://brunorusso.com.br")

def minimize_to_tray():
    root.withdraw()
    create_tray_icon()

def create_tray_icon():
    # Create an image with an icon for the tray
    image = Image.new('RGB', (64, 64), color=(255, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 32, 32), fill=(255, 0, 0))


    # Create the tray icon
    icon = pystray.Icon("pomodoro", image, "Pomodoro Timer", menu=pystray.Menu(
        pystray.MenuItem("Show", show_window),
        pystray.MenuItem("Quit", quit_app)
    ))
    icon.run()

def show_window(icon, item):
    root.deiconify()
    icon.stop()

def quit_app(icon, item):
    icon.stop()
    root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pomodoro Timer")

    # Definir o ícone da janela
    icon_path = "pomodoro.ico"  # Caminho para o seu arquivo de ícone
    icon_image = ImageTk.PhotoImage(file=icon_path)
    root.iconphoto(False, icon_image)

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

    stop_button = tk.Button(root, text="Stop Pomodoro", command=stop_pomodoro)
    stop_button.pack()

    minimize_button = tk.Button(root, text="Minimize to Tray", command=minimize_to_tray)
    minimize_button.pack()

    close_button = tk.Button(root, text="Close", command=root.quit)
    close_button.pack()
    
    about_button = tk.Button(root, text="About", command=open_about_page)
    about_button.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    root.mainloop()