import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog

from PIL import Image


def get_input_folder():
    folder_path1 = filedialog.askdirectory(initialdir=initial_dir,
                                           title="Select Source Directory")
    input_folder_entry.delete(0, tk.END)  # Clear entry widget
    input_folder_entry.insert(0, folder_path1)  # Insert the selected folder path


def get_output_folder():
    folder_path2 = filedialog.askdirectory(title="Select Destination Directory")
    output_folder_entry.delete(0, tk.END)  # Clear entry widget
    output_folder_entry.insert(0, folder_path2)  # Insert the selected folder path


def option_selected(option):
    if option == "Portrait Wallpaper":
        print("Portrait Wallpaper")
        return "Portrait Wallpaper"
    elif option == "Landscape Wallpaper":
        print("Landscape Wallpaper")
        return "Landscape Wallpaper"
    elif option == "Ultrawide Wallpaper":
        print("Ultrawide Wallpaper")
        return "Ultrawide Wallpaper"


def organize_images():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    selected_option = option_selected(selected_option_menu.get())

    if not os.path.exists(input_folder):
        print("Source Folder Not Found!")
        return
    if not os.path.exists(output_folder):
        print("Destination Folder Not Found!")
        return

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.igf', '.bmp')):
            image_path = os.path.join(input_folder, filename)

            with Image.open(image_path) as img:
                width, height = img.size

                if selected_option == "Portrait Wallpaper" and height > width:
                    new_folder = os.path.join(output_folder, "Portrait")
                elif selected_option == "Landscape Wallpaper" and 1920 <= width < 3840:
                    new_folder = os.path.join(output_folder, "Landscape")
                elif selected_option == "Ultrawide Wallpaper" and width >= 3840:
                    new_folder = os.path.join(output_folder, "Ultrawide")
                else:
                    continue

                os.makedirs(new_folder, exist_ok=True)

                new_filename = f"{filename.split('.')[0]}_{width}x{height}.{filename.split('.')[-1]}"
                new_filepath = os.path.join(output_folder, new_filename)

                try:
                    time.sleep(0.1)
                    shutil.move(image_path, new_filepath)
                    output_text.insert(tk.END, f"Moved: {filename} to {new_filepath}\n")
                except Exception as e:
                    output_text.insert(tk.END, f"Error moving {filename}: {e}\n")


initial_dir = os.path.join(os.path.expanduser("~"), "Pictures")

root = tk.Tk()
root.title("IMAGE SORTER")
root.configure(background="#343434")

# Create button to choose source directory
button1 = tk.Button(root,
                    text="Choose Source Directory",
                    font=("Courier New", 12),
                    command=get_input_folder)
button1.pack(padx=10, pady=5, anchor="w")
button1.configure(background="#565656", foreground="#F3F3F3")

# Create input folder entry
input_folder_entry = tk.Entry(root, font=("Courier New", 12), width=60)
input_folder_entry.pack(padx=10, pady=10, anchor="w")

# Create button to choose destination directory
button2 = tk.Button(root,
                    text="Choose Destination Directory",
                    font=("Courier New", 12),
                    command=get_output_folder)
button2.pack(padx=10, pady=5, anchor="w")
button2.configure(background="#565656", foreground="#F3F3F3")

# Create output folder entry
output_folder_entry = tk.Entry(root, font=("Courier New", 12), width=60)
output_folder_entry.pack(padx=10, pady=10, anchor="w")

selected_option_menu = tk.StringVar(root)
selected_option_menu.set("Choose Wallpaper")

# Create drop down list for function selection
option_menu = tk.OptionMenu(root, selected_option_menu,
                            "Portrait Wallpaper",
                            "Landscape Wallpaper",
                            "Ultrawide Wallpaper")
option_menu.pack(padx=10, pady=5, anchor="w")
option_menu.configure(background="#565656", foreground="#F3F3F3")

# Create the start button
button3 = tk.Button(root, text="Sort Images", font=("Courier New", 12),
                    command=organize_images, width=20)
button3.pack(padx=10, pady=5, anchor="se")
button3.configure(background="#565656", foreground="#F3F3F3")

# Create output display area and text
output_text = tk.Text(root, height=10, width=80)
output_text.pack(padx=10, pady=10, anchor="w")
output_text.configure(background="#CCCCCC", foreground="#000000")

root.mainloop()
