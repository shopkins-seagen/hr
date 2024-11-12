
class Review():
    def __init__(self,id,title,rating,comment):
        self.id=id
        self.title=title
        self.rating=rating
        self.comment=comment
class Employee():
    def __init__(self,id,name,dob,address,ssn,title,start_date,end_date):
        self.id = id
        self.name = name
        self.dob = dob
        self.address = address
        self.ssn = ssn
        self.title = title
        self.start_date = start_date
        self.end_date =end_date
        self.reviews =[]
class Employees():
    def __init__(self):
        self.employees =[]

def load():
    for n in ["Shawn","Steve","Chris"]:
        e = Employee(n,"")

