from models import Employee
from src.assignment06 import app
import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):

        response = app.get_employees().get()
        print(response)

if __name__ == '__main__':
    unittest.main()
