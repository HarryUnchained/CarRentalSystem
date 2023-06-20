class Customer:
    def __init__(self, cursor):
        self.cursor = cursor

    def view_all_customers(self):
        query = "SELECT * FROM dbo.Customer"
        self.cursor.execute(query)
        customers = self.cursor.fetchall()

        print("---- All Customers ----")
        for customer in customers:
            print(f"CustomerID: {customer.CustomerID}")
            print(f"First Name: {customer.FirstName}")
            print(f"Last Name: {customer.LastName}")
            print(f"Email: {customer.Email}")
            print(f"Phone: {customer.Phone}")
            print(f"Address: {customer.Address}")
            print("-----------------------")

    def add_customer(self):
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name: ")
        email = input("Enter the email: ")
        phone = input("Enter the phone: ")
        address = input("Enter the address: ")

        query = "INSERT INTO dbo.Customer (FirstName, LastName, Email, Phone, Address) VALUES (?, ?, ?, ?, ?)"
        try:
            self.cursor.execute(query, (first_name, last_name, email, phone, address))
            self.cursor.commit()
            print("Customer added successfully!")
        except Exception as e:
            print("Failed to add customer:", str(e))

    def delete_customer(self):
        customer_id = input("Enter the CustomerID of the customer to delete: ")
        query = "DELETE FROM dbo.Customer WHERE CustomerID = ?"
        try:
            self.cursor.execute(query, customer_id)
            self.cursor.commit()
            print("Customer deleted successfully!")
        except Exception as e:
            print("Failed to delete customer:", str(e))

    def update_customer(self):
        customer_id = input("Enter the CustomerID of the customer to update: ")
        field_name = input("Enter the field name to update (FirstName, LastName, Email, Phone, Address): ")
        new_value = input("Enter the new value: ")

        query = f"UPDATE dbo.Customer SET {field_name} = ? WHERE CustomerID = ?"
        try:
            self.cursor.execute(query, (new_value, customer_id))
            self.cursor.commit()
            print("Customer updated successfully!")
        except Exception as e:
            print("Failed to update customer:", str(e))

    def search_customer(self):
        search_value = input("Enter the value to search: ")

        query = "SELECT * FROM dbo.Customer WHERE FirstName LIKE ? OR LastName LIKE ? OR Email LIKE ? OR Phone LIKE ?"
        self.cursor.execute(query, (f"%{search_value}%", f"%{search_value}%", f"%{search_value}%", f"%{search_value}%"))
        customers = self.cursor.fetchall()

        if len(customers) > 0:
            print("---- Search Results ----")
            for customer in customers:
                print(f"CustomerID: {customer.CustomerID}")
                print(f"First Name: {customer.FirstName}")
                print(f"Last Name: {customer.LastName}")
                print(f"Email: {customer.Email}")
                print(f"Phone: {customer.Phone}")
                print(f"Address: {customer.Address}")
                print("-----------------------")
        else:
            print("No customers found for the given search value.")
