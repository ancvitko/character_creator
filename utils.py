# utils.py


import tkinter as tk
from tkinter import ttk

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']

        # Binding events for focus in and focus out
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        """Inserts the placeholder text and sets its color."""
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color  # Set the placeholder color

        # This line is added to ensure that the placeholder appears with the correct color
        self.bind("<Configure>", self.update_placeholder_color)

    def foc_in(self, *args):
        """Clears the placeholder when the entry is focused."""
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self['foreground'] = self.default_fg_color  # Reset to default foreground color

    def foc_out(self, *args):
        """Restores the placeholder if the entry is empty when it loses focus."""
        if not self.get():
            self.put_placeholder()

    def update_placeholder_color(self, event=None):
        """Updates the color of the placeholder when the widget is configured."""
        if self.get() == self.placeholder:
            self['foreground'] = self.placeholder_color


# utils.py
def map_slider_to_rarity(value):
    return value

def map_slider_to_expertise(value):
    mapping = {0: "VERY_LOW", 1: "LOW", 2: "MEDIUM", 3: "HIGH", 4: "VERY_HIGH"}
    return mapping.get(value, "MEDIUM")

