from time import time

class Model:

    GRAVITY = 9.81

    def __init__(self, weight=50, length=5, width=5, friction=0.7):
        self.weight = weight
        self.length = length
        self.width = width
        self.friction = friction
        self.last_time = time()
        self.contact_angle = 0 #TODO
        self.gripped_angle = 0 #TODO

        # TODO: initialize the state variables, such as: obj position, obj vel, obj accel, etc (if any more needed).

    """
    Takes in the motor_pos and sensor_dist and updates the state. Returns the new position of the block.
    """
    def update_state(self, motor_pos, sensor_dist):
        curr_time = time.time()
        delta_t = curr_time - self.last_time
        self.last_time = curr_time

        if motor_pos >= self.gripped_angle:
            pass
            return #todo
        elif motor_pos >= self.contact_angle:
            pass
            return #todo
        else:
            pass
            return #todo

    """
    Calculates the force of friction between the gripper and the block.
    """
    def calculate_friction(self):
        pass

    """
    Resets the state variables to 0.
    """
    def restart(self):
        pass

    """
    Takes in an array, formatted [weight, length, width, friction], and
    updates the model to reflect these settings.
    """
    def update_settings(self, setting):
        pass



