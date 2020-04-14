import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    """
    doc
    """

    PADDING = 10
    MENU_PADDING = 5

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Prosthetic Gui")
        self._make_menu_frame()
        self.sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self._make_main_frame()
        self.menu.grid(row=1, column=1, padx=self.PADDING, pady=self.PADDING)
        self.sep.grid(row=2, column=1, sticky="ew")
        self.main_frame.grid(row=3, column=1, padx=self.PADDING, pady=self.PADDING)

    def main(self):
        self.mainloop()

    def _make_menu_frame(self):
        self.menu = ttk.Frame(self)
        mass_lbl = ttk.Label(self.menu, text="mass:")
        length_lbl = ttk.Label(self.menu, text="Length:")
        width_lbl = ttk.Label(self.menu, text="Width:")
        friction_lbl = ttk.Label(self.menu, text="Height:")
        mass_ent = ttk.Entry(self.menu, )
        length_ent = ttk.Entry(self.menu)
        width_ent = ttk.Entry(self.menu)
        friction_ent = ttk.Entry(self.menu)
        mass_lbl.grid(    row=1, column=1)
        length_lbl.grid(    row=1, column=3)
        width_lbl.grid(     row=1, column=5)
        friction_lbl.grid(  row=1, column=7)
        mass_ent.grid(    row=1, column=2, padx=self.MENU_PADDING, pady=self.MENU_PADDING)
        length_ent.grid(    row=1, column=4, padx=self.MENU_PADDING, pady=self.MENU_PADDING)
        width_ent.grid(     row=1, column=6, padx=self.MENU_PADDING, pady=self.MENU_PADDING)
        friction_ent.grid(  row=1, column=8, padx=self.MENU_PADDING, pady=self.MENU_PADDING)

    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self)





