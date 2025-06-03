import os
os.environ["SDL_AUDIODRIVER"] = "dummy"
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import threading
import random
import time

# Initialize pygame mixer for sounds
pygame.mixer.init()

# Paths to assets
SOUNDS_DIR = os.path.join("sounds")
JUMPSCARE_IMAGE = os.path.join("Jumpscares", "jumpscare.png")
JUMPSCARE_SOUND = os.path.join("Jumpscares", "jumpscare.wav")
MESSAGES = [
    "Did you hear that?",
    "I'm watching you...",
    "Don't look behind you.",
    "You can't escape.",
    "It's too quiet..."
]

# GUI setup
root = tk.Tk()
root.title("Ghost in the Machine")

# Feature toggles (must be after root is created)
features = {
    "random_sounds": tk.BooleanVar(root, value=True),
    "jumpscare": tk.BooleanVar(root, value=True),
    "creepy_messages": tk.BooleanVar(root, value=True)
}

def play_random_sound():
    if not features["random_sounds"].get():
        return
    sounds = [f for f in os.listdir(SOUNDS_DIR) if f.endswith(".wav")]
    if sounds:
        sound_file = os.path.join(SOUNDS_DIR, random.choice(sounds))
        try:
            pygame.mixer.Sound(sound_file).play()
        except Exception as e:
            print(f"Error playing sound: {e}")

def show_jumpscare():
    if not features["jumpscare"].get():
        return
    top = tk.Toplevel(root)
    top.attributes('-fullscreen', True)
    try:
        img = Image.open(JUMPSCARE_IMAGE)
        img = img.resize((top.winfo_screenwidth(), top.winfo_screenheight()), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=photo)
        label.image = photo
        label.pack()
        try:
            pygame.mixer.Sound(JUMPSCARE_SOUND).play()
        except Exception as e:
            print(f"Error playing jumpscare sound: {e}")
        top.after(2000, top.destroy)  # Show for 2 seconds
    except Exception as e:
        print(f"Error showing jumpscare: {e}")
        top.destroy()

def show_creepy_message():
    if not features["creepy_messages"].get():
        return
    message = random.choice(MESSAGES)
    messagebox.showinfo("...", message)

def random_events():
    while True:
        time.sleep(random.randint(10, 30))
        event = random.choice([play_random_sound, show_jumpscare, show_creepy_message])
        root.after(0, event)

tk.Checkbutton(root, text="Random Sounds", variable=features["random_sounds"]).pack(anchor='w')
tk.Checkbutton(root, text="Jumpscares", variable=features["jumpscare"]).pack(anchor='w')
tk.Checkbutton(root, text="Creepy Messages", variable=features["creepy_messages"]).pack(anchor='w')

tk.Button(root, text="Test Jumpscare", command=show_jumpscare).pack(pady=10)
tk.Button(root, text="Test Sound", command=play_random_sound).pack(pady=10)
tk.Button(root, text="Test Message", command=show_creepy_message).pack(pady=10)

# Start random events in a background thread
threading.Thread(target=random_events, daemon=True).start()

root.mainloop()