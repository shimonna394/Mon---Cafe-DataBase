import sqlite3
import sys
import os
import printdb
import action

def parse_file(filename, cursor):
    file = open(filename)
    for line in file:
        line = line.strip(' \t\n\r')
        content = line.split(',')
        if line.startswith("E"):
            id = content[1].strip('\t\r\n')
            name = content[2].strip('\t\r\n')
            salary = content[3].strip('\n\t\r')
            coffee_stand = content[4].strip('\n\t\r')
            cursor.execute("INSERT INTO Employees (id,name,salary,coffee_stand) \
            VALUES  (?,?,?,?);", (id, name, salary, coffee_stand))
        elif line.startswith("C"):
            id = content[1].strip('\n\t\r')
            location = content[2].strip('\n\t\r')
            number_of_employees = content[3].strip('\n\t\r')
            cursor.execute("INSERT INTO Coffee_stands (id,location,number_of_employees) \
                        VALUES  (?,?,?);", (id, location, number_of_employees))
        elif line.startswith("S"):
            id = content[1].strip('\n\t\r')
            name = content[2].strip('\n\t\r')
            contact_information = content[3].strip('\n\t\r')
            cursor.execute("INSERT INTO Suppliers (id,name,contact_information) \
                                    VALUES  (?,?,?);", (id, name, contact_information))
        elif line.startswith("P"):
            id = content[1].strip('\n\t\r')
            description = content[2].strip('\n\t\r')
            price = content[3].strip('\n\t\r')
            quantity = 0
            cursor.execute("INSERT INTO Products (id,description,price,quantity) \
                                                VALUES  (?,?,?,?);", (id, description, price,quantity))


def create_tables(cursor):
    cursor.executescript("""
    CREATE TABLE Employees
    (id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary REAL NOT NULL,
    coffee_stand INTEGER REFERENCES Coffee_stand(id)
    );
    CREATE TABLE Suppliers
    (id INTEGER PRIMARY KEY,
    name TEXT NOT NULL ,
    contact_information TEXT
    );
    CREATE TABLE Products
    (id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    price REAL NOT NULL,
     quantity INTEGER  NOT NULL 
     );
     CREATE TABLE Coffee_stands
     (id INTEGER PRIMARY KEY,
     location TEXT NOT NULL ,
     number_of_employees INTEGER 
     );
     CREATE TABLE Activities
     (product_id INTEGER REFERENCES Product(id),
     quantity INTEGER NOT NULL,
     activator_id INTEGER NOT NULL,
     date DATE NOT NULL
     );
""")


def main(args):
    if os.path.isfile('moncafe.db'):
        os.remove('moncafe.db')
    dbcon = sqlite3.connect('moncafe.db')
    with dbcon:
        cursor = dbcon.cursor()
        filename = os.path.abspath(os.path.realpath(sys.argv[1]))
        create_tables(cursor)
        parse_file(filename, cursor)
    dbcon.commit()
    dbcon.close()


if __name__ == '__main__':
    main(sys.argv)
