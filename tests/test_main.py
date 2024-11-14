from peewee import SqliteDatabase
from models import Employee,Review,upload_employees
from src.assignment06 import app
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Don't use a real database, instead, let's use an in-memory version that gets thrown away once tests are done
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        # Bind our tables to this one instead of our people.db file
        self.database.bind([Employee, Review])
        # Connect and create tables
        self.database.connect()
        self.database.create_tables([Employee, Review])
        upload_employees('C:\\python\\first\\310-Au24-07-hr_system-shopkins-seagen\\src\\assignment06\\static\\uploads\\MOCK_DATA_3.csv')
    def tearDown(self):
        self.database.drop_tables([Employee, Review])
        self.database.close()

    def test_get_employees(self):
        employees = app.get_employees()
        self.assertEqual(len(employees),50)
    def test_get_employee(self):
        e = app.get_employees()[0]
        employee = app.get_employee(e.id)
        self.assertEqual(employee.name,e.name)
    def test_add_employee(self):
        emp = {
            "name": "Test",
            "dob": "1999-01-01",
            'address': '123 Main St',
            'ssn':'333-33-3333',
            'title':'dev',
            'started':'2019-01-10'}

        new_employee  = app.add_employee(emp)[1]
        employee = app.get_employee(new_employee.id)
        self.assertEqual(new_employee,employee)

    def test_update_employee(self):
        e = app.get_employees()[2]

        emp = {
            "id":e.id,
            "name": e.name,
            "dob": e.dob,
            'address': 'Omicron Persei 8',
            'ssn': e.ssn,
            'title': e.title,
            'started': e.started,
            'ended': e.ended}

        app.update_employee(emp)
        employee = app.get_employee(e.id)
        self.assertEqual(e.name,employee.name)
        self.assertNotEquals(e.address,employee.address)


if __name__ == '__main__':
    unittest.main()
