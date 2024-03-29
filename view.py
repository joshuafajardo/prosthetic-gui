import tkinter as tk
from tkinter import ttk
import time



def start_view(controller, model):
    view = View(controller, model)
    while True:
        view.update_view()
        time.sleep(1/100)


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
        self.setting_num = tk.IntVar()
        self.menu = self.make_menu_frame()
        self.sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.main_frame, self.canvas = self.make_main_frame()
        self.block, self.left_grip, self.right_grip, self.direction_label = self.initiate_objects()
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
        self.canvas.coords(self.direction_label, (block_coords[0]+block_coords[2])/2,
                           (block_coords[1]+block_coords[3])/2)
        
        if self.controller.trial_state == "grasp":
            direction_text = u"\u2B95\u2B05"
        elif self.controller.trial_state == "lift":
            direction_text = u"\u2B06"
        elif self.controller.trial_state == "hold":
            direction_text = u"\u2015"
        else:   # release
            # direction_text = u"\u2B0C"
            direction_text = "\u2B05\u2B95"

        self.canvas.itemconfig(self.direction_label, text=direction_text)
        if self.model.broken:
            self.canvas.itemconfig(self.block, fill="red")
        else:
            self.canvas.itemconfig(self.block, fill="#F9D23D")
        self.update()
        self.setting_num.set(self.controller.curr_setting+1)

    def find_block_coords(self):
        separation = max(self.model.grip_sep, self.model.width)
        # separation = self.grip_sep
        if self.model.grip.x + self.model.GRIPPER_WIDTH > self.model.block.x \
           and self.model.grip.x < self.model.block.x + self.model.length \
           and self.model.grip_sep < self.model.width: #in contact
            return ((self.CANVAS_WIDTH - separation * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - self.model.block.x * self.VERTICAL_SCALE,
                    (self.CANVAS_WIDTH + separation * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - (self.model.length + self.model.block.x) * self.VERTICAL_SCALE)

        else:
            return ((self.CANVAS_WIDTH - self.model.width * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - self.model.block.x * self.VERTICAL_SCALE,
                    (self.CANVAS_WIDTH + self.model.width * self.HORIZONTAL_SCALE) / 2,
                    self.CANVAS_HEIGHT - (self.model.length + self.model.block.x) * self.VERTICAL_SCALE)

    def find_lg_coords(self):
        separation = max(self.model.grip_sep, self.model.width)
        # separation = self.grip_sep
        return ((self.CANVAS_WIDTH - separation * self.HORIZONTAL_SCALE) / 2 - self.GRIP_THICKNESS,
                self.CANVAS_HEIGHT - self.model.grip.x * self.VERTICAL_SCALE,
                (self.CANVAS_WIDTH - separation * self.HORIZONTAL_SCALE) / 2,
                self.CANVAS_HEIGHT - (self.model.GRIPPER_WIDTH + self.model.grip.x) * self.VERTICAL_SCALE)

    def find_rg_coords(self):
        separation = max(self.model.grip_sep, self.model.width)
        # separation = self.grip_sep
        return ((self.CANVAS_WIDTH + separation * self.HORIZONTAL_SCALE) / 2,
                self.CANVAS_HEIGHT - self.model.grip.x * self.VERTICAL_SCALE,
                (self.CANVAS_WIDTH + separation * self.HORIZONTAL_SCALE) / 2 + self.GRIP_THICKNESS,
                self.CANVAS_HEIGHT - (self.model.GRIPPER_WIDTH + self.model.grip.x) * self.VERTICAL_SCALE)

    def initiate_objects(self):
        block_coords = self.find_block_coords()
        block = self.canvas.create_rectangle(block_coords[0], block_coords[1],
                                             block_coords[2], block_coords[3], fill="#F9D23D")

        direction_label = self.canvas.create_text((block_coords[0]+block_coords[2])/2,
                                                  (block_coords[1]+block_coords[3])/2,
                                                  text=u"\u2B95 \u2B05",
                                                  font=('Helvetica',36),
                                                  anchor=tk.CENTER)

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
        return block, left_grip, right_grip, direction_label

    def make_menu_frame(self):
        menu = ttk.Frame(self)
        prev_button = ttk.Button(menu, text="Previous Setting", command=self.controller.prev_setting)
        prev_button.grid(row=0, column=0, columnspan=2)
        next_button = ttk.Button(menu, text="Next Setting", command=self.controller.next_setting)
        next_button.grid(row=1, column=0,columnspan=2)
        setting_label = ttk.Label(menu, text="Setting: ")
        setting_label.grid(row=2, column=0, columnspan=1)
        settingnum_label = ttk.Label(menu, textvariable=self.setting_num)
        settingnum_label.grid(row=2, column=1, columnspan=1)
        return menu

    def make_main_frame(self):
        main_frame = ttk.Frame(self)
        canvas = tk.Canvas(main_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        canvas.pack()
        return main_frame, canvas