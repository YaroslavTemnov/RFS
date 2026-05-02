import psycopg2
from psycopg2.extras import DictCursor
import json

def json_import():
    with open("contacts.json", "r") as f:
        data = json.load(f)

    for contact in data:
        cursor.execute(""" INSERT INTO contacts(name, number, email, birthday, group_id) VALUES (%s, %s, %s, %s, %s)""", (
            contact.get("name"),
            contact.get("number"),
            contact.get("email"),
            contact.get("birthday"),
            contact.get("group_id"),
        ))

def json_export():
    cursor.execute("SELECT * FROM contacts")
    result = cursor.fetchall()
    contacts_list = []
    for row in result:
        contacts_list.append(dict(row))
    with open('contacts.json', 'w') as f:
        json.dump(contacts_list, f,indent=2,default=str)

def sort():
    print('\nfor sorting by name enter "n"')
    print('for sorting by birthday enter "b"')
    print('for sorting by date enter "d":')
    sort_by = input()
    print('also enter "d" or "a" for descending or asending order consequently:')
    order = input()
    if sort_by == "n" and order == "a":
        return "ORDER BY name"
    elif sort_by == "n" and order == "d":
        return "ORDER BY name DESC"
    elif sort_by == "b" and order == "a":
        return "ORDER BY birthday"
    elif sort_by == "b" and order == "d":
        return "ORDER BY birthday DESC"
    elif sort_by == "d" and order == "a":
        return "ORDER BY id"
    elif sort_by == "d" and order == "d":
        return "ORDER BY id DESC"

def add_phone():
    def_run = True
    while def_run:
        info = [x for x in input("Enter name, phone and type of number of the contact separated by space:").split()]
        while True:
            print(f"Is info correct?: {info[0]} {info[1]} {info[2]}?")
            correct = input("y/n: ")
            if correct == "y" and len(info) == 3:
                cursor.execute("CALL add_phone(%s, %s, %s)", (info[0], info[1], info[2]))
                conn.commit()
                print("added sucsessfully")
                def_run = False
                break
            if correct == "n":
                break
            else:
                print("Please write fully and correctly")
                continue

def get_info(first, last):
    cursor = conn.cursor(cursor_factory=DictCursor)
    sql = "SELECT * FROM get_contacts(%s, %s) "
    cursor.execute(sql, (first, last))
    result = cursor.fetchall()

    for contact in result:
        print("name: ", contact["name"], "number: ", contact["number"])
    
    if last == 0:
        return None
    else:
        while True:
            print('\nEnter "n" to show next page')
            print('Enter "p" to show previous page')
            print('Enter "q" to quit:')
            page = input()
            if page == "n":
                get_info(first + last, last)
            elif page == "p":
                if first - last > 0:
                    get_info(first - last, last)
                else:
                    print("\nfirst page")
                    get_info(first, last)
            elif page == "q":
                cursor.close()
                return None
            
def search():
    cursor = conn.cursor(cursor_factory=DictCursor)
    while True:
        print('\nEnter name, number or email of the contact, or group name for all contacts of the group')
        print('Or enter "q" to quit:')
        info = input()
        if info == "q":
            break
        else:
            sql = "SELECT * FROM search(%s) " + sort()
            cursor.execute(sql, (info,))
            result = cursor.fetchall()
            if result:
                for contact in result:
                    print(f"name: {contact["name"]} --- number: {contact["number"]}, --- email: {contact["email"]}, phones:")
                    sql = "SELECT * FROM get_contact_phones(%s) "
                    cursor.execute(sql, (contact["id"],))
                    res = cursor.fetchall()
                    for phone_number in res:
                        print(f"{phone_number["phone"]}")
            else:
                print("No matches")
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
                print("Deleted successfully")
                def_run = False
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

def move_to_group():
    while True:
        name, group = [x for x in input("Enter name and group separating by space: ").split()]
        if name and group:
            cursor.execute("CALL move_to_group(%s, %s)", (name, group,))
            conn.commit()
            print("Added successfully")
            break
        else:
            print("please try again")

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
#json_import()


# sql = f"""
#     COPY contacts (name, number, email, birthday, group_id) 
#     FROM STDIN 
#     WITH (FORMAT CSV, HEADER, DELIMITER ',', QUOTE '"', ESCAPE '\\')
#     """
# with open(csv, 'r', ) as f:
#     cursor.copy_expert(sql, f)
# conn.commit()

with open("functions.sql", "r") as f:
    sql = f.read()
    cursor.execute(sql)
    conn.commit()

with open("procedures.sql", "r") as f:
    sql = f.read()
    cursor.execute(sql)
    conn.commit()

# with open("schema.sql", "r") as f:
#     sql = f.read()
#     cursor.execute(sql)
#     conn.commit()
#     print("success")

while True:
    print('Enter "g" to get info')
    print('Enter "s" to search')
    print('Enter "u" to update contact')
    print('Enter "d" to delete contat')
    print('Enter "m" to multiple add')
    print('Enter "a" to add contact')
    print('Enter "p" to add another phone to the contact')
    print('Enter "e" to quit')
    print('Enter "mg" to move a contact into group')
    operation = input()

    if operation == "s":
        search()

    elif operation == "g":
        while True:
            first = int(input("Enter from which to start:"))
            last = int(input("Enter how many contacts:"))
            if first >= 0 and last >= 0:
                get_info(first, last)
                break
            else:
                print("write correctly")

    elif operation == "a":
        add_contact()
    
    elif operation == "p":
        add_phone()

    elif operation == "m":
        multiple_add()

    elif operation == "mg":
        move_to_group()
    elif operation == "e":
        break

    elif operation == "d":
        delete_contact()

    elif operation == "u":
        update_contact()

    else:
        print("please, write correctly")
json_export()
conn.close()
cursor.close()