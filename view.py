import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    """
    doc
    """

    PADDING = 10
    MENU_PADDING = 5
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 500
    GRIP_THICKNESS = 20
    SCALE = 1000

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

    def update_view(self):
        block_coords = self.find_block_coords()
        self.canvas.coords(self.block, block_coords[0], block_coords[1], block_coords[2], block_coords[3])
        lg_coords = self.find_lg_coords()
        self.canvas.coords(self.left_grip, lg_coords[0], lg_coords[1], lg_coords[2], lg_coords[3])
        rg_coords = self.find_rg_coords()
        self.canvas.coords(self.right_grip, rg_coords[0], rg_coords[1], rg_coords[2], rg_coords[3])
        self.update()

    def find_block_coords(self):
        return ((self.CANVAS_WIDTH - self.model.width * self.SCALE) / 2,
                self.CANVAS_HEIGHT - self.model.block.x * self.SCALE,
                (self.CANVAS_WIDTH + self.model.width * self.SCALE) / 2,
                self.CANVAS_HEIGHT - (self.model.length + self.model.block.x) * self.SCALE)

    def find_lg_coords(self):
        return ((self.CANVAS_WIDTH - self.model.grip_sep * self.SCALE) / 2 - self.GRIP_THICKNESS,
                self.CANVAS_HEIGHT - self.model.grip.x * self.SCALE,
                (self.CANVAS_WIDTH - self.model.grip_sep * self.SCALE) / 2,
                self.CANVAS_HEIGHT - (self.model.GRIPPER_WIDTH + self.model.grip.x) * self.SCALE)

    def find_rg_coords(self):
        return ((self.CANVAS_WIDTH + self.model.grip_sep * self.SCALE) / 2,
                self.CANVAS_HEIGHT - self.model.grip.x * self.SCALE,
                (self.CANVAS_WIDTH + self.model.grip_sep * self.SCALE) / 2 + self.GRIP_THICKNESS,
                self.CANVAS_HEIGHT - (self.model.GRIPPER_WIDTH + self.model.grip.x) * self.SCALE)

    def initiate_objects(self):
        block_coords = self.find_block_coords()
        block = self.canvas.create_rectangle(block_coords[0], block_coords[1],
                                             block_coords[2], block_coords[3])
        lg_coords = self.find_lg_coords()
        left_grip = self.canvas.create_rectangle(lg_coords[0], lg_coords[1],
                                                 lg_coords[2], lg_coords[3])
        rg_coords = self.find_rg_coords()
        right_grip = self.canvas.create_rectangle(rg_coords[0], rg_coords[1],
                                                  rg_coords[2], rg_coords[3])
        return block, left_grip, right_grip

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





