import tkinter as tk
import tkinter.ttk as ttk

class AbilityUI:
    def __init__(self, root, back_to_menu):
        self.root = root
        self.back_to_menu = back_to_menu  # Store the callback function to return to the main menu

        self.setup_ui(root)

    def setup_ui(self, root):
        # Create a frame to hold the ability UI
        ability_frame = ttk.Frame(root)
        ability_frame.pack()

        # Create a label for the ability name
        ability_name_label = ttk.Label(ability_frame, text="Ability Name:")
        ability_name_label.grid(row=0, column=0)
        ability_name_entry = ttk.Entry(ability_frame)
        ability_name_entry.grid(row=0, column=1)

        # Create a label for the ability description
        ability_description_label = ttk.Label(ability_frame, text="Ability Description:")
        ability_description_label.grid(row=1, column=0)
        ability_description_entry = ttk.Entry(ability_frame)
        ability_description_entry.grid(row=1, column=1)

        # Create a button to go back to the main menu
        back_to_menu_button = ttk.Button(ability_frame, text="Back to Menu", command=self.back_to_menu)
        back_to_menu_button.grid(row=2, column=0, columnspan=2)