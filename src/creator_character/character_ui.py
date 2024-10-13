# ui.py
import json
import os
import tkinter as tk
import math
from PIL import Image, ImageTk
from tkinter import ttk
from creator_character.utils import PlaceholderEntry, map_slider_to_expertise
from creator_character.stats_calculator import calculate_and_save, expertise_progression
from tkinter import filedialog, messagebox
from creator_character.ability_tooltip import Tooltip
from creator_character.passives_tooltip import PassivesTooltip
from PIL import ImageDraw
from PIL import ImageFont



class CharacterCreatorUI:
    def __init__(self, root, back_to_menu):
        self.root = root
        self.back_to_menu = back_to_menu  # Store the callback function to return to the main menu
        self.start_stat_vars = []
        self.expertise_vars = {}
        self.ability_vars = []  # Store ability dropdown variables
        self.passive_vars = []  # Store passive ability dropdown variables
        self.modified = False  # Flag to track changes
        self.current_level = 1
        self.current_health = 0
        self.current_speed = 0
        self.current_phys_atk = 0
        self.current_phys_def = 0
        self.current_pir_atk = 0
        self.current_pir_def = 0
        self.current_mag_atk = 0
        self.current_mag_def = 0

        self.setup_ui(root)
        self.drawPreview()

    def on_modify(self, *_):
        """Sets the modified flag to True whenever a change is made."""
        self.modified = True
        self.drawPreview()

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
                

            self.current_level = 1
            self.current_health = int(self.start_stat_vars[0].get())
            self.current_speed = int(self.start_stat_vars[1].get())
            self.current_phys_atk = int(self.start_stat_vars[2].get())
            self.current_phys_def = int(self.start_stat_vars[3].get())
            self.current_pir_atk = int(self.start_stat_vars[4].get())
            self.current_pir_def = int(self.start_stat_vars[5].get())
            self.current_mag_atk = int(self.start_stat_vars[6].get())
            self.current_mag_def = int(self.start_stat_vars[7].get())
            self.modified = False  # Reset the modified flag after loading a character
            self.drawPreview()
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
        species_list = ["Dragon", "Beast","Elf", "Elemental", "Giant", "Human", "Mech", "Minotaur", "Ravenfolk", "Satyr", "Spirit", "Undead"]  # Add more species as needed
        species_list.sort()  # Sort the species list
        self.species_var = tk.StringVar(value=species_list[0])  # Default to the first species

        # Character Name
        ttk.Label(root, text="Character Name:", anchor="w").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.name_entry.grid(row=1, column=1, padx=(10, 0), pady=10)

        # Species Dropdown
        ttk.Label(root, text="Species:", anchor="w").grid(row=2, column=0, padx=20, pady=10, sticky="w")
        species_dropdown = ttk.Combobox(root, textvariable=self.species_var, values=species_list, state="readonly")
        species_dropdown.grid(row=2, column=1, padx=(35, 0), pady=10)
        species_dropdown.bind("<ButtonPress>", lambda _: self.on_modify())   
        species_dropdown.bind("<<ComboboxSelected>>", lambda _: species_dropdown.selection_clear())
        species_dropdown.bind("<FocusOut>", lambda _: species_dropdown.selection_clear())

        
        # Rarity slider - align with expertise labels
        ttk.Label(root, text="Rarity:", anchor="w").grid(row=3, column=0, padx=20, pady=10, sticky="w")
        rarity_slider = ttk.Scale(root, from_=0, to=4, orient="horizontal", variable=self.rarity_var, command=lambda v: self.rarity_var.set(int(float(v))))
        rarity_slider.grid(row=3, column=1, padx=(70, 0), pady=10, sticky="w")  # Align with the label
        rarity_slider.bind("<ButtonRelease>", lambda _: self.on_modify())

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
            ttk.Label(root, text=f"Starting {stat}:", anchor="w").grid(row=i+5, column=4, padx=(20, 20), pady=5, sticky="w")
            entry = PlaceholderEntry(root, placeholder="1-20 recommended", textvariable=self.start_stat_vars[i], justify="left")
            entry.grid(row=i+5, column=4, padx=(150, 0), pady=5)
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

        # load in the abilities from res/dep/abilities.json
        ABILITIES = {}
        with open('./dep/abilities.json', 'r') as f:
            ABILITIES = json.load(f)

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
        PASSIVES = {}
        with open('./dep/passives.json', 'r') as f:
            PASSIVES = json.load(f)
            PASSIVES = dict(sorted(PASSIVES.items()))
        
        for i in range(6):
            row = i // 2 + 1
            col = i % 2 + 4

            if col == 5:
                ttk.Label(root, text=f"Passive #{i+1}", anchor="w").grid(row=row, column=col, padx=(150, 0), pady=5, sticky="w")
            else:
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

            passive_dropdown.bind("<<ComboboxSelected>>", lambda _, ad=passive_dropdown: ad.selection_clear())
            passive_dropdown.bind("<FocusOut>", lambda _, ad=passive_dropdown: ad.selection_clear())

        # Create a canvas for vertical lines
        canvas = tk.Canvas(root, width=3, bg="black")
        canvas.grid(row=14, column=4, rowspan=10, sticky='ns', padx=(250, 0))

        # Create a button to load the drawPreview
        preview_button = ttk.Button(root, text="Refresh Preview", command=self.drawPreview)
        preview_button.grid(row=14, column=5, pady=(5, 5), padx=(0, 0))

        # Previous Level Button
        prev_button = ttk.Button(root, text="Previous Level", command=self.prev_level)
        prev_button.grid(row=14, column=5, pady=(5, 5), padx=(300, 0))

        # Next Level Button
        next_button = ttk.Button(root, text="Next Level", command=self.next_level)
        next_button.grid(row=14, column=5, pady=(5, 5), padx=(550, 0))

    def prev_level(self):
        if self.current_level > 1:
            self.current_level -= 1
            # Calculate the stats for the given level
            self.current_health -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('HP').get())]['every_level']['HP'])
            ## for every 5th level add the every_5th_level value
            if (self.current_level+1) % 5 == 0:
                self.current_health -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('HP').get())]['every_5th_level']['HP'])
            self.current_speed -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('Speed').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_speed -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('Speed').get())]['every_5th_level']['Secondary'])

            self.current_phys_atk -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_ATK').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_phys_atk -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_ATK').get())]['every_5th_level']['Secondary'])

            self.current_phys_def -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_DEF').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_phys_def -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_DEF').get())]['every_5th_level']['Secondary'])
            self.current_pir_atk -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_ATK').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_pir_atk -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_ATK').get())]['every_5th_level']['Secondary'])
            self.current_pir_def -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_DEF').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_pir_def -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_DEF').get())]['every_5th_level']['Secondary'])
            self.current_mag_atk -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_ATK').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_mag_atk -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_ATK').get())]['every_5th_level']['Secondary'])
            self.current_mag_def -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_DEF').get())]['every_level']['Secondary'])
            if (self.current_level+1) % 5 == 0:
                self.current_mag_def -= int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_DEF').get())]['every_5th_level']['Secondary'])
        self.drawPreview()

    def next_level(self):
        if self.current_level < 40:
            '''
                              if stat == 'HP':
                        increase_per_level = expertise_progression[expertise_level]['every_level']['HP']
                        increase_every_5th_level = expertise_progression[expertise_level]['every_5th_level']['HP']
                        '''
            self.current_level += 1
            self.current_health += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('HP').get())]['every_level']['HP'])
            ## for every 5th level add the every_5th_level value
            if self.current_level % 5 == 0:
                self.current_health += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('HP').get())]['every_5th_level']['HP'])
            self.current_speed += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('Speed').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_speed += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('Speed').get())]['every_5th_level']['Secondary'])
            self.current_phys_atk += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_ATK').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_phys_atk += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_ATK').get())]['every_5th_level']['Secondary'])
            self.current_phys_def += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_DEF').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_phys_def += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PHYS_DEF').get())]['every_5th_level']['Secondary'])
            self.current_pir_atk += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_ATK').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_pir_atk += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_ATK').get())]['every_5th_level']['Secondary'])
            self.current_pir_def += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_DEF').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_pir_def += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('PIR_DEF').get())]['every_5th_level']['Secondary'])
            self.current_mag_atk += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_ATK').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_mag_atk += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_ATK').get())]['every_5th_level']['Secondary'])
            self.current_mag_def += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_DEF').get())]['every_level']['Secondary'])
            if self.current_level % 5 == 0:
                self.current_mag_def += int(expertise_progression[map_slider_to_expertise(self.expertise_vars.get('MAG_DEF').get())]['every_5th_level']['Secondary'])
        self.drawPreview()

    # Function to clear values
    def clear_values(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all values?"):
            self.name_entry.delete(0, tk.END)  # Clear the character name entry
            self.species_var.set("")  # Reset species selection
            self.rarity_var.set(0)  # Reset rarity slider to default
            for var in self.expertise_vars.values():
                var.set(2)  # Reset expertise sliders to 'MEDIUM'
            for var in self.start_stat_vars: # Clear starting stat entries
                var.set("")  
            for var in self.passive_vars: #Clear passive dropdowns
                var.set("")
            for var in self.ability_vars: # Clear ability dropdowns
                var.set("")
            self.modified = False

    def drawPreview(self):
        # Load and resize the main image
        image = Image.open("./res/img/CardBackground.png")  # Ensure the correct file extension is used
        image = image.convert("RGBA")  # Convert the image to RGBA mode to support transparency
        image = image.resize((600, 300), Image.LANCZOS)  # Better resampling filter

        # Load the smaller image
        smaller_image = Image.open("./res/img/Ian_Full_Body.png")  # Load the image again
        smaller_image = smaller_image.convert("RGBA")  # Convert to RGBA mode to support transparency
        smaller_image = smaller_image.resize((133, 216), Image.LANCZOS)  # Resize to a smaller image

        # Paste the smaller image onto the main image at a specific position, using its alpha channel
        paste_position = (28, 31)  # Coordinates where you want to paste the smaller image
        image.paste(smaller_image, paste_position, smaller_image)  # Use the third argument to include transparency

        # Create a draw object to modify the main image
        drawRarity = ImageDraw.Draw(image)
        # Optional: Load a custom font (if available) or use default
        # font = ImageFont.truetype("./res/fonts/your_font.ttf", 30)
        font = ImageFont.load_default()  # Use the default font
        # Define the position and text
        text = str(self.map_slider_to_rarity(self.rarity_var.get()))  # Get the rarity from the slider
        rarity_length = len(text)
        text_position = (90-math.ceil(rarity_length*2.5), 30)  # Top-left corner of the image
        # Draw the text on the main image
        if text == "Common":
            text_color = (255, 255, 255)
        if text == "Uncommon":
            text_color = (0, 255, 0)
        if text == "Rare":
            text_color = (0, 0, 255)
        if text == "Epic":
            text_color = (255, 0, 255)
        if text == "Legendary":
            text_color = (255, 215, 0)
        drawRarity.text(text_position, text, fill=text_color, font=font)
        del drawRarity

        drawName = ImageDraw.Draw(image)
        name = self.name_entry.get()
        name_length = len(name)
        name_position = (75-math.floor(name_length*1.3), 252)
        name_color = (255, 255, 255)
        drawName.text(name_position, name, fill=name_color, font=font, align="center")
        del drawName

        drawSpecies = ImageDraw.Draw(image)
        species = self.species_var.get()
        species_length = len(species)
        species_position = (92-math.floor(species_length*2.5), 235)
        species_color = (255, 255, 255)
        drawSpecies.text(species_position, species, fill=species_color, font=font, align="center")
        del drawSpecies

        drawLevel = ImageDraw.Draw(image)
        level = "LVL: " + str(self.current_level)
        level_position = (180, 38)
        level_color = (255, 255, 255)
        drawLevel.text(level_position, level, fill=level_color, font=font, align="center")
        del drawLevel

        drawHP = ImageDraw.Draw(image)
        hp = "HP : "
        hp += str(self.current_health)
        hp_position = (180, 60)
        hp_color = (255, 255, 255)
        drawHP.text(hp_position, hp, fill=hp_color, font=font, align="center")
        del drawHP

        drawSpeed = ImageDraw.Draw(image)
        speed = "SPD : "
        speed += str(self.current_speed)
        speed_position = (180, 80)
        speed_color = (255, 255, 255)
        drawSpeed.text(speed_position, speed, fill=speed_color, font=font, align="center")
        del drawSpeed

        drawPhysAtk = ImageDraw.Draw(image)
        physAtk = "PHYS ATK : "
        physAtk += str(self.current_phys_atk)
        physAtk_position = (180, 100)
        physAtk_color = (255, 255, 255)
        drawPhysAtk.text(physAtk_position, physAtk, fill=physAtk_color, font=font, align="center")
        del drawPhysAtk

        drawPirAtk = ImageDraw.Draw(image)
        pirAtk = "PIR ATK : "
        pirAtk += str(self.current_pir_atk)
        pirAtk_position = (180, 120)
        pirAtk_color = (255, 255, 255)
        drawPirAtk.text(pirAtk_position, pirAtk, fill=pirAtk_color, font=font, align="center")
        del drawPirAtk

        drawMagAtk = ImageDraw.Draw(image)
        magAtk = "MAG ATK : "
        magAtk += str(self.current_mag_atk)
        magAtk_position = (180, 140)
        magAtk_color = (255, 255, 255)
        drawMagAtk.text(magAtk_position, magAtk, fill=magAtk_color, font=font, align="center")
        del drawMagAtk

        drawPhysDef = ImageDraw.Draw(image)
        physDef = "PHYS DEF : "
        physDef += str(self.current_phys_def)
        physDef_position = (180, 160)
        physDef_color = (255, 255, 255)
        drawPhysDef.text(physDef_position, physDef, fill=physDef_color, font=font, align="center")
        del drawPhysDef

        drawPirDef = ImageDraw.Draw(image)
        pirDef = "PIR DEF : "
        pirDef += str(self.current_pir_def)
        pirDef_position = (180, 180)
        pirDef_color = (255, 255, 255)
        drawPirDef.text(pirDef_position, pirDef, fill=pirDef_color, font=font, align="center")
        del drawPirDef

        drawMagDef = ImageDraw.Draw(image)
        magDef = "MAG DEF : "
        magDef += str(self.current_mag_def)
        magDef_position = (180, 200)
        magDef_color = (255, 255, 255)
        drawMagDef.text(magDef_position, magDef, fill=magDef_color, font=font, align="center")
        del drawMagDef

        drawHPExpertise = ImageDraw.Draw(image)
        hpExpertise = "HP EXPERTISE : "
        hpExpertise += self.map_slider_to_expertise(self.expertise_vars['HP'].get())
        hpExpertise_position = (300, 60)
        hpExpertise_color = (255, 255, 255)
        drawHPExpertise.text(hpExpertise_position, hpExpertise, fill=hpExpertise_color, font=font, align="center")
        del drawHPExpertise

        drawSpeedExpertise = ImageDraw.Draw(image)
        speedExpertise = "SPD EXPERTISE : "
        speedExpertise += self.map_slider_to_expertise(self.expertise_vars['Speed'].get())
        speedExpertise_position = (300, 80)
        speedExpertise_color = (255, 255, 255)
        drawSpeedExpertise.text(speedExpertise_position, speedExpertise, fill=speedExpertise_color, font=font, align="center")
        del drawSpeedExpertise

        drawPhysAtkExpertise = ImageDraw.Draw(image)
        physAtkExpertise = "PHYS ATK EXPERTISE : "
        physAtkExpertise += self.map_slider_to_expertise(self.expertise_vars['PHYS_ATK'].get())
        physAtkExpertise_position = (300, 100)
        physAtkExpertise_color = (255, 255, 255)
        drawPhysAtkExpertise.text(physAtkExpertise_position, physAtkExpertise, fill=physAtkExpertise_color, font=font, align="center")
        del drawPhysAtkExpertise

        drawPirAtkExpertise = ImageDraw.Draw(image)
        pirAtkExpertise = "PIR ATK EXPERTISE : "
        pirAtkExpertise += self.map_slider_to_expertise(self.expertise_vars['PIR_ATK'].get())
        pirAtkExpertise_position = (300, 120)
        pirAtkExpertise_color = (255, 255, 255)
        drawPirAtkExpertise.text(pirAtkExpertise_position, pirAtkExpertise, fill=pirAtkExpertise_color, font=font, align="center")
        del drawPirAtkExpertise

        drawMagAtkExpertise = ImageDraw.Draw(image)
        magAtkExpertise = "MAG ATK EXPERTISE : "
        magAtkExpertise += self.map_slider_to_expertise(self.expertise_vars['MAG_ATK'].get())
        magAtkExpertise_position = (300, 140)
        magAtkExpertise_color = (255, 255, 255)
        drawMagAtkExpertise.text(magAtkExpertise_position, magAtkExpertise, fill=magAtkExpertise_color, font=font, align="center")
        del drawMagAtkExpertise

        drawPhysDefExpertise = ImageDraw.Draw(image)
        physDefExpertise = "PHYS DEF EXPERTISE : "
        physDefExpertise += self.map_slider_to_expertise(self.expertise_vars['PHYS_DEF'].get())
        physDefExpertise_position = (300, 160)
        physDefExpertise_color = (255, 255, 255)
        drawPhysDefExpertise.text(physDefExpertise_position, physDefExpertise, fill=physDefExpertise_color, font=font, align="center")
        del drawPhysDefExpertise

        drawPirDefExpertise = ImageDraw.Draw(image)
        pirDefExpertise = "PIR DEF EXPERTISE : "
        pirDefExpertise += self.map_slider_to_expertise(self.expertise_vars['PIR_DEF'].get())
        pirDefExpertise_position = (300, 180)
        pirDefExpertise_color = (255, 255, 255)
        drawPirDefExpertise.text(pirDefExpertise_position, pirDefExpertise, fill=pirDefExpertise_color, font=font, align="center")
        del drawPirDefExpertise

        drawMagDefExpertise = ImageDraw.Draw(image)
        magDefExpertise = "MAG DEF EXPERTISE : "
        magDefExpertise += self.map_slider_to_expertise(self.expertise_vars['MAG_DEF'].get())
        magDefExpertise_position = (300, 200)
        magDefExpertise_color = (255, 255, 255)
        drawMagDefExpertise.text(magDefExpertise_position, magDefExpertise, fill=magDefExpertise_color, font=font, align="center")
        del drawMagDefExpertise




        # Convert the modified image to a Tkinter-compatible PhotoImage object
        self.photo = ImageTk.PhotoImage(image)  # Store a reference to the image

        # save image
        #image.save("./res/img/FullCard.png")

        # Create a label to display the image
        image_label = ttk.Label(self.root, image=self.photo)  # Use the stored reference
        image_label.grid(row=14, column=5, rowspan=10, padx=(20, 0), pady=20)