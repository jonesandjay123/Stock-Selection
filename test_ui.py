import os
import datetime
import tkinter as tk
from tkinter import scrolledtext

def create_folder_and_file():
    today = datetime.date.today()
    folder_name = f"{today}_csv"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

        file_path = os.path.join(folder_name, "test.csv")
        with open(file_path, "w") as file:
            file.write("This is a test file.\n")
        output_message(f"Folder '{folder_name}' created and 'test.csv' added.")
    else:
        output_message(f"The folder '{folder_name}' already exists. No further action is needed.")

def output_message(message):
    text_area.insert(tk.END, f"{message}\n")
    text_area.see(tk.END)

def main():
    global text_area
    root = tk.Tk()
    root.title("Test UI")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    button = tk.Button(frame, text="Create Folder and File", command=create_folder_and_file)
    button.pack(padx=10, pady=10)

    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
    text_area.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
