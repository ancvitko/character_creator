import os
import json
import tkinter as tk
from creator_character.character_ui import CharacterCreatorUI
from creator_spell.ability_ui import AbilityUI
import tkinter.ttk as ttk
import sv_ttk
from res.dep.abilities import ABILITIES  # Import your existing ABILITIES dictionary from Python file
from res.dep.passives import PASSIVES  # Import your existing PASSIVES dictionary from Python file

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.setup_directories()  # Ensure directories exist
        self.create_abilities_json()  # Create abilities.json if it doesn't exist
        self.create_passives_json()  # Create passives.json if it doesn't exist
        self.setup_main_menu()

    def setup_directories(self):
        """Creates the required directories if they don't exist."""
        required_directories = [
            "./characters",
            "./res/dep"
        ]
        for directory in required_directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def create_abilities_json(self):
        """Creates abilities.json from ABILITIES Python dictionary if it doesn't exist."""
        abilities_file = './res/dep/abilities.json'
        
        # Check if the abilities.json file already exists
        if not os.path.exists(abilities_file):
            with open(abilities_file, 'w') as f:
                json.dump(ABILITIES, f, indent=4)  # Write ABILITIES to the JSON file
                print(f"abilities.json created at {abilities_file}")
        else:
            print(f"abilities.json already exists at {abilities_file}")

    def create_passives_json(self):
        """Creates passives.json from PASSIVES Python dictionary if it doesn't exist."""
        passives_file = './res/dep/passives.json'
        
        # Check if the passives.json file already exists
        if not os.path.exists(passives_file):
            with open(passives_file, 'w') as f:
                json.dump(PASSIVES, f, indent=4)  # Write PASSIVES to the JSON file
                print(f"passives.json created at {passives_file}")
        else:
            print(f"passives.json already exists at {passives_file}")

    def setup_main_menu(self):
        """Sets up the main menu UI."""
        for widget in self.root.winfo_children():
            widget.destroy()

        root.title("Project Shardfall Suite")
        open_character_creator_button = ttk.Button(self.root, text="Character Creator", command=self.open_character_creator, width=20)
        open_ability_creator_button = ttk.Button(self.root, text="Ability Creator", command=self.open_ability_creator, width=20)
        open_character_creator_button.pack(pady=(300, 0))
        open_ability_creator_button.pack(pady=10)

    def open_character_creator(self):
        """Opens the Character Creator UI."""
        for widget in self.root.winfo_children():
            widget.destroy()
        character_creator = CharacterCreatorUI(self.root, self.setup_main_menu)
        root.title("Project Shardfall Character Creator")

    def open_ability_creator(self):
        """Opens the Ability Creator UI."""
        for widget in self.root.winfo_children():
            widget.destroy()
        ability_creator = AbilityUI(self.root, self.setup_main_menu)
        root.title("Project Shardfall Ability Creator")


if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    sv_ttk.set_theme("dark")
    root.state('zoomed')
    root.resizable(True, True)
    main_menu = MainMenu(root)
    root.mainloop()
