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
    print("1. Venues above a capacity.")
    print("2. Payments above an amount using a specific method.")
    print("3. Concerts by a performer name.")
    print("4. Customers with a specific seat type / ticket type.")
    print("5. Find Performers by a specific genre.")
    print("6. Exit")
    return input("\nEnter your choice: ")

def runQueryFromChoice(choice, cursor):
    if choice == "1":
        capacity = int(input("Enter the minimum capacity: "))
        cursor.execute("SELECT Name FROM Venue WHERE Capacity > ?", (capacity,))
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(row[0])
            print()
        else:
            print("No venues found above specified capacity.")
    elif choice == "2":
        print("\nEnter the payment details:")
        print("Note: The payment method should be one of the following: Cash, Card, Online\n")
        amount = float(input("Enter the minimum payment amount: "))
        method = input("Enter the payment method: ")
        cursor.execute("SELECT * FROM Payment WHERE Amount > ? AND Method = ?", (amount, method.capitalize()))
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(row[1], row[2], row[3])
            print()
        else:
            print("No payments found for the specified amount and method.")
    elif choice == "3":
        examples = cursor.execute("SELECT Name From Performer").fetchall()
        print("Examples of performers within the database:")
        print(examples)
        performer_name = input("\nEnter the performer's name: ")
        cursor.execute("""SELECT c.Title
                            FROM Performs ps
                            JOIN Concert c ON c.ConcertId = ps.PerformerID
                            JOIN Performer p ON p.PerformerID = ps.PerformerID
                            WHERE p.Name = ?;""", (performer_name,))
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(row[0])
            print()
        else:
            print("No concerts found for the specified performer.")
    elif choice == "4":
        examples = cursor.execute("SELECT SeatNumber From Ticket").fetchall()
        print("Examples of seat types within the database:")
        print(examples)
        seat_type = input("\nEnter the seat type: ")
        cursor.execute("""SELECT cu.FirstName, cu.LastName, t.SeatNumber
                        FROM Customer cu
                        JOIN Purchases p ON cu.CustomerID = p.CustomerID
                        JOIN Ticket t ON p.TicketID = t.TicketID
                        WHERE t.SeatNumber = ?;
                        """, (seat_type,))
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(row[0])
            print()
        else:
            print("No customers found for the specified seat type.")
    elif choice == "5":
        genre = input("Enter the genre of performers you'd like to find: ")
        cursor.execute("""SELECT Name FROM Performer WHERE Genre LIKE ?""", (genre,))
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row[0])
            print()
        else:
            print("No performers found for the specified genre.")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()