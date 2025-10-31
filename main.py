import os

import sqlite3
conn = sqlite3.connect('tripapp.db')

#Creating the initial tables
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS trips(
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_location TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    budget REAL
    );
CREATE TABLE IF NOT EXISTS activities(
    actvity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    cost REAL,
    date TEXT,
    time TEXT,
    Description TEXT
            )
            

""")




def main_menu():
    while True:
        print("""
        ----------------------------
        -The Ultimate Trip Desginer-
        ----------------------------
        """)

        
        
        menu = """
        COMMANDS:
        Type 'new' to create a new trip
        Type 'edit' to view/edit an exsisting trip
        Type 'quit' to exit the program

        
        """
        print(menu)
    
        command = input("Enter Command: ")

        if command == 'new':
            create_trip()
        elif command == 'edit':
            trips_menu()
        elif command == 'quit':
            print('Ending Program!')
            break
        else:
            print('Invalid Command!Please try again!')
            print('Press enter to continue:')    

def create_trip():
    clear_console()
    print("""
    -----------------
    -Create New Trip-
    -----------------
    
    Time to start a new adventure! Please answer
    the following questions to initialize a new trip.
    Feel free to leave fields blank by pressing enter.
    Type 'main' if you want to cancel creating a trip

    """)
    
    while True:
        name = input('Create the name for the trip:')
        if name.strip() == '':
            print('The trip requires a name')
            continue
        else:
            break
    
    while True:
        startDate = input("What is the start date of the trip('MM-DD-YYYY format')")
        break

    endDate = input("What is the start date of the trip('MM-DD-YYYY format')")
    budget = input("What is the budget of the trip(in USD)")

    sql = """
        INSERT INTO trips(trip_location,start_date,end_date,budget)
        VALUES(?,?,?,?)
    """

    cur = conn.cursor()
    cur.execute(sql,(name,startDate,endDate,budget))
    conn.commit()

    print("Trip Created! Returning to the main menu. Press enter to continue:")


def trips_menu():
    pass

def clear_console():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # macOS / Linux
    else:
        os.system('clear')

main_menu()