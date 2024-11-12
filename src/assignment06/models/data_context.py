from peewee import *

db = SqliteDatabase('hr.db',pragmas={'journal_mode':'wal','foreign_keys': 1})

class Employee(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    dob = DateField()
    address = CharField(null=True)
    ssn = CharField()
    title = CharField()
    start_date = DateField()
    end_date = DateField(null=True)
    class Meta:
        database = db
        db_table = 'Employee'
class Review(Model):
    id = IntegerField(primary_key=True)
    rating = IntegerField()
    review_date = DateField()
    comment = CharField()
    employee_id=ForeignKeyField(Employee,backref='Reviews')
    class Meta:
        database = db
        db_table = 'Reviews'

def create():
    db.create_tables([Employee,Review])
def seed():

    for n in ["Shawn" , "Steve", "Tim"]:
        e = Employee(name=n, dob="10-Sep-1971", address="localhost", ssn="444-444-4444",start_date="28-May-2008",title="Dev")
        e.save()

    # rec = Employee(name="Steve", dob="10-Sep-1971", address="localhost", ssn="444-444-4444",start_date="28-May-2008",title="Dev")
    # rec.save()
    # rev = Review( rating=3, review_date="10-Nov-2023", comment="guy rules",employee_id=rec.id)
    # rev.save()


def get_employees():

    employees = Employee.select(Employee,Review).join(Review)
    return employees

create()
seed()