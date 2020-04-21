from model import Model
from view import View


class Controller:

    MESSAGE_SEPARATOR = ' '.encode('utf-8')

    """
    Takes in a view to communicate with and an input string, formatted, "W:weight, length, width, friction".
    """
    def __init__(self, settings):
        self.model = Model()
        self.view = View(self, self.model)
        self.view.update()
        self.settings_list = settings
        self.curr_setting = -1
        self.next_setting()
        self.finished = False

    def next_setting(self):
        self.curr_setting += 1
        if self.curr_setting == len(self.settings_list):
            self.finished = True
        else:
            self.model.update_settings(self.settings_list[self.curr_setting])

    def prev_setting(self):
        if self.curr_setting != 0:
            self.curr_setting -= 1

    def process_reading(self, reading):
        """
        Processes sensor and encoder readings in real time.
        Takes in an READING formatted as "(motor_pos)m(sensor_dist)s", and sends
        that data to the model. Returns the Normal force felt by each finger.
        """
        split_point = reading.find(' ')
        motor_pos, sensor_dist = reading[:split_point], reading[split_point + 1:]
        return self.model.update_state(int(motor_pos),
                                       int(sensor_dist))
