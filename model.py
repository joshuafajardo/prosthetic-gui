from time import time
from item import Item


class Model:

    GRAVITY = 9.81
    MIN_SENSOR_DIST = 0
    MAX_SENSOR_DIST = 100
    CLOSED_MOTOR_POS = 0
    OPEN_GRIP_SEPARATION = 0.2
    GRIPPER_WIDTH = 0.05

    APERTURE_GAIN = 0.0001
    DIST_GAIN = 0.01

    def __init__(self, mass=5, length=0.05, width=0.05, friction_static=0.7, friction_kinetic=0.6, stiffness=0.5):
        self.mass = mass
        self.length = length
        self.width = width
        self.friction_static = friction_static
        self.friction_kinetic = friction_kinetic
        self.stiffness = stiffness
        self.finger_stiffness = 10**4 #todo: ask if this is necessary later on

        self.grip = Item()
        self.block = Item()
        self.grip_sep = self.OPEN_GRIP_SEPARATION
        self.last_time = time()

    """
    Takes in the motor_pos and sensor_dist and updates the state. Returns the new position of the block, the force
    applied to the block.
    """
    #todo: queston: when does kinetic friction turn static?
    def update_state(self, motor_pos, sensor_dist):
        grip_sep_new = motor_pos * self.APERTURE_GAIN #todo

        curr_time = time()
        # todo: sometimes delta_t gives me div by zero error :(
        delta_t = curr_time - self.last_time
        self.last_time = curr_time

        x_grip_new = sensor_dist * self.DIST_GAIN  # todo
        v_grip_new = (x_grip_new - self.grip.x) / delta_t
        a_grip_new = (v_grip_new - self.grip.v) / delta_t

        normal = 0
        # this if statement creates the new block state (and normal force)
        if self.grip.x + self.GRIPPER_WIDTH > self.block.x \
           and self.grip.x < self.block.x + self.length:
            if self.grip_sep < self.width: #in contact
                normal = self.stiffness * (self.width - self.grip_sep) / 2
                v_rel = self.grip.v - self.block.v
                a_req = v_rel / delta_t
                ff_req = self.mass * (a_req + self.GRAVITY) / 2
                ff_max = self.friction_static * normal

                if ff_req <= ff_max:  # static
                    x_block_new = self.block.x + (x_grip_new - self.grip.x)
                    v_block_new = v_grip_new
                    a_block_new = self.grip.a
                else:  # kinetic
                    friction = 2 * normal * self.friction_kinetic * (v_rel / (abs(v_rel) or 1))  # last factor determines sign; the or 1 allows for short circuiting
                    a_block_new = (friction / self.mass) - self.GRAVITY
                    v_block_new = self.block.v + self.block.a * delta_t  # purposely using old acceleration
                    x_block_new = self.block.x + self.block.v * delta_t
            else:  # not in contact
                a_block_new = -self.GRAVITY
                v_block_new = self.block.v + self.block.a * delta_t  # purposely using old acceleration
                x_block_new = self.block.x + self.block.v * delta_t
        else:
            if self.grip_sep < self.width:  # todo: cover case where collision and block runs into the floor/ceiling
                if self.grip.x + self.GRIPPER_WIDTH < self.block.x \
                   and not x_grip_new + self.GRIPPER_WIDTH < self.block.x:  # below block -> collide
                    a_block_new = -self.GRAVITY
                    v_block_new = v_grip_new
                    x_block_new = x_grip_new + self.GRIPPER_WIDTH
                elif self.grip.x > self.block.x + self.length \
                     and not self.grip.x > self.block.x + self.length:  # above block -> collide
                    a_block_new = -self.GRAVITY
                    v_block_new = v_grip_new
                    x_block_new = x_grip_new - self.length
                else:
                    a_block_new = -self.GRAVITY
                    v_block_new = self.block.v + self.block.a * delta_t  # purposely using old acceleration
                    x_block_new = self.block.x + self.block.v * delta_t
            else:  # same code as directly above
                a_block_new = -self.GRAVITY
                v_block_new = self.block.v + self.block.a * delta_t  # purposely using old acceleration
                x_block_new = self.block.x + self.block.v * delta_t

        if x_block_new <= 0:
            self.block.x = 0
            self.block.v = 0
            self.block.a = 0
        else:
            self.block.x = x_block_new
            self.block.v = v_block_new
            self.block.a = a_block_new

        self.grip.x = x_grip_new
        self.grip.v = v_grip_new
        self.grip.a = a_grip_new

        self.grip_sep = grip_sep_new  # updating motor position at the end

        if self.grip.x + self.GRIPPER_WIDTH > self.block.x \
           and self.grip.x < self.block.x + self.length:
            if self.grip_sep < self.width: #in contact
                return self.stiffness * (self.width - self.grip_sep) / 2
        elif self.grip_sep < self.width and self.grip_sep < 0:
            return -self.grip_sep * self.finger_stiffness / 2
        return 0

    """
    Resets the state variables to 0.
    """
    def reset(self):
        self.block.reset()
        self.grip.reset()
        self.grip_sep = self.OPEN_GRIP_SEPARATION
        self.last_time = time()


    """
    Takes in an array, formatted [mass, length, width, static, kinetic, stiffness], and
    updates the model to reflect these settings.
    """
    def update_settings(self, setting):
        self.mass = float(setting[0])
        self.length = float(setting[1])
        self.width = float(setting[2])
        self.friction_static = float(setting[3])
        self.friction_kinetic = float(setting[4])
        self.stiffness = float(setting[5])

        self.reset()



