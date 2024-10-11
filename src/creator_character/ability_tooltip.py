import tkinter as tk

class Tooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tooltip_window = None

        # Bind events to show and hide the tooltip
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.update_tooltip)

        # Store the descriptions for tooltip display
        self.ability_descriptions = {}

    def set_descriptions(self, descriptions):
        """
        Set the descriptions for the abilities to be displayed in the tooltip.
        """
        self.ability_descriptions = descriptions

    def calculate_tooltip_position(self):
        """
        Calculate the position of the tooltip relative to the widget.
        """
        x = self.widget.winfo_rootx() + 175
        y = self.widget.winfo_rooty() - self.tooltip_window.winfo_reqheight() + 65
        return x, y

    def show_tooltip(self, event=None):
        """
        Create and show the tooltip when the mouse enters the widget.
        """
        if self.tooltip_window is None:
            self.tooltip_window = tk.Toplevel(self.widget)
            self.tooltip_window.wm_overrideredirect(True)  # No window decorations
            self.tooltip_label = tk.Label(self.tooltip_window, text="", background="black",
                                          foreground="white", borderwidth=1, relief="solid", justify="left")
            self.tooltip_label.pack()

        x, y = self.calculate_tooltip_position()
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.deiconify()  # Show window if hidden

    def hide_tooltip(self, event=None):
        """
        Hide the tooltip when the mouse leaves the widget.
        """
        if self.tooltip_window is not None:
            self.tooltip_window.withdraw()

    def update_tooltip(self, event=None):
        """
        Update the tooltip text based on the widget's value.
        """
        if self.tooltip_window is not None:
            x, y = self.calculate_tooltip_position()
            self.tooltip_window.wm_geometry(f"+{x}+{y}")  # Reposition dynamically

        current_value = self.widget.get() or ""
        if current_value in self.ability_descriptions:
            description = self.ability_descriptions[current_value]['description']
            tooltip_text = f"{description}\nEffect#1: {self.ability_descriptions[current_value]['effect_1']}\nValue#1: {self.ability_descriptions[current_value]['value_1']}"
            cooldown = self.ability_descriptions[current_value]['cooldown']

            if self.ability_descriptions[current_value]['effect_2'] != 'NONE':
                tooltip_text += f"\nEffect#2: {self.ability_descriptions[current_value]['effect_2']}\nValue#2: {self.ability_descriptions[current_value]['value_2']}"

            if self.ability_descriptions[current_value]['effect_3'] != 'NONE':
                tooltip_text += f"\nEffect#3: {self.ability_descriptions[current_value]['effect_3']}\nValue#3: {self.ability_descriptions[current_value]['value_3']}"

            if self.ability_descriptions[current_value]['effect_4'] != 'NONE':
                tooltip_text += f"\nEffect#4: {self.ability_descriptions[current_value]['effect_4']}\nValue#4: {self.ability_descriptions[current_value]['value_4']}"

            if self.ability_descriptions[current_value]['effect_5'] != 'NONE':
                tooltip_text += f"\nEffect#5: {self.ability_descriptions[current_value]['effect_5']}\nValue#5: {self.ability_descriptions[current_value]['value_5']}"

            if self.ability_descriptions[current_value]['effect_6'] != 'NONE':
                tooltip_text += f"\nEffect#6: {self.ability_descriptions[current_value]['effect_6']}\nValue#6: {self.ability_descriptions[current_value]['value_6']}"

            tooltip_text += f"\nCooldown: {cooldown} turn(s)"
            self.tooltip_label.config(text=tooltip_text)
        else:
            self.tooltip_label.config(text="")  # Clear if not found
