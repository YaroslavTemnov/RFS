import psycopg2
from psycopg2.extras import DictCursor

def get_info():
    cursor = conn.cursor(cursor_factory=DictCursor)
    while True:
        first = int(input("Enter from which to start:"))
        last = int(input("Enter how many contacts:"))
        if first and last:
            sql = "SELECT * FROM get_contacts(%s, %s) "
            cursor.execute(sql, (first, last))
            result = cursor.fetchall()
            for contact in result:
                print("id: ", contact["id"], "name: ", contact["name"], "number: ", contact["number"])
            break
        else:
            print("write correctly")
            
    cursor.close()

def search():
    cursor = conn.cursor(cursor_factory=DictCursor)
    while True:
        info = input("Enter a name or a number of the contact that you want to find or write exit to exit:")
        if info == "exit":
            break
        else:
            sql = "SELECT * FROM search(%s)"
            cursor.execute(sql, (info,))
            result = cursor.fetchall()
            for contact in result:
                print(f"name: {contact["name"]} --- number: {contact["number"]}")
            break
    cursor.close()



def add_contact():
    def_run = True
    while def_run:
            name = input("Enter the name: ")
            number = input("Enter the number: ")
            sql = "SELECT upsert(%s, %s)"
            while True:
                print(f"Is data correct?\nname: {name}; number: {number}")
                correct = input("y/n: ")
                if correct == "y":
                    cursor.execute(sql, (name, number))
                    conn.commit()
                    print("added successfully")
                    def_run = False
                    break
                if correct == "n":
                    break
                else:
                    continue
        
def delete_contact():
    def_run = True
    while def_run:
            name = input("Enter the name or number of the contact that you want to delete: ")
            while True:
                print(f"Are you sure that you want to delete this contact: {name}?")
                correct = input("y/n: ")
                if correct == "y":
                    cursor.execute("CALL delete_contact(%s)", (name,))
                    conn.commit()
                    print("Deleted sucsessfully")
                    def_run = False
                    break
                if correct == "n":
                    break
                else:
                    continue
    
def update_contact():
    def_run = True
    while def_run:
            name = input("Enter the name that you want to update: ")
            new_name = input("Enter the new name: ")
            new_number = input("Enrer the new number: ")
            sql = f"UPDATE contacts SET name = %s, number = %s WHERE name = %s"
            while True:
                print(f"Is new data correct?\nnew name: {new_name}; new number: {new_number}")
                correct = input("y/n: ")
                if correct == "y":
                    cursor.execute(sql, (new_name, new_number, name))
                    conn.commit()
                    print("updated successfully")
                    def_run = False
                    break
                if correct == "n":
                    break
                else:
                    continue
def multiple_add():
    names = [x for x in input("Enter a names of the contacts through space:").split()]
    numbers = [x for x in input("Enter a numbers of the contacts through space:").split()]
    cursor.execute("CALL multiple_inserting(%s, %s, %s)", (names, numbers, None))
    conn.commit()


try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        user = "postgres",
        password = "12345678",
        port = 5432,
        dbname = "phonebook"
    )
    print("Connection succesful!")
except:
    print("Conection failed")

cursor = conn.cursor(cursor_factory=DictCursor)
cursor.execute("SELECT * FROM contacts")
result = cursor.fetchall()
table_name = "contacts"
csv = "contacts.csv"

sql = f"""
    COPY contacts (name, number) 
    FROM STDIN 
    WITH (FORMAT CSV, HEADER, DELIMITER ',', QUOTE '"', ESCAPE '\\')
    """
with open(csv, 'r', ) as f:
    cursor.copy_expert(sql, f)

conn.commit()
with open("functions.sql", "r") as f:
    sql = f.read()
    cursor.execute(sql)
    conn.commit()
with open("procedures.sql", "r") as f:
    sql = f.read()
    cursor.execute(sql)
    conn.commit()

while True:
    operation = input("get info / search / update contact / delete contact / multiple add / add contact / exit : ")
    if operation == "search":
        search()
    elif operation == "get info":
        get_info()
    elif operation == "add contact":
        add_contact()
    elif operation == "multiple add":
        multiple_add()
    elif operation == "exit":
        break
    elif operation == "delete contact":
        delete_contact()
    elif operation == "update contact":
        update_contact()
    else:
        print("please, write correctly")

conn.close()
cursor.close()