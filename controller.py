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
        if self.curr_setting == self.settings.length:
            self.finished = True
        else:
            self.model.update_settings(self.settings_list[self.curr_setting])


    def prev_setting(self):
        if self.curr_setting != 0:
            self.curr_setting -= 1


    """ 
    Processes sensor and encoder readings in real time.
    Takes in an input formatted as "(motor_pos)m(sensor_dist)s", and sends that data to the model.
    """
    def process_readings(self, input):
        #FIXME: handle packet loss
        m_end = input.find('m')
        s_end = len(input) - 1
        self.model.update_state(input[0:m_end], input[m_end + 1:s_end])
