import sqlite3

def main():
    conn = sqlite3.connect("Misbach_Christopherson.db") 
    cursor = conn.cursor()

    while True:
        choice = printQueryMenu()
        if choice == "6":
            print("Exiting...")
            break
        runQueryFromChoice(choice, cursor)
        
    conn.close()
            

def printQueryMenu():
    print("Choose a query to run (by number):")
    print("1. Venues above a capacity")
    print("2. Payments above an amount using method")
    print("3. Concerts by a performer name.")
    print("4. Customers with a specific seat type / ticket type")
    print("6. Exit")
    return input("\nEnter your choice: ")

def runQueryFromChoice(choice, cursor):
    if choice == "1":
        capacity = int(input("Enter the minimum capacity: "))
        cursor.execute("SELECT Name FROM Venue WHERE Capacity > ?", (capacity,))
        rows = cursor.fetchall()
        print(rows)
        print()
    elif choice == "2":
        print("\nEnter the payment details:")
        print("Note: The payment method should be one of the following: cash, credit card, debit card\n")
        amount = float(input("Enter the minimum payment amount: "))
        method = input("Enter the payment method: ")
        cursor.execute("SELECT * FROM Payment WHERE Amount > ? AND Method = ?", (amount, method.capitalize()))
        rows = cursor.fetchall()
        print(rows)
        print()
    elif choice == "3":
        examples = cursor.execute("SELECT Name From Performer").fetchall()
        print("Examples of performers within the database:")
        print(examples)
        performer_name = input("Enter the performer's name: \n")
        cursor.execute("""SELECT c.Title
                            FROM Performs ps
                            JOIN Concert c ON c.ConcertId = ps.PerformerID
                            JOIN Performer p ON p.PerformerID = ps.PerformerID
                            WHERE p.Name = ?;""", (performer_name,))
        rows = cursor.fetchall()
        print(rows)
        print()
    elif choice == "4":
        seat_type = input("Enter the seat type: ")
        cursor.execute("""SELECT cu.FirstName, cu.LastName, t.SeatNumber
                        FROM Customer cu
                        JOIN Purchases p ON cu.CustomerID = p.CustomerID
                        JOIN Ticket t ON p.TicketID = t.TicketID
                        WHERE t.SeatNumber = ?;
                        """, (seat_type,))
        rows = cursor.fetchall()
        print(rows)
        print()
    elif choice == "5":
        print("This query is not implemented yet.")
    else:
        print("Invalid choice. Please try again.")




if __name__ == "__main__":
    main()