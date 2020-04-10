import unittest
import model
import time

class TestMain(unittest.TestCase):
    def test_script_reading(self):
        pass

class TestModel(unittest.TestCase):
    def test_update_settings(self):
        my_model = model.Model()
        my_model.update_settings([3, 0.05, 0.04, 0.7, 0.4, 10**4])
        self.assertTrue(my_model.mass == 3)
        self.assertTrue(my_model.stiffness == 10**4)

    """
    [mass=0.25, length=.05, width=.04, static=0.7, kinetic=0.4, stiffness=10^4]
    """
    def test_basic_lifting(self):
        my_model = model.Model()
        my_model.APERTURE_GAIN = 0.01
        my_model.DIST_GAIN = 0.01
        my_model.update_settings([0.25, 0.05, 0.04, 0.7, 0.4, 10**4])
        time.sleep(0.05)
        self.assertTrue(my_model.update_state(4.01, 0) == 0)
        time.sleep(0.05)
        self.assertTrue(my_model.update_state(3.99, 0) == 0)
        time.sleep(0.05)
        self.assertAlmostEqual(my_model.update_state(3.95, 0), 0.5)
        time.sleep(0.05)
        self.assertAlmostEqual(my_model.update_state(3.95, 0), 2.5)
        time.sleep(0.5)
        self.assertAlmostEqual(my_model.update_state(3.95, 1), 2.5)
        self.assertAlmostEqual(my_model.block.x, 0.01)
        time.sleep(0.5)
        self.assertAlmostEqual(my_model.update_state(3.95, 1), 2.5)
        time.sleep(0.5)
        self.assertAlmostEqual(my_model.update_state(4.01, 1), 2.5)
        time.sleep(0.5)
        self.assertAlmostEqual(my_model.update_state(4.01, 1), 0)
        time.sleep(1)
        my_model.update_state(4.01, 1)
        self.assertAlmostEqual(my_model.block.x, 0) #todo is it bad that it needs to wait through so many iterations?


class TestController(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()