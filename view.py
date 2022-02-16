import tkinter as tk
from tkinter import ttk
import time


def start_view(controller, model):
    view = View(controller, model)
    while True:
        view.update_view()
        time.sleep(1/60)


class View(tk.Tk):
    """
    doc
    """
    PADDING = 10
    MENU_PADDING = 5
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 600
    GRIP_THICKNESS = 30
    VERTICAL_SCALE = 1700
    HORIZONTAL_SCALE = 2250

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
        self.background = "#dbdbdb"
        self.update_view()

    def update_view(self):
        block_coords = self.find_block_coords()
        self.canvas.coords(self.block, block_coords[0], block_coords[1], block_coords[2], block_coords[3])
        lg_coords = self.find_lg_coords()
        self.canvas.coords(self.left_grip, lg_coords[0], lg_coords[1], lg_coords[2], lg_coords[3])
        rg_coords = self.find_rg_coords()
        self.canvas.coords(self.right_grip, rg_coords[0], rg_coords[1], rg_coords[2], rg_coords[3])
        if self.model.broken:
            self.canvas.itemconfig(self.block, fill="red")
        else:
            self.canvas.itemconfig(self.block, fill="#F9D23D")
        self.update()

    def find_block_coords(self):
        if self.grip.x + self.GRIPPER_WIDTH > self.block.x \
           and self.grip.x < self.block.x + self.length \
           and self.grip_sep < self.width: #in contact
            return ((self.CANVAS_WIDTH - self.model.grip_sep * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - self.model.block.x * self.VERTICAL_SCALE,
                    (self.CANVAS_WIDTH + self.model.grip_sep * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - (self.model.length + self.model.block.x) * self.VERTICAL_SCALE)

        else:
            return ((self.CANVAS_WIDTH - self.model.width * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - self.model.block.x * self.VERTICAL_SCALE,
                    (self.CANVAS_WIDTH + self.model.width * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - (self.model.length + self.model.block.x) * self.VERTICAL_SCALE)

    def find_lg_coords(self):
        # separation = max(self.model.grip_sep, self.model.width)
        return ((self.CANVAS_WIDTH - self.model.grip_sep * self.HORIZONTAL_SCALE) / 2 - self.GRIP_THICKNESS,
                self.CANVAS_HEIGHT - self.model.grip.x * self.VERTICAL_SCALE,
                (self.CANVAS_WIDTH - self.model.grip_sep * self.HORIZONTAL_SCALE) / 2,
                self.CANVAS_HEIGHT - (self.model.GRIPPER_WIDTH + self.model.grip.x) * self.VERTICAL_SCALE)

    def find_rg_coords(self):
        # separation = max(self.model.grip_sep, self.model.width)
        return ((self.CANVAS_WIDTH + self.model.grip_sep * self.HORIZONTAL_SCALE) / 2,
                self.CANVAS_HEIGHT - self.model.grip.x * self.VERTICAL_SCALE,
                (self.CANVAS_WIDTH + self.model.grip_sep * self.HORIZONTAL_SCALE) / 2 + self.GRIP_THICKNESS,
                self.CANVAS_HEIGHT - (self.model.GRIPPER_WIDTH + self.model.grip.x) * self.VERTICAL_SCALE)

    def initiate_objects(self):
        block_coords = self.find_block_coords()
        block = self.canvas.create_rectangle(block_coords[0], block_coords[1],
                                             block_coords[2], block_coords[3], fill="#F9D23D")

        lg_coords = self.find_lg_coords()
        left_grip = self.canvas.create_rectangle(lg_coords[0], lg_coords[1],
                                                 lg_coords[2], lg_coords[3], fill="#D6D6D6")
        rg_coords = self.find_rg_coords()
        right_grip = self.canvas.create_rectangle(rg_coords[0], rg_coords[1],
                                                  rg_coords[2], rg_coords[3], fill="#D6D6D6")

        min_height = self.CANVAS_HEIGHT - self.model.MIN_HEIGHT * self.VERTICAL_SCALE
        min_line = self.canvas.create_line(0, min_height,
                                           self.CANVAS_WIDTH, min_height, dash=(3, 3))

        self.canvas.tag_raise(min_line)
        self.canvas.tag_lower(block)
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
