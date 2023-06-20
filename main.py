import pyodbc

from Login import Login


def create_connection(server: str, database: str) -> pyodbc.Connection:
    # Set up the connection string
    connection_string = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes"

    try:
        # Establish the connection
        conn = pyodbc.connect(connection_string, timeout=2)
        print(f"Connection to {server} successful!")
        return conn
    except pyodbc.Error:
        raise


def user_signin(cursor):
    login = Login(cursor=cursor)
    # Get username and password from user input
    while True:

        username = input("Enter UserName: ")
        password = input("Enter Password: ")

        # Check if username or password is empty
        if not username or not password:
            print("Username or password cannot be empty. Please try again.")
        else:
            try:
                # Try logging in
                login.authenticate(username, password)
                break  # Break the loop if authentication is successful
            except Exception as e:
                print(f"An error occurred during login: {str(e)}")


# Before running the program install python and relevant libraries.
# Use pip install pyodbc,
#     pip install tabulate,
#     pip install requests
def main():
    # Set up the server connection parameters
    # Uses Windows Authentication so only requires server name and database name.
    # After creating database add an entry to admin table
    # PhoneNumber = Your Whatsapp number starting with +92 or 03 please note to use
    # a number which is on whatsapp where you wish to receive an otp
    # Number must not contain any spaces or other characters eg: +923009994333
    # Set the Master field to 1 meaning True

    server = 'CompleteServerName using \\ eg. MARK-IV\\SQLEXPRESS'
    database = 'DatabaseName eg. CarRental'
    conn = None
    cursor = None
    try:
        # Create the connection
        conn = create_connection(server, database)
        print("Connection created successfully")

        # Create a cursor object to execute SQL queries
        # Use the cursor to execute SQL queries or perform other database operations
        cursor = conn.cursor()
        user_signin(cursor)
    except pyodbc.Error as e:
        print(f"An error occurred with the database: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and the connection when you're done
        cursor.close()
        print("Cursor closed")

        if conn is not None:
            conn.close()
            print("Connection closed")

        else:
            print("Connection wasn't established")


if __name__ == '__main__':
    main()
