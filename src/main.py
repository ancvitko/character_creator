import tkinter as tk
from character_ui import CharacterCreatorUI
from ability_ui import AbilityUI
import tkinter.ttk as ttk
import sv_ttk

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.setup_main_menu()

    def setup_main_menu(self):
        # Clear any existing widgets (in case we're coming back from the character UI)
        for widget in self.root.winfo_children():
            widget.destroy()

        root.title("Project Shardfall Suite")
        # Create a button that opens the character creation UI
        open_character_creator_button = ttk.Button(self.root, text="Character Creator", command=self.open_character_creator)
        open_ability_creator_button = ttk.Button(self.root, text="Ability Creator", command=self.open_ability_creator)
        open_character_creator_button.pack(pady=50)
        open_ability_creator_button.pack(pady=50)


    def open_character_creator(self):
        # Clear the main menu and show the character creator UI
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize the CharacterCreatorUI
        character_creator = CharacterCreatorUI(self.root, self.setup_main_menu)  # Pass the method to go back to the main menu
        root.title("Project Shardfall Character Creator")

    def open_ability_creator(self):
        # Clear the main menu and show the character creator UI
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize the CharacterCreatorUI
        ability_creator = AbilityUI(self.root, self.setup_main_menu)
        root.title("Project Shardfall Ability Creator")

if __name__ == "__main__":
    root = tk.Tk()
    # Center the window
    root.eval('tk::PlaceWindow . center')
    # Set theme before creating the UI
    sv_ttk.set_theme("dark")  # Set the dark theme here
    # Apply theme to the title bar
    # apply_theme_to_titlebar(root)
    root.state('zoomed')
    root.resizable(True, True)
    main_menu = MainMenu(root)
    root.mainloop()
