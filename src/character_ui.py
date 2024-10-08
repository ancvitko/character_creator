# ui.py
import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from utils import PlaceholderEntry
from stats_calculator import calculate_and_save
from tkinter import filedialog, messagebox
from abilities import ABILITIES
from ability_tooltip import Tooltip
from passives import PASSIVES
from passives_tooltip import PassivesTooltip



class CharacterCreatorUI:
    def __init__(self, root, back_to_menu):
        self.root = root
        self.back_to_menu = back_to_menu  # Store the callback function to return to the main menu
        self.start_stat_vars = []
        self.expertise_vars = {}
        self.ability_vars = []  # Store ability dropdown variables
        self.passive_vars = []  # Store passive ability dropdown variables
        self.modified = False  # Flag to track changes

        self.setup_ui(root)

    def on_modify(self, *_):
        """Sets the modified flag to True whenever a change is made."""
        self.modified = True

    def load_character(self):
        # Open a file dialog to select a character file with default directory './characters/'
        # Create characters directory if it doesn't exist
        if not os.path.exists("characters"):
            os.makedirs("characters")
        filename = filedialog.askopenfilename(initialdir='./characters/', filetypes=[("Text Files", "*.txt")])
        if not filename:
            return  # If no file is selected, return

        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

                # Read character name
                name_line = lines[0].strip()
                name = name_line.split(": ")[1] if ": " in name_line else ""
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, name)

                # Read species
                species_line = lines[1].strip()
                species = species_line.split(": ")[1] if ": " in species_line else ""
                self.species_var.set(species)

                # Read rarity
                rarity_line = lines[2].strip()
                rarity = rarity_line.split(": ")[1] if ": " in rarity_line else ""
                self.rarity_var.set(self.map_rarity_to_slider(rarity))

                # Read expertise levels
                for i, line in enumerate(lines[5:14]):  # Adjusted the start index to match expertise levels
                    if ": " in line:
                        stat, level = line.split(": ")
                        self.expertise_vars[stat.split()[0]].set(self.map_expertise_to_slider(level.strip()))

                # Read Level 1 stats
                for i, line in enumerate(lines[17:25]):  # Adjusted the start index to match level 1 stats
                    if ": " in line:
                        stat, value = line.split(": ")
                        self.start_stat_vars[i].set(value.strip())

                # Find the abilities section
                abilities_start = None
                for i, line in enumerate(lines):
                    if "Abilities:" in line:
                        abilities_start = i + 1  # Abilities section starts after this line
                        break

                if abilities_start is None:
                    raise ValueError("Abilities section not found in the file.")

                # Read Abilities
                abilities = []
                for i in range(abilities_start, len(lines)):
                    line = lines[i].strip()
                    if line == "":
                        continue
                    if line.startswith("LVL "):  # This identifies each ability
                        ability_name = line.split(": ")[1].strip()
                        abilities.append(ability_name)

                # Update the ability dropdowns with loaded abilities
                for i, ability_var in enumerate(self.ability_vars):
                    if i < len(abilities):
                        ability_var.set(abilities[i])
                    else:
                        ability_var.set("")  # Reset any leftover ability vars if not present in the file

                # Find the passives section
                passives_start = None
                for i, line in enumerate(lines):
                    if "Passives:" in line:
                        passives_start = i + 1
                        break

                if passives_start is None:
                    raise ValueError("Passives section not found in the file.")
                
                # Read Passives
                passives = []
                for i in range(passives_start, len(lines)):
                    line = lines[i].strip()
                    if line == "":
                        continue
                    if line.startswith("Passive #"):  # This identifies each passive
                        passive_name = line.split(": ")[1].strip()
                        passives.append(passive_name)

                # Update the passive dropdowns with loaded passives
                for i, passive_var in enumerate(self.passive_vars):
                    if i < len(passives):
                        passive_var.set(passives[i])
                    else:
                        passive_var.set("")  # Reset any leftover passive vars if not present in the file


            self.modified = False  # Reset the modified flag after loading a character
        except Exception as e:
            messagebox.showerror("Error", f"Could not load character: {e}")


    def map_rarity_to_slider(self, rarity):
        mapping = {"Common": 0, "Uncommon": 1, "Rare": 2, "Epic": 3, "Legendary": 4}
        return mapping.get(rarity, 0)

    
    def map_slider_to_rarity(self, value):
        mapping = {0: "Common", 1: "Uncommon", 2: "Rare", 3: "Epic", 4: "Legendary"}
        return mapping.get(value, "Common")


    def map_expertise_to_slider(self, expertise):
        mapping = {"VERY_LOW": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "VERY_HIGH": 4}
        return mapping.get(expertise, 2)

    def map_slider_to_expertise(self, value):
        mapping = {0: "VERY_LOW", 1: "LOW", 2: "MEDIUM", 3: "HIGH", 4: "VERY_HIGH"}
        return mapping.get(value, "MEDIUM")

    def back_to_menu_with_prompt(self):
        """Check if there are unsaved changes before returning to the menu."""
        if self.modified:
            # Ask user if they want to discard unsaved changes
            confirm = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before leaving?",
                icon='warning'
            )
            if confirm:  # Yes, save changes
                calculate_and_save(
                    self.name_entry.get(),
                    self.species_var.get(),  # Get the selected species
                    self.map_slider_to_rarity(self.rarity_var.get()),
                    self.start_stat_vars,
                    self.expertise_vars,
                    self.ability_vars,
                    self.modified,
                )
            elif confirm is False:  # No, don't save changes
                self.modified = False  # Reset the modified flag
                self.back_to_menu()  # Proceed to menu
                
            elif confirm is None:  # Cancel, don't go back
                return
        else:
            self.back_to_menu()  # No changes, proceed to menu

    def setup_ui(self, root):

         # Add a Back Button to return to the main menu
        back_button = ttk.Button(root, text="Return", command=self.back_to_menu_with_prompt)
        back_button.grid(row=0, column=0, padx=(0, 100), pady=10)
        
        # Load Button
        load_button = ttk.Button(root, text="Load Character", command=self.load_character)
        load_button.grid(row=0, column=0, padx=(150, 0), pady=20)
        

        self.name_entry = ttk.Entry(root, justify="left")
        # Bind modifications to fields
        self.name_entry.bind("<KeyRelease>", self.on_modify)
        self.rarity_var = tk.IntVar(value=0)
        
        # Pre-established species list
        species_list = ["Beast", "Dragon", "Elf", "Elemental", "Giant", "Human", "Mech", "Minotaur", "Ravenfolk", "Satyr", "Spirit", "Undead"]  # Add more species as needed
        self.species_var = tk.StringVar(value=species_list[0])  # Default to the first species

        # Character Name
        name_label = ttk.Label(root, text="Character Name:", anchor="w").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.name_entry.grid(row=1, column=1, padx=(10, 0), pady=10)

        # Species Dropdown
        ttk.Label(root, text="Species:", anchor="w").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        species_dropdown = ttk.Combobox(root, textvariable=self.species_var, values=species_list, state="readonly")
        species_dropdown.grid(row=2, column=1, padx=(35, 0), pady=10)

        species_dropdown.bind("<ButtonPress>", lambda _: self.on_modify())
        
        species_dropdown.bind("<<ComboboxSelected>>", lambda _: species_dropdown.selection_clear())

        # Bind focus out event to reset selection
        species_dropdown.bind("<FocusOut>", lambda _: species_dropdown.selection_clear())

        

        # Rarity slider - align with expertise labels
        ttk.Label(root, text="Rarity:", anchor="w").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        rarity_slider = ttk.Scale(root, from_=0, to=4, orient="horizontal", variable=self.rarity_var, 
                                command=lambda v: self.rarity_var.set(int(float(v))))
        rarity_slider.grid(row=3, column=1, padx=(70, 0), pady=10, sticky="w")  # Align with the label

        rarity_slider.bind("<ButtonPress>", lambda _: self.on_modify())

        # Rarity label (dynamic)
        self.rarity_label = ttk.Label(root, text=self.map_slider_to_rarity(self.rarity_var.get()), anchor="w")
        self.rarity_label.grid(row=3, column=2, padx=0, pady=10, sticky="w")

        # Update rarity label when slider moves
        self.rarity_var.trace("w", lambda *_: self.rarity_label.config(text=self.map_slider_to_rarity(self.rarity_var.get())))
        
        # Expertise sliders for each stat
        stat_labels = ['HP', 'Speed', 'PHYS_ATK', 'PHYS_DEF', 'PIR_ATK', 'PIR_DEF', 'MAG_ATK', 'MAG_DEF']
        self.expertise_vars = {}

        for i, stat in enumerate(stat_labels):
            ttk.Label(root, text=f"{stat} Expertise:", anchor="w").grid(row=i+5, column=0, padx=20, pady=5, sticky="w")
            
            var = tk.IntVar(value=2)  # Default to 'MEDIUM'
            self.expertise_vars[stat] = var
            
            slider = ttk.Scale(root, from_=0, to=4, orient="horizontal", variable=var, command=lambda v, sv=var: sv.set(int(float(v))))
            slider.grid(row=i+5, column=1, padx=10, pady=5)

            expertise_label = ttk.Label(root, textvariable=tk.StringVar(value="MEDIUM"), anchor="w")
            expertise_label.grid(row=i+5, column=2, padx=10, pady=5, sticky="w")

            current_expertise_label = ttk.Label(root, text="MEDIUM", anchor="w", width=15)
            current_expertise_label.grid(row=i+5, column=2, padx=(0, 20), pady=5, sticky="w")

            var.trace("w", lambda *_, sv=var, cel=current_expertise_label: cel.config(text=self.map_slider_to_expertise(sv.get())))
            slider.bind("<ButtonPress>", lambda _: self.on_modify())

        # Starting stats inputs with placeholders
        self.start_stat_vars = [tk.StringVar() for _ in stat_labels]
        self.start_stat_entries = []

        for i, stat in enumerate(stat_labels):
            ttk.Label(root, text=f"Starting {stat}:", anchor="w").grid(row=i+5, column=4, padx=(50, 20), pady=5, sticky="w")
            entry = PlaceholderEntry(root, placeholder="1-20 recommended", textvariable=self.start_stat_vars[i], justify="left")
            entry.grid(row=i+5, column=5, padx=(0, 20), pady=5)
            self.start_stat_entries.append(entry)

        # Save Button
        save_button = ttk.Button(root, text="Save Character", command=lambda: (
            setattr(self, 'modified', calculate_and_save(
                self.name_entry.get(),
                self.species_var.get(),  # Get the selected species
                self.map_slider_to_rarity(self.rarity_var.get()),
                self.start_stat_vars,
                self.expertise_vars,
                self.ability_vars,
                self.passive_vars,
            ))
        ))


        save_button.grid(row=0, column=1, columnspan=1, pady=20)

        # Clear Values Button
        clear_button = ttk.Button(root, text="Clear Values", command=self.clear_values)
        clear_button.grid(row=0, column=2, pady=20)

        # Create a canvas for vertical lines
        canvas = tk.Canvas(root, width=3, bg="black")
        canvas.grid(row=0, column=3, rowspan=len(stat_labels) + 6, sticky='ns')  # Adjust rowspan as needed

        # Create a canvas for horizontal lines
        canvas = tk.Canvas(root, height=3, bg="black")
        canvas.grid(row=4, column=0, columnspan=9, sticky='ew')  # Adjust columnspan as needed

        # # Load and resize the image with the correct file extension
        # image = Image.open("./res/BelissaF2.png")  # Ensure the correct file extension is used
        # image = image.resize((200, 300), Image.LANCZOS)  # Better resampling filter
        # self.photo = ImageTk.PhotoImage(image)  # Store a reference to the image

        # # Create a label to display the image
        # image_label = ttk.Label(root, image=self.photo)  # Use the stored reference
        # image_label.grid(row=0, column=4, rowspan=5, padx=(20, 0), pady=20)

        canvas = tk.Canvas(root, height=3, bg="black")
        canvas.grid(row=13, column=0, columnspan=9, sticky='ew')  # Adjust rowspan as needed


        # Create a method to create dropdowns and save their variables
        def create_ability_dropdown(row, col, level, ability_list, descriptions, indexFlag):
            # Create a label for the ability
            if indexFlag != -1:
                ttk.Label(root, text=f"LVL {level} Ability #{indexFlag+1}: ", anchor="w").grid(row=row, column=col, padx=20, pady=5, sticky="w")
            else:
                ttk.Label(root, text=f"LVL {level} Ability:", anchor="w").grid(row=row, column=col, padx=20, pady=5, sticky="w")

            # Create a StringVar for the dropdown and store it in the list
            ability_var = tk.StringVar(value="")  # Default to empty value
            self.ability_vars.append(ability_var)  # Store the variable for later use

            # Create the dropdown
            ability_dropdown = ttk.Combobox(root, textvariable=ability_var, values=ability_list, state="readonly")
            ability_dropdown.grid(row=row, column=col + 1, padx=(35, 0), pady=5)
            ability_dropdown.bind("<ButtonPress>", lambda _: self.on_modify())

            # Create a tooltip for the ability dropdown
            tooltip = Tooltip(ability_dropdown)
            tooltip.set_descriptions(descriptions)  # Set the ability descriptions for tooltips

            # Bind selection event to clear focus selection
            ability_dropdown.bind("<<ComboboxSelected>>", lambda _, ad=ability_dropdown: ad.selection_clear())
            
            # Bind focus out event to reset selection
            ability_dropdown.bind("<FocusOut>", lambda _, ad=ability_dropdown: ad.selection_clear())

        # Create all the ability dropdowns
        for i in range(4):
            create_ability_dropdown(14 + i, 0, 1, list(ABILITIES['LVL1_ABILITIES'].keys()), ABILITIES['LVL1_ABILITIES'], i)

        create_ability_dropdown(18, 0, 3, list(ABILITIES['LVL3_ABILITIES'].keys()), ABILITIES['LVL3_ABILITIES'], -1)
        create_ability_dropdown(19, 0, 5, list(ABILITIES['LVL5_ABILITIES'].keys()), ABILITIES['LVL5_ABILITIES'], -1)
        create_ability_dropdown(20, 0, 8, list(ABILITIES['LVL8_ABILITIES'].keys()), ABILITIES['LVL8_ABILITIES'], -1)
        create_ability_dropdown(21, 0, 10, list(ABILITIES['LVL10_ABILITIES'].keys()), ABILITIES['LVL10_ABILITIES'], -1)
        create_ability_dropdown(22, 0, 13, list(ABILITIES['LVL13_ABILITIES'].keys()), ABILITIES['LVL13_ABILITIES'], -1)
        create_ability_dropdown(23, 0, 15, list(ABILITIES['LVL15_ABILITIES'].keys()), ABILITIES['LVL15_ABILITIES'], -1)
        create_ability_dropdown(14, 3, 18, list(ABILITIES['LVL18_ABILITIES'].keys()), ABILITIES['LVL18_ABILITIES'], -1)
        create_ability_dropdown(15, 3, 20, list(ABILITIES['LVL20_ABILITIES'].keys()), ABILITIES['LVL20_ABILITIES'], -1)
        create_ability_dropdown(16, 3, 23, list(ABILITIES['LVL23_ABILITIES'].keys()), ABILITIES['LVL23_ABILITIES'], -1)
        create_ability_dropdown(17, 3, 25, list(ABILITIES['LVL25_ABILITIES'].keys()), ABILITIES['LVL25_ABILITIES'], -1)
        create_ability_dropdown(18, 3, 28, list(ABILITIES['LVL28_ABILITIES'].keys()), ABILITIES['LVL28_ABILITIES'], -1)
        create_ability_dropdown(19, 3, 30, list(ABILITIES['LVL30_ABILITIES'].keys()), ABILITIES['LVL30_ABILITIES'], -1)
        create_ability_dropdown(20, 3, 33, list(ABILITIES['LVL33_ABILITIES'].keys()), ABILITIES['LVL33_ABILITIES'], -1)
        create_ability_dropdown(21, 3, 35, list(ABILITIES['LVL35_ABILITIES'].keys()), ABILITIES['LVL35_ABILITIES'], -1)
        create_ability_dropdown(22, 3, 38, list(ABILITIES['LVL38_ABILITIES'].keys()), ABILITIES['LVL38_ABILITIES'], -1)
        create_ability_dropdown(23, 3, 40, list(ABILITIES['LVL40_ABILITIES'].keys()), ABILITIES['LVL40_ABILITIES'], -1)

        """
        PASSIVE ABILITIES
        """
        ttk.Label(root, text=f"Passive Abilities", anchor="w").grid(row=0, column=4, padx=20, pady=5, sticky="w")
        for i in range(4):
            row = i // 2 + 1
            col = i % 2 + 4

            ttk.Label(root, text=f"Passive #{i+1}", anchor="w").grid(row=row, column=col, padx=(20, 0), pady=5, sticky="w")
            # Create a StringVar for the dropdown and store it in the list
            passive_var = tk.StringVar(value="")
            self.passive_vars.append(passive_var)

            # Create the dropdown
            passive_dropdown = ttk.Combobox(root, textvariable=passive_var, values=list(PASSIVES.keys()), state="readonly")
            passive_dropdown.grid(row=row, column=col, padx=(120,0), pady=5)
            passive_dropdown.bind("<ButtonPress>", lambda _: self.on_modify())

            # Create a tooltip for the ability dropdown
            tooltip = PassivesTooltip(passive_dropdown)
            tooltip.set_descriptions(PASSIVES)

            # Bind selection event to clear focus selection
            passive_dropdown.bind("<<ComboboxSelected>>", lambda _, ad=passive_dropdown: ad.selection_clear())

            # Bind focus out event to reset selection
            passive_dropdown.bind("<FocusOut>", lambda _, ad=passive_dropdown: ad.selection_clear())

    
    # Function to clear values
    def clear_values(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all values?"):
            self.name_entry.delete(0, tk.END)  # Clear the character name entry
            self.species_var.set("")  # Reset species selection
            self.rarity_var.set(0)  # Reset rarity slider to default
            for var in self.expertise_vars.values():
                var.set(2)  # Reset expertise sliders to 'MEDIUM'
            for var in self.start_stat_vars:
                var.set("")  # Clear starting stat entries
            for var in self.passive_vars:
                var.set("")  # Reset all dropdowns to an empty value or default value

            # Clear ability dropdowns
            for var in self.ability_vars:
                var.set("")  # Reset all dropdowns to an empty value or default value
            self.modified = False