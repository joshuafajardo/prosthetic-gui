import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    """
    doc
    """

    PADDING = 10
    MENU_PADDING = 5
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 800
    GRIP_THICKNESS = 10
    SCALE = 1

    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model = model
        self.title("Prosthetic Gui")
        self.menu = self.make_menu_frame()
        self.sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.main_frame, self.canvas = self.make_main_frame()
        self.block, self.left_grip, self.right_grip = self.initiate_objects()
        self.menu.grid(row=1, column=1, padx=self.PADDING, pady=self.PADDING)
        self.sep.grid(row=2, column=1, sticky="ew")
        self.main_frame.grid(row=3, column=1, padx=self.PADDING, pady=self.PADDING)

    def initiate_objects(self):
        block_bottom_corner = ((self.CANVAS_WIDTH - self.model.width * self.SCALE) / 2, 0)
        block_top_corner = ((self.CANVAS_WIDTH + self.model.width * self.SCALE) / 2, 0)
        block = self.canvas.create_rectangle(block_bottom_corner[0], block_bottom_corner[1],
                                             block_top_corner[0], block_top_corner[1])

        lg_bottom_corner = ((self.CANVAS_WIDTH - self.model.grip_sep * self.SCALE) / 2 - self.GRIP_THICKNESS, 0)
        lg_top_corner = ((self.CANVAS_WIDTH - self.model.grip_sep * self.SCALE) / 2,
                         self.model.GRIPPER_WIDTH * self.SCALE)
        left_grip = self.canvas.create_rectangle(lg_bottom_corner[0], lg_bottom_corner[1],
                                                 lg_top_corner[0], lg_top_corner[1])

        rg_bottom_corner = ((self.CANVAS_WIDTH + self.model.grip_sep * self.SCALE) / 2, 0)
        rg_top_corner = ((self.CANVAS_WIDTH + self.model.grip_sep * self.SCALE) / 2 + self.GRIP_THICKNESS,
                         self.model.GRIPPER_WIDTH * self.SCALE)
        right_grip = self.canvas.create_rectangle(rg_bottom_corner[0], rg_bottom_corner[1],
                                                  rg_top_corner[0], rg_top_corner[1])

        return block, left_grip, right_grip

    def main(self):
        self.mainloop()

    def make_menu_frame(self):
        menu = ttk.Frame(self)
        prev_button = ttk.Button(menu, text="Previous Setting", command=self.controller.prev_setting)
        next_button = ttk.Button(menu, text="Next Setting", command=self.controller.next_setting)
        prev_button.pack()
        next_button.pack()
        return menu

    def make_main_frame(self):
        main_frame = ttk.Frame(self)
        canvas = tk.Canvas(main_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        canvas.pack()
        return main_frame, canvas





