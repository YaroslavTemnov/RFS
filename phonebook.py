import psycopg2
from psycopg2.extras import DictCursor

def get_info():
    cursor = conn.cursor(cursor_factory=DictCursor)
    while True:
        print("Enter 1 for all contacts in ascending order by name")
        print("Enter 2 for all contacts in descending order by name")
        print("Enter 3 for all contacts in ascending order by number")
        print("Enter 4 for all contacts in descending order by number:")
        order = input()
        if order == "1":
            cursor.execute("SELECT * FROM contacts ORDER BY name ASC")
            result = cursor.fetchall()
            for key in result:
                print("name:", key["name"], "---", "number:", key["number"])
            break
        elif order == "2":
            cursor.execute("SELECT * FROM contacts ORDER BY name DESC")
            result = cursor.fetchall()
            for key in result:
                print("name:", key["name"], "---", "number:", key["number"])
            break
        elif order == "3":
            cursor.execute("SELECT * FROM contacts ORDER BY number ASC")
            result = cursor.fetchall()
            for key in result:
                print("name:", key["name"], "---", "number:", key["number"])
            break
        elif order == "4":
            cursor.execute("SELECT * FROM contacts ORDER BY number DESC")
            result = cursor.fetchall()
            for key in result:
                print("name:", key["name"], "---", "number:", key["number"])
            break
        else:
            print("choose only one option (1/2/3/4):")
            continue
    cursor.close()

def search():
    cursor = conn.cursor(cursor_factory=DictCursor)
    while True:
        info = input("Enter a name or a number of the contact that you want to find or write exit to exit:")
        if info == "exit":
            break
        else:
            sql = f"SELECT * FROM contacts WHERE name LIKE '%{info}%' OR number LIKE '%{info}%'" 
            cursor.execute(sql)
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
            sql = f"INSERT INTO contacts(name, number) VALUES(%s, %s)"
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
            sql = "DELETE FROM contacts WHERE name = %s OR number = %s"
            while True:
                print(f"Are you sure that you want to delete this contact: {name}?")
                correct = input("y/n: ")
                if correct == "y":
                    cursor.execute(sql, (name, name))
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

while True:
    operation = input("get info / search / update contact / delete contact / add contact / exit : ")
    if operation == "search":
        search()
    elif operation == "get info":
        get_info()
    elif operation == "add contact":
        add_contact()
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