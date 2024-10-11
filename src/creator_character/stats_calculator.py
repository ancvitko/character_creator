# stats_calculator.py

import json
import os
import math
from tkinter import messagebox
from creator_character.utils import map_slider_to_rarity, map_slider_to_expertise


# Expertise progression dictionary
expertise_progression = {
    'VERY_LOW': {'every_level': {'HP': 3, 'Secondary': 2}, 'every_5th_level': {'HP': 5, 'Secondary': 4}},
    'LOW': {'every_level': {'HP': 4, 'Secondary': 3}, 'every_5th_level': {'HP': 6, 'Secondary': 5}},
    'MEDIUM': {'every_level': {'HP': 5, 'Secondary': 4}, 'every_5th_level': {'HP': 7, 'Secondary': 6}},
    'HIGH': {'every_level': {'HP': 6, 'Secondary': 5}, 'every_5th_level': {'HP': 8, 'Secondary': 7}},
    'VERY_HIGH': {'every_level': {'HP': 7, 'Secondary': 6}, 'every_5th_level': {'HP': 9, 'Secondary': 8}}
}

def calculate_and_save(char_name, species, rarity_value, start_stat_vars, expertise_vars, ability_vars, passives_vars):

    if not char_name:
        messagebox.showwarning("Input Error", "Please enter a character name.")
        return
    
    if species is None:
        messagebox.showwarning("Input Error", "Please select a species.")
        return
    
    if passives_vars is None:
        messagebox.showwarning("Input Error", "Please select a passive.")
        return


    # Create the characters directory if it doesn't exist
    dir_path = "characters"
    os.makedirs(dir_path, exist_ok=True)

    # Construct the file path using the character name
    file_path = os.path.join(dir_path, f"{char_name}.txt")

    try:
        # Get starting stats as integers
        starting_stats = {stat: int(var.get()) for stat, var in zip(
            ['HP', 'Speed', 'PHYS_ATK', 'PHYS_DEF', 'PIR_ATK', 'PIR_DEF', 'MAG_ATK', 'MAG_DEF'], start_stat_vars)}

    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid numbers for starting stats (1-20 recommended).")
        return

    # Map rarity value to its string representation
    rarity = map_slider_to_rarity(rarity_value)
    

    # Map expertise integer values back to their string representations
    expertise = {stat: map_slider_to_expertise(var.get()) for stat, var in expertise_vars.items()}
    total_levels = 40  # Adjusted to include level 0 to level 39

    # Save stats for each level in the file
    try:
        with open(file_path, "w") as file:
            file.write(f"Character Name: {char_name}\n")
            file.write(f"Species: {species}\n")
            file.write(f"Rarity: {rarity}\n")
            file.write(f"____________________\n\n")

            # Write the chosen expertise levels
            file.write(f"Expertise Levels:\n")
            for stat, expertise_level in expertise.items():
                file.write(f"\t{stat} Expertise: {expertise_level}\n")
            file.write(f"____________________\n\n")

            for level in range(total_levels):
                final_stats = starting_stats.copy()
                for stat, expertise_level in expertise.items():
                    if stat == 'HP':
                        increase_per_level = expertise_progression[expertise_level]['every_level']['HP']
                        increase_every_5th_level = expertise_progression[expertise_level]['every_5th_level']['HP']
                    else:
                        increase_per_level = expertise_progression[expertise_level]['every_level']['Secondary']
                        increase_every_5th_level = expertise_progression[expertise_level]['every_5th_level']['Secondary']

                    # Calculate increases based on the current level
                    regular_increase = increase_per_level * level
                    special_increase = increase_every_5th_level * ((level + 1) // 5)

                    final_stats[stat] += regular_increase + special_increase

                file.write(f"Level {level + 1} Stats:\n")
                for stat, value in final_stats.items():
                    file.write(f"\t{stat}: {value}\n")
                dodge = round((final_stats['Speed'] * 0.6) / math.sqrt((level + 16))/2, 2)
                phys_crit = round((final_stats['PHYS_ATK'] * 0.3 + final_stats['Speed'] *0.3) / math.sqrt((level + 16)), 2)
                pir_crit = round((final_stats['PIR_ATK'] * 0.3 + final_stats['Speed'] *0.3) / math.sqrt((level + 16)), 2)
                mag_crit = round((final_stats['MAG_ATK'] * 0.3 + final_stats['Speed'] *0.3) / math.sqrt((level + 16)), 2)
                file.write(f"\tDodge: {dodge}%\n")
                file.write(f"\tPhysical Crit: {phys_crit}%\n")
                file.write(f"\tPierce Crit: {pir_crit}%\n")
                file.write(f"\tMagic Crit: {mag_crit}%\n")
                file.write("\n")
                
            # list to array of strings abilityvar
            abilities = [ability.get() for ability in ability_vars]
            # Write the abilities
            abilityLevels = ['LVL 1 #1', 'LVL 1 #2', 'LVL 1 #3', 'LVL 1 #4', 'LVL 3', 'LVL 5', 'LVL 8', 'LVL 10', 'LVL 13', 'LVL 15', 'LVL 18', 'LVL 20', 'LVL 23', 'LVL 25', 'LVL 28', 'LVL 30', 'LVL 33', 'LVL 35', 'LVL 38', 'LVL 40']
            ability_level_keys = ['LVL1_ABILITIES', 'LVL1_ABILITIES', 'LVL1_ABILITIES', 'LVL1_ABILITIES', 'LVL3_ABILITIES', 'LVL5_ABILITIES', 'LVL8_ABILITIES', 'LVL10_ABILITIES', 'LVL13_ABILITIES', 'LVL15_ABILITIES', 'LVL18_ABILITIES', 'LVL20_ABILITIES', 'LVL23_ABILITIES', 'LVL25_ABILITIES', 'LVL28_ABILITIES', 'LVL30_ABILITIES', 'LVL33_ABILITIES', 'LVL35_ABILITIES', 'LVL38_ABILITIES', 'LVL40_ABILITIES']
            file.write(f"____________________\n\n")
            # Load in the json file
            with open('./dep/abilities.json', 'r') as f:
                ABILITIES = json.load(f)
            file.write(f"Abilities:\n")
            for i, ability in enumerate(abilities):
                ability_level_key = ability_level_keys[i]  # Get the corresponding ability level key
                if ability in ABILITIES[ability_level_key]:
                    ability_data = ABILITIES[ability_level_key][ability]
                    file.write(f"{abilityLevels[i]}: {ability}\n")
                    file.write(f"\tDescription: {ability_data['description']}\n")
                    file.write(f"\tValue: {ability_data['value']}\n")
                    file.write(f"\tCooldown: {ability_data['cooldown']}\n\n")
                else:
                    file.write(f"{abilityLevels[i]}: {ability} NONE\n")
            file.write(f"____________________\n\n")
            file.write(f"Passives:\n")
            PASSIVES = {}
            with open('./dep/passives.json', 'r') as f:
                PASSIVES = json.load(f)
                
            passives = [passive.get() for passive in passives_vars]
            for i, passive in enumerate(passives):
                if passive in PASSIVES:
                    file.write(f"Passive #{i}: {passive}\n")
                    file.write(f"\tDescription: {PASSIVES[passive]['description1']}\n")
                    file.write(f"\tValue: {PASSIVES[passive]['value1']}\n\n")
                    file.write(f"\tDescription: {PASSIVES[passive]['description2']}\n")
                    file.write(f"\tValue: {PASSIVES[passive]['value2']}\n\n")
                else:
                    file.write(f"Passive #{i}: NONE\n")
            file.write(f"____________________\n\n")
            
        messagebox.showinfo("Saved", f"Character '{char_name}' stats saved to {file_path}")

        '''
        We return False to flag the UI that nothing is modified and we can return
        without being prompted that we haven't saved the character.
        '''
        return False

    except Exception as e:
        messagebox.showerror("Error", f"Could not save character: {e}")
