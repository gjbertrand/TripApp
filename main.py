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
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    name TEXT NOT NULL, 
    cost REAL,
    date TEXT,
    time TEXT,
    Description TEXT
            )
            

""")




def main_menu():
    while True:
        clear_console()
        print("""
        ----------------------------
        -The Ultimate Trip Desginer-
        ----------------------------
        
        Welcome to the Ultimate Trip Designer!
        Use this text based tool to create new trip plans
        and fill them with activities""")
        
        print("""
        -------------------------------
        Current: Trips""")
        
        cur = conn.cursor()
        cur.execute("""SELECT trip_id, trip_location FROM trips""")

        current_trips = cur.fetchall()
        if len(current_trips) == 0:
            print("""
        No Trips Found"""

            )
        else:
            for trip in current_trips:
                trip_id, location = trip 
                print(
        f"""        {trip_id}.  {location}""")
        
        print("""       ------------------------------""")
        
        
        menu = """
        COMMANDS:
        Type 'new' to create a new trip
        Type 'edit' to view/edit an existing trip
        Type 'quit' to exit the program


        """
        print(menu)
    
        command = input("Enter Command: ")

        if command == 'new':
            create_trip()
        elif command == 'edit':
            trip_chosen = input("Enter the number associated with the trip you want to view/edit: ")

            if  trip_chosen.isdigit() != True:
                print("Please enter in a valid digit")
                print("Press enter to continue:")
                continue
            trip_chosen = int(trip_chosen)

            script = "SELECT trip_location FROM trips WHERE trip_id = ? "

            cur.execute(script,(trip_chosen,))
            trip = cur.fetchone()

            if trip == None:
                print("No trip found with the given ID")
                input("Press enter to continue: ")
                continue

            else:
                trips_menu(trip_chosen)
        elif command == 'quit':
            print('Ending Program!')
            break
        else:
            print('Invalid Command!Please try again!')
            input('Press enter to continue:')
            continue    

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
        startDate = input("What is the start date of the trip('MM-DD-YYYY format'): ")
        break

    endDate = input("What is the start date of the trip('MM-DD-YYYY format'): ")
    budget = input("What is the budget of the trip(in USD): ")

    startDate = startDate if startDate.strip() != '' else None
    endDate = endDate if endDate.strip() != '' else None
    budget = float(budget) if budget.strip() != '' else None

    if 'main' in [name,startDate,endDate,budget]:
        return 

    sql = """
        INSERT INTO trips(trip_location,start_date,end_date,budget)
        VALUES(?,?,?,?)
    """

    cur = conn.cursor()
    cur.execute(sql,(name,startDate,endDate,budget))
    conn.commit()

    print("Trip Created! Returning to the main menu. Press enter to continue:")

def trips_list():
    pass

def trips_menu(trip_id):
    while True:
        clear_console()
        script = """SELECT trip_id,trip_location,start_date,end_date, budget FROM trips WHERE trip_id = ?"""
        cur.execute(script, (trip_id,))

        trip_info = cur.fetchone()

        tripID,tripLocation,startDate,endDate,budget = trip_info

        script = "SELECT activity_id,name FROM activities WHERE trip_id = ?"

        cur.execute(script,(trip_id,))
        acts = cur.fetchall()


        print(f"""
        ----------------------
        {tripLocation}
        ----------------------- 
        From {startDate} to {endDate}
        Total Budget: {budget}
    """)
        
        print("""
        Activities
        ------------------------------""")
        if len(acts) == 0:
             print("""
        No Activities  Found"""
            )
             
        else:
            for act in acts :
                activity_id, name = act 
                print(
        f"""        {activity_id}.  {name}""")
        
        print("""       ------------------------------""")
        


        

        menu = """
        COMMANDS:
        Type 'edit' to edit the overall trip details
        Tyep 'act' to add/edit/delete actvities
        Type 'main' to return to the homepage
        Type 'full' to see a full look at the itinerary and details
        Type 'delete' to delete this trip


            """
        print(menu)

        command = input("Enter a command: ")

        if command == 'main':
            input("Returning to main menu press enter to continue: ")
            return
        elif command == 'delete':
            print('Are you sure you want to remove this trip? Once removed it cannot be retrieved again')
            deleteInput = input("Type 'yes' to confirm or press enter to keep the trip: ")
            if deleteInput == 'yes':
                cur.execute("""DELETE FROM activities where trip_id = ?""", (tripID,))
                cur.execute("""DELETE FROM trips where trip_id = ?""",(tripID,))
                conn.commit()
                return
            else:
                continue
        elif command == 'full':
            response = full_itinerary(trip_id)

            if response == 'main':
                return
            else:
                continue
        
        elif command == 'act':
            while True:
                command_activity = input("Do you want to 'add', 'delete' or 'edit': ")

                if command_activity == 'add':
                    add_activity(trip_id)
                    break
                
                elif command_activity == 'delete':
                    act_chosen = input('Enter in the number of the activity you would like to delete: ')
                    if  act_chosen.isdigit() != True:
                        print("Please enter in a valid digit")
                        print("Press enter to continue:")
                        continue
                    act_chosen = int(act_chosen)

                    script = "SELECT name FROM activities WHERE activity_id = ?"
                    cur.execute(script,(act_chosen,))
                    act = cur.fetchone()

                    if act == None:
                        print("No activity found with that given ID")
                        input("Press enter to continue: ")
                        continue
                    print('Are you sure you want to remove this trip? Once removed it cannot be retrieved again.')
                    deleteInput = input("Type 'yes' to confirm or press enter to keep the trip: ")
                    if deleteInput == 'yes':
                        script = "DELETE FROM activities where activity_id = ?"
                        cur.execute(script,(act_chosen,))
                        conn.commit()
                        break
                    else:
                        continue
                elif command_activity == 'edit':
                    act_chosen = input('Enter in the number of the activity you would like to edit: ')
                    if  act_chosen.isdigit() != True:
                        print("Please enter in a valid digit")
                        print("Press enter to continue:")
                        continue

                    script = "SELECT name FROM activities WHERE activity_id = ?"
                    cur.execute(script,(act_chosen,))
                    act = cur.fetchone()

                    if act == None:
                        print("No activity found with that given ID")
                        input("Press enter to continue: ")
                        continue

                    else:
                        output = edit_activity(act_chosen)
                        if output == 'main':
                            return
                        break
                elif command_activity == 'main':
                    return 'main'
                else:
                    break
        elif command == 'edit':
             output =edit_trip(trip_id)
             if output == 'main':
                 return
        else:
            print('Invalid Command!Please try again!')
            input('Press enter to continue:')
            continue   

            
    
    return

def add_activity(trip_id):
    clear_console()
    tripScript = 'Select trip_location from Trips where trip_id = ?'
    cur.execute(tripScript, (trip_id,))
    tripName = cur.fetchone()
    tripName = tripName[0]
    print(f"""
    ---------------------------------
    Add activity to {tripName}
    ---------------------------------

    Add in details for a new activity for this trip.
    Type in 'back' to go back to the trip page and type 'main'
    to exit to the main menu. Fields can be left blank by pressing enter. Name is required.          
""")
    
    nameChosen = input("What is the name of the activity: ")
    costChosen = input("What is the cost of the activity(in USD): ")
    dateChosen = input("What is the date of the activity('MM-DD-YYYY'): ")
    timeChosen = input("What is the time of the activity(HH:MM): ")
    descChosen = input("Give a description of the activity: ")

    
    costChosen = float(costChosen) if costChosen.strip() != '' else None
    dateChosen = dateChosen if dateChosen.strip() != '' else None
    timeChosen = timeChosen if timeChosen.strip() != '' else None
    descChosen = descChosen if descChosen.strip() != '' else None

    if 'main' in [nameChosen,costChosen,dateChosen,timeChosen, descChosen]:
        return 'main'
    

    sql = 'INSERT INTO activities(trip_id,name,cost,date,time,description) VALUES (?,?,?,?,?,?)' 

    cur.execute(sql,(trip_id,nameChosen,costChosen,dateChosen,timeChosen,descChosen))
    conn.commit()

    print('Activity was successfully added!')
    input("Press enter to continue: ")
     


     

def full_itinerary(trip_id):
    clear_console()
    
    script = "SELECT trip_location, start_date, end_date, budget FROM trips WHERE trip_id = ?"
    cur.execute(script, (trip_id,))
    trip = cur.fetchone()
    if len(trip) == 0:
        print("Trip not found.")
        input("Press enter to continue: ")
        return

    tripLocation, startDate, endDate, budget = trip

    
    cur.execute("SELECT name, date, time, cost FROM activities WHERE trip_id = ? ORDER BY date ASC, time ASC", (trip_id,))
    activities = cur.fetchall()


    print(f"""
    --------------------------
    -{tripLocation} Itinerary-
    --------------------------

    Start Date: {startDate if startDate else 'N/A'}
    End Date:   {endDate if endDate else 'N/A'}
    Total Budget: {budget if budget else 'N/A'}

    """)

    print(f"{'Activity':<15} | {'Date':<12} | {'Time':<8} | {'Cost':<6}")
    print("-" * 50)

    if len(activities) == 0:
        print("No activities found for this trip.")
    else:
        for act in activities:
            name, date, time, cost = act
            print(f"{name:<15} | {date or 'N/A':<12} | {time or 'N/A':<8} | {cost or 0:<6}")

    print("\nTo exit back to the trip press enter or to go back to the main menu type 'main'")
    command = input("Enter command: ")
    if command == 'main':
        return 'main'

def edit_trip(trip_id):
    clear_console()
    script = "SELECT trip_id,trip_location,start_date,end_date, budget FROM trips WHERE trip_id = ?"
    cur.execute(script, (trip_id,))

    trip_info = cur.fetchone()

    tripID,tripLocation,startDate,endDate,budget = trip_info

    print(f"""
    ----------------------
    {tripLocation}
    ----------------------- 
    From {startDate} to {endDate}
    Total Budget: {budget}


    Enter in new details or press enter to keep the field the same. Set a field to empty by entering '-'
    Type 'main to exit to the main menu'
        
    """)

    locationChosen = input('Create a new name for the trip: ')
    startChosen = input("Create a new start date for the trip('MM-DD-YYY'): ")
    endChosen = input("Create a new end date for the trip('MM-DD-YYYY'): ")
    budgetChosen = input('What is the new budget for the trip: ')

    if 'main' in [locationChosen,startChosen,endChosen,budgetChosen]:
        return 'main'
    confirm = input("Confirm you want to edit the trip by typing 'yes': ")
    if confirm != 'yes':
        return
   
    if locationChosen != '':
        cur.execute("UPDATE trips SET trip_location = ? WHERE trip_id = ?", (locationChosen, trip_id))

    if startChosen == '-':
        cur.execute("UPDATE trips SET start_date = NULL WHERE trip_id = ?", (trip_id,))
    elif startChosen != '':
        cur.execute("UPDATE trips SET start_date = ? WHERE trip_id = ?", (startChosen, trip_id))

    
    if endChosen == '-':
        cur.execute("UPDATE trips SET end_date = NULL WHERE trip_id = ?", (trip_id,))
    elif endChosen != '':
        cur.execute("UPDATE trips SET end_date = ? WHERE trip_id = ?", (endChosen, trip_id))

    if budgetChosen == '-':
        cur.execute("UPDATE trips SET budget = NULL WHERE trip_id = ?", (trip_id,))
    elif budgetChosen != '':
        cur.execute("UPDATE trips SET budget = ? WHERE trip_id = ?", (budgetChosen, trip_id))

    conn.commit()
    print("Trip updated successfully!")
    input('Press enter to continue: ')
    return



    

def edit_activity(activity_id):
    clear_console()
    cur.execute('SELECT name FROM activities where activity_id = ?',(activity_id,))
    name =cur.fetchone()
    name = name[0]
    print(f"""
    ----------------------
    {name}
    ----------------------- 
 
    Enter in new details or press enter to keep the field the same. Set a field to empty by entering '-'
    Type 'main to exit to the main menu'
        
    """)

    nameChosen = input('Edit the name of the activity: ')
    priceChosen = input('Edit the price of the activity: ')
    dateChosen = input("Edit the date of the activity('MM-DD-YYYY'): ")
    timeChosen = input("Edit the time of the activity('HH:MM'): ")
    descChosen = input("Edit the description of the activity: ")

    if 'main' in [nameChosen, priceChosen, dateChosen, timeChosen, descChosen]:
        return 'main'

    confirm = input("Confirm you want to edit the activity by typing 'yes': ")
    if confirm != 'yes':
        return

    if nameChosen != '':
        cur.execute("UPDATE activities SET name = ? WHERE activity_id = ?", (nameChosen, activity_id))

    if priceChosen == '-':
        cur.execute("UPDATE activities SET cost = NULL WHERE activity_id = ?", (activity_id,))
    elif priceChosen != '':
        cur.execute("UPDATE activities SET cost = ? WHERE activity_id = ?", (priceChosen, activity_id))

    if dateChosen == '-':
        cur.execute("UPDATE activities SET date = NULL WHERE activity_id = ?", (activity_id,))
    elif dateChosen != '':
        cur.execute("UPDATE activities SET date = ? WHERE activity_id = ?", (dateChosen, activity_id))

    if timeChosen == '-':
        cur.execute("UPDATE activities SET time = NULL WHERE activity_id = ?", (activity_id,))
    elif timeChosen != '':
        cur.execute("UPDATE activities SET time = ? WHERE activity_id = ?", (timeChosen, activity_id))

    if descChosen == '-':
        cur.execute("UPDATE activities SET Description = NULL WHERE activity_id = ?", (activity_id,))
    elif descChosen != '':
        cur.execute("UPDATE activities SET Description = ? WHERE activity_id = ?", (descChosen, activity_id))

    conn.commit()
    print("Activity updated successfully!")


def clear_console():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # mac or Linux
    else:
        os.system('clear')

main_menu()