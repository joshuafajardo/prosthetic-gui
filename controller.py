from model import Model


class Controller:
    """
    Takes in an input SETTINGS string, formatted, "W:weight, length, width, friction".
    """
    def __init__(self, settings):
        self.model = Model()
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
            self.model.update_settings(self.settings_list[self.curr_setting])

    def process_reading(self, reading):
        """
        Processes sensor and encoder readings in real time.
        Takes in an READING formatted as "(motor_pos) (sensor_dist)", and sends
        that data to the model. Returns the Normal force felt by each finger.
        For testing purposes, process_reading is also capable of setting the model to a certain position.
        Testing lines are formatted: "SETUP block_x grip_x grip_sep"
        """
        print(reading)
        if "SETUP" in reading:
            reading = reading.split(' ')
            self.model.setup(float(reading[1]), float(reading[2]), float(reading[3]))
        elif "ENV_INFO" in reading:
            return self.model.curr_settings()
        else:
            split_point = reading.find(' ')
            motor_pos, sensor_dist = reading[:split_point], reading[split_point + 1:]
            return self.model.update_state(float(motor_pos),
                                           float(sensor_dist))
