from time import time
from item import Item

class Model:

    GRAVITY = 9.81
    MIN_SENSOR_DIST = 0
    MAX_SENSOR_DIST = 100
    CLOSED_MOTOR_POS = 0
    OPEN_GRIP_SEPARATION = 8
    GRIPPER_WIDTH = 5

    def __init__(self, mass=50, length=5, width=5, friction_static=0.7, friction_kinetic=0.6, stiffness=0.5):
        self.mass = mass
        self.length = length
        self.width = width
        self.friction_static = friction_static
        self.friction_kinetic = friction_kinetic
        self.stiffness = stiffness
        self.last_time = time()
        self.grip = Item()
        self.block = Item()
        self.grip_sep = self.OPEN_GRIP_SEPARATION

    """
    Takes in the motor_pos and sensor_dist and updates the state. Returns the new position of the block, the force
    applied to the block.
    """
    #todo: queston: when does kinetic friction turn static?
    def update_state(self, motor_pos, sensor_dist):
        grip_sep_new = 0 #todo
        x_grip_new = 0 #todo


        curr_time = time.time()
        delta_t = curr_time - self.last_time
        self.last_time = curr_time

        v_grip_new = (x_grip_new - self.grip.x) / delta_t
        a_grip_new = (v_grip_new - self.grip.v) / delta_t

        #todo: what outcome do we want if the gripper is closed, then the hand is lowered onto the block?
        if self.grip_sep < self.block.width \
           and self.grip.x + self.GRIPPER_WIDTH > self.block.x \
           and self.grip.x < self.block.x + self.length:
            N = self.stiffness * (self.block.width - self.grip_sep)
            if 1: #todo: static
                self.block.x += (x_grip_new - self.grip.x)
                self.block.v = self.grip.v
                self.block.a = self.grip.a
            else: #kinetic
                pass

            self.block.a = (self.calc_applied_force(motor_pos) / self.mass) - self.GRAVITY


        self.block.v = self.block.a * delta_t



        self.block.x = 0 #todo

        self.block.x = min(self.MIN_SENSOR_DIST, max(self.MAX_SENSOR_DIST, self.pos))
        self.motor_pos = motor_pos #updating motor position at the end


    def sum_of_forces(self):
        gravity = self.mass * self.GRAVITY
        if (self.grip_sep < self.contact_angle):
            normal = 0
            friction = 0
        else:
            normal = self.displacement(self.grip_sep) * self.stiffness
            applied = 0 #todo

    def displacement(self):
        pass

    def is_gripped(self, ):
        pass

    """
    Resets the state variables to 0.
    """
    def restart(self):
        pass

    """
    Takes in an array, formatted [mass, length, width, friction], and
    updates the model to reflect these settings.
    """
    def update_settings(self, setting):
        pass



