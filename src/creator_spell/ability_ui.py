import tkinter as tk
import tkinter.ttk as ttk

class AbilityUI:
    def __init__(self, root, back_to_menu):
        self.root = root
        self.back_to_menu = back_to_menu  # Store the callback function to return to the main menu

        self.setup_ui(root)

    def setup_ui(self, root):
        # Create a frame to hold the ability UI
        # ability_frame = ttk.Frame(root)
        # ability_frame.pack()
        
        # Create a button to go back to the main menu
        back_to_menu_button = ttk.Button(root, text="Return", command=self.back_to_menu)
        back_to_menu_button.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=20, sticky="w")

        # Create a list of list[1, 3, 5, 8, 10, 13, 15, 18, 20, 23, 25, 28, 30, 33, 35, 38, 40]
        ability_levels = ['LVL 1', 'LVL 3', 'LVL 5', 'LVL 8', 'LVL 10', 'LVL 13', 'LVL 15', 'LVL 18', 'LVL 20', 'LVL 23', 'LVL 25', 'LVL 28', 'LVL 30', 'LVL 33', 'LVL 35', 'LVL 38', 'LVL 40']
        ability_level_label = ttk.Label(root, text="Ability Level:")
        ability_level_label.grid(row=1, column=0, padx=(10, 0), pady=20, sticky="w")
        ability_level_dropdown = ttk.Combobox(root, textvariable="", values=ability_levels, state="readonly")
        ability_level_dropdown.grid(row=1, column=1, padx=(10, 0), pady=20, sticky="w")
        # ability_level_dropdown.bind("<ButtonPress>", lambda _: self.on_modify())
        
        ability_level_dropdown.bind("<<ComboboxSelected>>", lambda _: ability_level_dropdown.selection_clear())

        # Bind focus out event to reset selection
        ability_level_dropdown.bind("<FocusOut>", lambda _: ability_level_dropdown.selection_clear())

        # Create a label for the ability name
        ability_name_label = ttk.Label(root, text="Ability Name:")
        ability_name_label.grid(row=2, column=0, padx=(10, 0), pady=20, sticky="w")
        ability_name_entry = ttk.Entry(root)
        ability_name_entry.grid(row=2, column=1, padx=(10, 0), pady=20, sticky="w")

        # Create a label for the ability description
        ability_description_label = ttk.Label(root, text="Ability Description:")
        ability_description_label.grid(row=3, column=0, padx=(10, 0), pady=20, sticky="w")
        ability_description_entry = ttk.Entry(root)
        ability_description_entry.grid(row=3, column=1, padx=(10, 0), pady=20, sticky="w")

