import tkinter as tk
import tkinter.ttk as ttk

class PassiveUI:
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


        passive_name_label = ttk.Label(root, text="Passive Name:")
        passive_name_label.grid(row=1, column=0, padx=(10, 0), pady=20, sticky="w")
        passive_name_entry = ttk.Entry(root)
        passive_name_entry.grid(row=1, column=1, padx=(10, 0), pady=20, sticky="w")

        passive_description1_label = ttk.Label(root, text="Passive Description #1:")
        passive_description1_label.grid(row=2, column=0, padx=(10, 0), pady=20, sticky="w")
        passive_description1_entry = ttk.Entry(root)
        passive_description1_entry.insert(0, "None")
        # Increase the width of the Entry element
        passive_description1_entry.configure(width=50)
        passive_description1_entry.grid(row=2, column=1, padx=(10, 0), pady=20, sticky="w")

        passive_value1_label = ttk.Label(root, text="Passive Value #1:")
        passive_value1_label.grid(row=3, column=0, padx=(10, 0), pady=20, sticky="w")
        passive_value1_entry = ttk.Entry(root,)
        passive_value1_entry.insert(0, "None")
        passive_value1_entry.grid(row=3, column=1, padx=(10, 0), pady=20, sticky="w")

        passive_description2_label = ttk.Label(root, text="Passive Description #2:")
        passive_description2_label.grid(row=4, column=0, padx=(10, 0), pady=20, sticky="w")
        passive_description2_entry = ttk.Entry(root,)
        passive_description2_entry.insert(0, "None")
        # Increase the width of the Entry element
        passive_description2_entry.configure(width=50)
        passive_description2_entry.grid(row=4, column=1, padx=(10, 0), pady=20, sticky="w")

        passive_value2_label = ttk.Label(root, text="Passive Value #2:")
        passive_value2_label.grid(row=5, column=0, padx=(10, 0), pady=20, sticky="w")
        passive_value2_entry = ttk.Entry(root,)
        passive_value2_entry.insert(0, "None")
        passive_value2_entry.grid(row=5, column=1, padx=(10, 0), pady=20, sticky="w")
        





