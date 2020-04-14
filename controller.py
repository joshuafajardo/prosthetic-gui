from model import Model
from view import View


class Controller:
    """
    Takes in a view to communicate with and an input string, formatted, "W:weight, length, width, friction".
    """
    def __init__(self, settings):
        self.model = Model()
        self.view = View(self)
        self.curr_setting = 0
        self.settings_list = settings
        self.finished = False

    def next_setting(self):
        self.curr_setting += 1
        if self.curr_setting == self.settings_list.length:
            self.finished = True
        else:
            self.model.update_settings(self.settings_list[self.curr_setting])

    def prev_setting(self):
        if self.curr_setting != 0:
            self.curr_setting -= 1

    def process_readings(self, reading):
        """
        Processes sensor and encoder readings in real time.
        Takes in an READING formatted as "(motor_pos)m(sensor_dist)s", and sends
        that data to the model. Returns the Normal force felt by each finger.
        """
        m_end = reading.find('m')
        s_end = len(reading) - 1
        return self.model.update_state(reading[0:m_end], reading[m_end + 1:s_end])
