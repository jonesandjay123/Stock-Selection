import os
import sys
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

def create_folder_and_file():
    console.delete(1.0, tk.END)  # 清空訊息欄
    api_key = api_key_entry.get()

    if not api_key:
        console_output("API Key cannot be empty.")
        return

    today = datetime.now().strftime('%Y-%m-%d')
    folder_name = f"{today}_csv"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        with open(os.path.join(folder_name, "test.csv"), "w") as f:
            f.write("This is a test.")
        console_output(f"Created folder '{folder_name}' and file 'test.csv'.")
    else:
        console_output(f"The folder '{folder_name}' already exists. No further action is needed.")
    
    console_output(f"API Key: {api_key}")

def console_output(message):
    console.insert(tk.END, f"{message}\n")
    console.see(tk.END)

app = tk.Tk()
app.title("Test UI")

api_key_label = tk.Label(app, text="API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(app)
api_key_entry.pack()

create_button = tk.Button(app, text="Create Folder and File", command=create_folder_and_file)
create_button.pack()

console_label = tk.Label(app, text="Console Output:")
console_label.pack()
console = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
console.pack()

app.mainloop()
