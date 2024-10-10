import sqlite3

# connect to sqlitte
connections = sqlite3.connect("-- ENTER NAME OF DB TO BE CREATED --")

# Create a cursor object to insert record, create table -
cursor = connections.cursor()

# Create the table - 
table_info = """
--- TABLE FIELDS ---
EXAMPLE:- create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

# Insert some more records -
""" -- EXECUTE DETAILS IN TABLE --"""
cursor.execute('''Insert into STUDENT values("John", "DataScience", "A", 100)''')
cursor.execute('''Insert into STUDENT values("Henry", "Construction", "B", 60)''')
cursor.execute('''Insert into STUDENT values("Tom", "Art", "C", 65)''')
cursor.execute('''Insert into STUDENT values("Sam", "Medicines", "D", 55)''')

# Display all the records - 
print("Inserted records are - ")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

# commit changes in your database - 
connections.commit()
connections.close()