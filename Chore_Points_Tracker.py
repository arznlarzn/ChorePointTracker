import tkinter as tk
from tkinter import messagebox
from tkinter import Menu

bunk_points_file = "bunk_points.txt"
bunk_points = {}

def save_bunk_points():
    with open(bunk_points_file, "w") as file:
        for bunk_key, points in bunk_points.items():
            bunk_number, person = bunk_key
            bunk_key_str = str(bunk_key)
            file.write(f"{bunk_key_str}:{points}\n")

def load_bunk_points():
    try:
        with open(bunk_points_file, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) != 2:
                    # Skip this line if it doesn't have the expected format
                    continue
                
                bunk_key_str, points = parts
                bunk_key_parts = bunk_key_str.strip("()").split(", ")
                if len(bunk_key_parts) != 2:
                    # Skip this line if bunk key format is invalid
                    continue
                
                bunk_number, person = bunk_key_parts
                bunk_points[(int(bunk_number), person.strip("'"))] = int(points)
    except FileNotFoundError:
        # If file doesn't exist, no data needs to be loaded
        pass

def add_points():
    bunk_number = bunk_entry.get()
    points = points_entry.get()
    person = person_var.get()
    
    #checking that Bunk number and Points are intergers, and throw error/warning if not
    if not bunk_number.isdigit() or not points.isdigit():
        messagebox.showerror("Error", "Please enter valid bunk number and points.")
        return
    
    bunk_number = int(bunk_number)
    points = int(points)
    
    #checking that bunk_numbers range from 1 - 76
    if not 1 <= bunk_number <= 76:
        messagebox.showerror("Error", "Bunk number must be between 1 and 76.")
        return
    
    bunk_key = (bunk_number, person)

    if bunk_key not in bunk_points:
        bunk_points[bunk_key] = 0
    
    #Actually adding the new points to the total, while also throwing a messagebox up for the total amount of points for the user to see.
    bunk_points[bunk_key] += points
    messagebox.showinfo("Success", f"{points} points added to bunk {bunk_number} ({person}). Total points for bunk {bunk_number} ({person}): {bunk_points[bunk_key]}")
    save_bunk_points()

def remove_points():
    bunk_number = bunk_entry.get()
    points = points_entry.get()
    person = person_var.get()

    if not bunk_number.isdigit() or not points.isdigit():
        messagebox.showerror("Error", "Please enter a valid bunk number and points.")
        return
    
    bunk_number = int(bunk_number)
    points = int(points)

    bunk_key = (bunk_number, person)

    if bunk_key not in bunk_points:
        bunk_points[bunk_key] = 0
    
    if points > bunk_points[bunk_key]:
        messagebox.showerror("Error", "Cannot remove more points than are available.")
        return

    bunk_points[bunk_key] -= points
    messagebox.showinfo("Success!", f"{points} points removed from bunk {bunk_number} ({person}). Total points for bunk {bunk_number}: {bunk_points[bunk_key]}")
    save_bunk_points()

def check_points():
    bunk_number = bunk_entry.get()
    person = person_var.get()
    
    if not bunk_number.isdigit():
        messagebox.showerror("Error", "Please enter a valid bunk number.")
        return
    
    bunk_number = int(bunk_number)
    
    if not 1 <= bunk_number <= 76:
        messagebox.showerror("Error", "Bunk number must be between 1 and 76.")
        return
    
    bunk_key = (bunk_number, person)

    if bunk_key in bunk_points:
        messagebox.showinfo("Points", f"Total points for bunk {bunk_number} ({person}): {bunk_points[bunk_key]}")
    else:
        messagebox.showinfo("Points", f"Bunk {bunk_number} ({person}) has not accumulated any points yet.")


def open_txt_file():
    try:
        import subprocess
        subprocess.Popen(['notepad', bunk_points_file])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

# Create main window
root = tk.Tk()
root.title("Chore Points Tracker")

# Load existing bunk points
load_bunk_points()

# Create widgets
bunk_label = tk.Label(root, text="Bunk Number:")
bunk_label.grid(row=0, column=0, padx=5, pady=5)

bunk_entry = tk.Entry(root)
bunk_entry.grid(row=0, column=1, padx=5, pady=5)

points_label = tk.Label(root, text="Points:")
points_label.grid(row=1, column=0, padx=5, pady=5)

points_entry = tk.Entry(root)
points_entry.grid(row=1, column=1, padx=5, pady=5)

person_var = tk.StringVar(root, "A") # Default person is A
person_A_radio = tk.Radiobutton(root, text="A", variable=person_var, value="A")
person_A_radio.grid(row=2, column=0, padx=5, pady=5)
person_B_radio = tk.Radiobutton(root, text="B", variable=person_var, value="B")
person_B_radio.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Points", command=add_points)
add_button.grid(row=3, column=0, columnspan=2, padx=100, pady=5, sticky="we")

check_button = tk.Button(root, text="Check Points", command=check_points)
check_button.grid(row=4, column=0, columnspan=2, padx=100, pady=5, sticky="we")

remove_button = tk.Button(root, text="Remove Points", command=remove_points)
remove_button.grid(row=5, column=0, columnspan=2, padx=100, pady=5, sticky="we")
# Start the GUI

menubar = Menu(root)
file = Menu(menubar, tearoff=0)
file.add_command(label="Check Points!", command=check_points)
file.add_command(label="Open as a text file", command=open_txt_file)
menubar.add_cascade(label="File", menu=file)
root.config(menu=menubar)

root.geometry("300x230")
root.mainloop()
