import unittest
import model

class TestMain(unittest.TestCase):
    def test_script_reading(self):
        pass

class TestModel(unittest.TestCase):
    def __init__(self):
        super()
        self.model = model.Model()

    def test_update(self):
        pass


class TestController(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()