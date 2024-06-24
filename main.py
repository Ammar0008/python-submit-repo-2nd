import tkinter as tk

def on_click():
    label.config(text="Button clicked!")

root = tk.Tk()
root.title("Tkinter Example")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

button = tk.Button(root, text="Click Me", command=on_click)
button.pack(pady=20)

root.mainloop()
