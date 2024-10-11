import tkinter as tk
import tkinter.ttk as ttk

class AbilityUI:
    def __init__(self, root, back_to_menu):
        self.root = root
        self.back_to_menu = back_to_menu  # Store the callback function to return to the main menu
        self.ability_effects = []

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
        ability_description_entry.configure(width=50)

        self.ability_effects = ["DAM_PHYS_ATK_1_ENEMY", "DAM_PIR_ATK_1_ENEMY", "DAM_MAG_ATK_1_ENEMY", "HEAL_1_ALLY", "NONE",
                                "DEBUFF_DEF_ALL_1_ENEMY", "BUFF_ATK_ALL_SELF", "BUFF_DEF_ALL_SELF", "BUFF_ATK_MAG_SELF",
                                "BUFF_ATK_PIR_SELF", "BUFF_ATK_PHYS_SELF", "BUFF_DEF_MAG_SELF", "BUFF_DEF_PIR_SELF",
                                "BUFF_DEF_PHYS_SELF", "BUFF_ATK_MAG_ALLY", "BUFF_ATK_PIR_ALLY", "BUFF_ATK_PHYS_ALLY",
                                "BUFF_DEF_MAG_ALLY", "BUFF_DEF_PIR_ALLY", "BUFF_DEF_PHYS_ALLY", "DEBUFF_ATK_ALL_ENEMY",
                                "DEBUFF_DEF_ALL_ALL_ENEMY", "DEBUFF_ATK_MAG_ENEMY", "DEBUFF_ATK_PIR_ENEMY", "DEBUFF_ATK_PHYS_ENEMY",
                                "DEBUFF_DEF_MAG_ENEMY", "DEBUFF_DEF_PIR_ENEMY", "DEBUFF_DEF_PHYS_ENEMY", "BUFF_ATK_MAG_ALL",
                                "BUFF_ATK_PIR_ALL", "BUFF_ATK_PHYS_ALL", "BUFF_DEF_MAG_ALL", "BUFF_DEF_PIR_ALL", "BUFF_DEF_PHYS_ALL",
                                "DEBUFF_ATK_ALL_ALLY", "DEBUFF_DEF_ALL_ALLY", "DEBUFF_ATK_MAG_AdLLY", "DEBUFF_ATK_PIR_ALLY",
                                "HEAL_2_ALLY", "HEAL_ALL_ALLY"
                                ]
        # Sort the ability effects, but make sure "NONE" is at the start
        self.ability_effects.sort(key=lambda x: x if x != "NONE" else " ")

        # Set the default values for the ability name and description
        ability_name_entry.insert(0, "Basic Attack")
        ability_description_entry.insert(0, "A basic attack that deals damage to a single target.")

        # Create a label for the ability effects
        ability_effects_label = ttk.Label(root, text="Ability Effects:")
        ability_effects_label.grid(row=4, column=0, padx=(10, 0), pady=20, sticky="w")

        # Create labels and entries for each effect and value
        effect_1_label = ttk.Label(root, text="Effect 1:")
        effect_1_label.grid(row=5, column=0, padx=(10, 0), pady=10, sticky="w")
        effect_1_dropdown = ttk.Combobox(root, values=self.ability_effects, state="readonly")
        effect_1_dropdown.grid(row=5, column=1, padx=(10, 0), pady=10, sticky="w")
        effect_1_dropdown.bind("<<ComboboxSelected>>", lambda _: effect_1_dropdown.selection_clear())
        # Bind focus out event to reset selection
        effect_1_dropdown.bind("<FocusOut>", lambda _: effect_1_dropdown.selection_clear())
        

        value_1_label = ttk.Label(root, text="Value 1:")
        value_1_label.grid(row=6, column=0, padx=(10, 0), pady=10, sticky="w")
        value_1_entry = ttk.Entry(root)
        value_1_entry.grid(row=6, column=1, padx=(10, 0), pady=10, sticky="w")
        

        effect_2_label = ttk.Label(root, text="Effect 2:")
        effect_2_label.grid(row=7, column=0, padx=(10, 0), pady=10, sticky="w")
        effect_2_dropdown = ttk.Combobox(root, values=self.ability_effects, state="readonly")
        effect_2_dropdown.grid(row=7, column=1, padx=(10, 0), pady=10, sticky="w")
        effect_2_dropdown.bind("<<ComboboxSelected>>", lambda _: effect_2_dropdown.selection_clear())
        # Bind focus out event to reset selection
        effect_2_dropdown.bind("<FocusOut>", lambda _: effect_2_dropdown.selection_clear())

        value_2_label = ttk.Label(root, text="Value 2:")
        value_2_label.grid(row=8, column=0, padx=(10, 0), pady=10, sticky="w")
        value_2_entry = ttk.Entry(root)
        value_2_entry.grid(row=8, column=1, padx=(10, 0), pady=10, sticky="w")
        value_2_entry.insert(0, "0")

        effect_3_label = ttk.Label(root, text="Effect 3:")
        effect_3_label.grid(row=9, column=0, padx=(10, 0), pady=10, sticky="w")
        effect_3_dropdown = ttk.Combobox(root, values=self.ability_effects, state="readonly")
        effect_3_dropdown.grid(row=9, column=1, padx=(10, 0), pady=10, sticky="w")
        effect_3_dropdown.bind("<<ComboboxSelected>>", lambda _: effect_3_dropdown.selection_clear())
        # Bind focus out event to reset selection
        effect_3_dropdown.bind("<FocusOut>", lambda _: effect_3_dropdown.selection_clear())
    

        value_3_label = ttk.Label(root, text="Value 3:")
        value_3_label.grid(row=10, column=0, padx=(10, 0), pady=10, sticky="w")
        value_3_entry = ttk.Entry(root)
        value_3_entry.grid(row=10, column=1, padx=(10, 0), pady=10, sticky="w")
        value_3_entry.insert(0, "0")

        effect_4_label = ttk.Label(root, text="Effect 4:")
        effect_4_label.grid(row=11, column=0, padx=(10, 0), pady=10, sticky="w")
        effect_4_dropdown = ttk.Combobox(root, values=self.ability_effects, state="readonly")
        effect_4_dropdown.grid(row=11, column=1, padx=(10, 0), pady=10, sticky="w")
        effect_4_dropdown.bind("<<ComboboxSelected>>", lambda _: effect_4_dropdown.selection_clear())
        # Bind focus out event to reset selection
        effect_4_dropdown.bind("<FocusOut>", lambda _: effect_4_dropdown.selection_clear())


        value_4_label = ttk.Label(root, text="Value 4:")
        value_4_label.grid(row=12, column=0, padx=(10, 0), pady=10, sticky="w")
        value_4_entry = ttk.Entry(root)
        value_4_entry.grid(row=12, column=1, padx=(10, 0), pady=10, sticky="w")
        value_4_entry.insert(0, "0")

        effect_5_label = ttk.Label(root, text="Effect 5:")
        effect_5_label.grid(row=13, column=0, padx=(10, 0), pady=10, sticky="w")
        effect_5_dropdown = ttk.Combobox(root, values=self.ability_effects, state="readonly")
        effect_5_dropdown.grid(row=13, column=1, padx=(10, 0), pady=10, sticky="w")
        effect_5_dropdown.bind("<<ComboboxSelected>>", lambda _: effect_5_dropdown.selection_clear())
        # Bind focus out event to reset selection
        effect_5_dropdown.bind("<FocusOut>", lambda _: effect_5_dropdown.selection_clear())

        value_5_label = ttk.Label(root, text="Value 5:")
        value_5_label.grid(row=14, column=0, padx=(10, 0), pady=10, sticky="w")
        value_5_entry = ttk.Entry(root)
        value_5_entry.grid(row=14, column=1, padx=(10, 0), pady=10, sticky="w")
        value_5_entry.insert(0, "0")

        effect_6_label = ttk.Label(root, text="Effect 6:")
        effect_6_label.grid(row=15, column=0, padx=(10, 0), pady=10, sticky="w")
        effect_6_dropdown = ttk.Combobox(root, values=self.ability_effects, state="readonly")
        effect_6_dropdown.grid(row=15, column=1, padx=(10, 0), pady=10, sticky="w")
        effect_6_dropdown.bind("<<ComboboxSelected>>", lambda _: effect_6_dropdown.selection_clear())
        # Bind focus out event to reset selection
        effect_6_dropdown.bind("<FocusOut>", lambda _: effect_6_dropdown.selection_clear())

        value_6_label = ttk.Label(root, text="Value 6:")
        value_6_label.grid(row=16, column=0, padx=(10, 0), pady=10, sticky="w")
        value_6_entry = ttk.Entry(root)
        value_6_entry.grid(row=16, column=1, padx=(10, 0), pady=10, sticky="w")
        value_6_entry.insert(0, "0")

        cooldown_label = ttk.Label(root, text="Cooldown:")
        cooldown_label.grid(row=17, column=0, padx=(10, 0), pady=10, sticky="w")
        cooldown_entry = ttk.Entry(root)
        cooldown_entry.grid(row=17, column=1, padx=(10, 0), pady=10, sticky="w")
        cooldown_entry.insert(0, "0")
