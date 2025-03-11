import tkinter as tk
import pydirectinput
import ctypes
import time

user32 = ctypes.windll.user32

# Toggle
def toggle_status():
    global is_running, message_index
    is_running = not is_running
    status_label.config(text=f"Status: {'ON' if is_running else 'OFF'}")
    if is_running:
        message_index = 0
        perform_actions()

# Mode
def switch_mode(selected_mode):
    global mode
    mode = selected_mode
    toggle_button.config(state=tk.NORMAL)
    set_keybind_button.config(state=tk.NORMAL)
    remove_keybind_button.config(state=tk.NORMAL)
    keybind_entry.config(state='normal')

# State
is_running = False
keybind = None
message_index = 0

# Actions
def perform_actions():
    global message_index
    actions = {
        "(Axe Sideswing) Combat + Build": [
            ("f", 0.25),
            ("left_click", 0.7),
            ("1", 0.001),
            ("left_click_hold", 0.42),
            ("2", 0.001)
        ],
        "(Axe Sideswing) Combat": [
            ("f", 0.25),
            ("left_click", 0.7),
            ("1", 0.001),
            ("2", 0.001)
        ],
        "(Axe Upswing) Combat + Build": [
            ("f", 0.25),
            ("left_click", 0.8),
            ("1", 0.001),
            ("left_click_hold", 0.42),
            ("2", 0.001)
        ],
        "(Axe Upswing) Combat": [
            ("f", 0.25),
            ("left_click", 0.8),
            ("1", 0.001),
            ("2", 0.001)
        ],
        "(Pickaxe Sideswing) Combat + Build": [
            ("f", 0.25),
            ("left_click", 0.6),
            ("1", 0.001),
            ("left_click_hold", 0.42),
            ("2", 0.001)
        ],
        "(Pickaxe Sideswing) Combat": [
            ("f", 0.25),
            ("left_click", 0.6),
            ("1", 0.001),
            ("2", 0.001)
        ],
        "(Pickaxe Upswing) Combat + Build": [
            ("f", 0.25),
            ("left_click", 0.7),
            ("1", 0.001),
            ("left_click_hold", 0.42),
            ("2", 0.001)
        ],
        "(Pickaxe Upswing) Combat": [
            ("f", 0.25),
            ("left_click", 0.7),
            ("1", 0.001),
            ("2", 0.001)
        ],
        "EVE_DEAD Mode": [
            ("f", 0.25),
            ("left_click", 0.6),
            ("1", 0.001),
            ("f", 0.001),
            ("left_click_hold", 0.42),
            ("2", 0.001)
        ]
    }[mode]
    if is_running:
        action, delay = actions[message_index]
        if action == "f":
            pydirectinput.press("f")
        elif action == "left_click":
            pydirectinput.click()
        elif action == "left_click_hold":
            pydirectinput.mouseDown()
            time.sleep(delay)
            pydirectinput.mouseUp()
        elif action == "1":
            pydirectinput.press("1")
        elif action == "2":
            pydirectinput.press("2")
        message_index = (message_index + 1) % len(actions)
        root.after(int(delay * 1000), perform_actions)

# Keybind
def set_keybind():
    global keybind
    keybind = keybind_entry.get().upper()
    if len(keybind) == 1:
        keybind_label.config(text=f"Current Keybind: {keybind}")
        keybind_entry.config(state='disabled')
    else:
        keybind_label.config(text="Invalid Keybind: Must be a single character")

def remove_keybind():
    global keybind
    keybind = None
    keybind_label.config(text="Current Keybind: None")
    keybind_entry.config(state='normal')

def limit_keybind_entry(*args):
    value = keybind_var.get()
    if len(value) > 1:
        keybind_var.set(value[:1])

def check_key_press():
    if keybind:
        vk_code = ord(keybind)
        if user32.GetAsyncKeyState(vk_code) & 0x8000:
            toggle_status()
    root.after(100, check_key_press)

# UI
root = tk.Tk()
root.title("Sapper Macro")
root.geometry("300x200")

status_label = tk.Label(root, text="Status: OFF", font=("Arial", 12))
status_label.pack(side=tk.BOTTOM, pady=10)

toggle_button = tk.Button(root, text="Toggle On/Off", command=toggle_status, state=tk.DISABLED)
toggle_button.pack(side=tk.TOP, pady=10)

modes = [
    "(Axe Sideswing) Combat + Build",
    "(Axe Sideswing) Combat",
    "(Axe Upswing) Combat + Build",
    "(Axe Upswing) Combat",
    "(Pickaxe Sideswing) Combat + Build",
    "(Pickaxe Sideswing) Combat",
    "(Pickaxe Upswing) Combat + Build",
    "(Pickaxe Upswing) Combat",
    "EVE_DEAD Mode"
]
mode_var = tk.StringVar(root)
mode_var.set("Select Mode")
mode_dropdown = tk.OptionMenu(root, mode_var, *modes, command=switch_mode)
mode_dropdown.pack(side=tk.TOP, pady=10)

keybind_var = tk.StringVar()
keybind_var.trace_add('write', limit_keybind_entry)
keybind_entry = tk.Entry(root, textvariable=keybind_var, state=tk.DISABLED)
keybind_entry.pack(side=tk.TOP, pady=5)

keybind_buttons_frame = tk.Frame(root)
keybind_buttons_frame.pack(side=tk.TOP, pady=5)

set_keybind_button = tk.Button(keybind_buttons_frame, text="Set Keybind", command=set_keybind, state=tk.DISABLED)
set_keybind_button.pack(side=tk.LEFT, padx=5)

remove_keybind_button = tk.Button(keybind_buttons_frame, text="Remove Keybind", command=remove_keybind, state=tk.DISABLED)
remove_keybind_button.pack(side=tk.LEFT, padx=5)

keybind_label = tk.Label(root, text="Current Keybind: None", font=("Arial", 10))
keybind_label.pack(side=tk.TOP, pady=5)

root.after(100, check_key_press)
root.mainloop()