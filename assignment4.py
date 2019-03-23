import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import folium

# ================================================================================
# // User inputs and error handling
# ================================================================================
def enter_db_name():
    db_name = input("Enter the name of the database you want to access (without .db): \t")
    return db_name
def main():
    database_name = enter_db_name()
    check_connection = 'file:{}.db?mode=rw'.format(database_name)
    try:
        conn = sqlite3.connect(check_connection, uri=True)
        database_name = "./{}.db".format(database_name)
        main_query(database_name)
    except sqlite3.OperationalError:
        print("database doesn't exist, try again!")
        main()
# ================================================================================
# // Main function
# ================================================================================

def main_query(database_name):
    while True:
        print("""
        1. Q1               2. Q2
        3. Q3               4. Q4
        5. QUIT
        """)
        #Ask user to input a number between 1-5
        #Which further calls the respective function
        choice = input('Choose from above: ')
        if choice == '1':
            print('1 option')
            q1(database_name)
        elif choice == '2':
            print('2 option')
            q2(database_name)
        elif choice == '3':
            print('3 option')
            q3(database_name)
        elif choice == '4':
            print('4 option')
            q4(database_name)
        elif choice == '5':
            exit(0)
        else:
            print('Invalid Input. Try again')
# ================================================================================
# // Q1
# ================================================================================
def q1(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)
# ================================================================================
# // Q2
# ================================================================================
def q2(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)
# ================================================================================
# // Q3
# ================================================================================
def q3(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)
# ================================================================================
# // Q4
# ================================================================================
def q4(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    conn.close()
    main_query(database_name)