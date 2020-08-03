import sqlite3
import os
def print_db(cursor):
    cursor.execute("SELECT * FROM Activities;")
    Activities = cursor.fetchall()
    print("Activities")
    for Activities in Activities:
        print(Activities)

    cursor.execute("SELECT * FROM Coffee_stands;")
    Coffee_stands = cursor.fetchall()
    print("Coffee_stands")
    for Coffee_stands in Coffee_stands:
        print(Coffee_stands)

    cursor.execute("SELECT * FROM Employees;")
    Employees = cursor.fetchall()
    print("Employees")
    for Employees in Employees:
        print(Employees)

    Products = cursor.execute("SELECT * FROM Products;").fetchall()
    print("Products")
    for Products in Products:
        print(Products)

    cursor.execute("SELECT * FROM Suppliers;")
    Suppliers = cursor.fetchall()
    print("Suppliers")
    for Suppliers in Suppliers:
        print(Suppliers)

    createIncome(cursor)
    cursor.execute("SELECT Employees.name,Employees.salary,Coffee_stands.location,Employees_income.income "
                   "FROM (Employees INNER JOIN Coffee_stands ON  Employees.coffee_stand=Coffee_stands.id) "
                   "INNER JOIN Employees_income ON Employees.id=Employees_income.id "
                   "ORDER BY Employees.name")
    Employees_reports=cursor.fetchall()
    print("\nEmployees reports")
    for Employees_reports in Employees_reports:
        name=(str(Employees_reports[0]))
        income=Employees_reports[3]
        Employees_reports=(name,Employees_reports[1],str(Employees_reports[2].strip(" ")),income)
        toPrint=""
        for i in Employees_reports:
            toPrint=toPrint+str(i)+ " "
        print(toPrint[0:-1])
    cursor.execute("DROP TABLE IF EXISTS Employees_income")

    cursor.execute("""
    SELECT Activities.date , Products.description , Activities.quantity , Employees.name , 
                   Suppliers.name
                   FROM Activities
                   INNER JOIN Products ON (Activities.product_id=Products.id) 
                   LEFT JOIN Employees ON (Activities.activator_id=Employees.id)
                   LEFT JOIN Suppliers ON (Activities.activator_id=Suppliers.id)
                   ORDER BY Activities.date
                   """)
    activities=cursor.fetchall()
    if activities:
        print("\nActivities")
        for act in activities:
            print(act)


def createIncome(cursor):
    cursor.executescript("""
            CREATE TABLE Employees_income
            (id INTEGER REFERENCES Employees(id),
            income REAL NOT NULL 
            );
        """)
    Employees=cursor.execute("SELECT id FROM Employees").fetchall()
    for employee in Employees:
        cursor.execute("INSERT INTO Employees_income (id,income)\
            VALUES  (?,?);", (employee[0], 0))
    Actions=cursor.execute("SELECT * FROM Activities").fetchall()
    for action in Actions:
        quantity=float(action[1])
        if quantity<0:
            product_id=action[0]
            Products=cursor.execute("SELECT price From Products Where id=?", [product_id])
            for product in Products:
                price=product[0]
                update=(price*(-quantity))
                cursor.execute("UPDATE Employees_income set income=income+? WHERE id=?", [update,action[2]])



def main():
    if os.path.isfile('moncafe.db'):
        dbcon = sqlite3.connect('moncafe.db')
        with dbcon:
            cursor = dbcon.cursor()
            print_db(cursor)
        dbcon.commit()
        dbcon.close()

if __name__ == '__main__':
    main()