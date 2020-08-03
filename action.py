import os
import printdb
import sqlite3
import sys

def create_Activities(filename, cursor):
    file = open(filename)
    for line in file:
        line = line.strip(' \t\n\r')
        content = line.split(',')
        product_id=content[0].strip('\t\r\n')
        quantity=content[1].strip('\t\r\n')
        activator_id=content[2].strip('\t\r\n')
        date=content[3].strip('\t\r\n')
        originalQuantity = cursor.execute("SELECT quantity FROM Products Where id=?", [product_id])
        for quan in originalQuantity:
            update=quan[0]+int(quantity)
            if not update<0:
                cursor.execute("UPDATE Products set quantity=? WHERE id=?",[update,product_id])
                cursor.execute("INSERT INTO Activities (product_id,quantity,activator_id,date) \
                            VALUES  (?,?,?,?);", (product_id, quantity, activator_id, date))


def main(args):
    if os.path.isfile('moncafe.db'):
        dbcon = sqlite3.connect('moncafe.db')
        with dbcon:
            cursor = dbcon.cursor()
            filename = os.path.abspath(os.path.realpath(sys.argv[1]))
            create_Activities(filename,cursor)
        dbcon.commit()
        printdb.main()
        dbcon.close()
if __name__ == '__main__':
    main(sys.argv)


