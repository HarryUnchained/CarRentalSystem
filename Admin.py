from tabulate import tabulate

import Car
import Customer


class Admin:
    def __init__(self, cursor, is_master):
        self.cursor = cursor
        self.is_master = is_master

    def main_menu(self):
        print("----Main Menu----")
        menu_options = [
            "Dashboard",
            "Manage Cars",
            "Manage Customer",
            "Rent a Car",
            "Return Cars",
            "View All Cars"
        ]
        if self.is_master:
            menu_options.append("Manage Admins")
        menu_options.append("Exit")

        for i, option in enumerate(menu_options, start=1):
            print(f"{i}. {option}")
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            self.dashboard()
        elif user_choice == "2":
            self.manage_cars()
        elif user_choice == "3":
            self.manage_customer()
        elif user_choice == "4":
            self.rent_car()
        elif user_choice == "5":
            self.return_cars()
        elif user_choice == "6":
            self.view_all_cars()
        elif user_choice == "7" and self.is_master:
            self.manage_admins()
        elif user_choice == "8":
            return
        else:
            print("Invalid choice. Please try again.")

    def dashboard(self):
        cursor = self.cursor
        query = "SELECT TotalCars, TotalCustomers, TotalBookedCars FROM DashboardView"
        cursor.execute(query)
        result = cursor.fetchone()
        total_cars = result.TotalCars
        total_customers = result.TotalCustomers
        total_booked_cars = result.TotalBookedCars

        print("Total Cars ==> [", total_cars, "]")
        print("Total Customers ==> [", total_customers, "]")
        print("Total Booked Cars ==> [", total_booked_cars, "]")

        input("Press any key to exit...")

    def manage_cars(self):
        print("----Manage Cars----")
        menu_options = ["View All Cars", "Add a New Car", "Update Car Info",
                        "Delete a Car Record", "Send a Car for Maintenance"]
        for i, option in enumerate(menu_options, start=1):
            print(f"{i}. {option}")
        user_choice = input("Enter your choice: ")
        car = Car.Car(cursor=self.cursor)
        if user_choice == 1:
            car.view_all_cars()
        elif user_choice == 2:
            car.add_car()
        elif user_choice == 3:
            car.update_car()
        elif user_choice == 4:
            car.delete_car()
        else:
            car.send_car_for_maintenance()

    def manage_customer(self):
        print("----Manage Customer----")
        menu_options = ["View All Customers", "Add New Customer", "Delete Customer", "Update Customer"]
        while True:
            for i, option in enumerate(menu_options, start=1):
                print(f"{i}. {option}")
            user_choice = input("Enter your choice: ")
            customer = Customer.Customer(cursor=self.cursor)
            if user_choice == "1":
                customer.view_all_customers()
            elif user_choice == "2":
                customer.add_customer()
            elif user_choice == "3":
                customer.delete_customer()
            elif user_choice == "4":
                customer.update_customer()
            else:
                print("Invalid choice. Please try again.")
                continue

            choice = input("Do you want to continue managing customers? (Y/N): ")
            if choice.lower() != "y":
                break

    def rent_car(self):
        print("---- Rent a Car ----")
        # Implement the logic to rent a car

        # Get the available cars using the ViewAvailableCars view
        query = "SELECT * FROM ViewAvailableCars"
        self.cursor.execute(query)
        available_cars = self.cursor.fetchall()

        # Display the available cars to the user
        print("Available Cars:")
        for car in available_cars:
            print(f"Car ID: {car.CarID}, Make: {car.Make}, Model: {car.Model}, Color: {car.Color}")

        # Prompt the user to select a car
        car_id = input("Enter the Car ID to rent: ")

        # Get customer information
        customer = self.select_customer()

        # Get rental duration
        rental_duration = self.select_rental_duration()

        try:
            # Create a reservation entry
            query = "INSERT INTO Reservation (CustomerID, CarID, PickupDate, DropoffDate) VALUES (?, ?, GETDATE(), " \
                    "DATEADD(HOUR, ?, GETDATE()))"
            self.cursor.execute(query, (customer.CustomerID, car_id, rental_duration.DurationHours))
            reservation_id = self.cursor.lastrowid

            # Update the car's availability status
            query = "UPDATE Availability SET Available = 0 WHERE RegistrationNumber = ?"
            self.cursor.execute(query, (car_id,))

            # Generate invoice for the reservation
            total_amount = rental_duration.Rate * rental_duration.DurationHours
            query = "INSERT INTO Invoice (ReservationID, TotalAmount, IssuedDate, DueDate, PaymentStatus) VALUES (?, " \
                    "?, GETDATE(), DATEADD(DAY, 7, GETDATE()), 'Pending')"
            self.cursor.execute(query, (reservation_id, total_amount))

            print("Car rented successfully.")
        except Exception as e:
            print("Error renting a car:", str(e))

    def return_cars(self):
        print("---- Return Cars ----")

        # Get input from the user
        customer_id = input("Enter the CustomerID: ")
        registration_number = input("Enter the Registration Number of the car to be returned: ")

        # Implement the logic to return cars
        try:
            # Check if the customer exists
            query = "SELECT * FROM Customer WHERE CustomerID = ?"
            self.cursor.execute(query, (customer_id,))
            customer = self.cursor.fetchone()

            if customer is None:
                print("Customer does not exist.")
                return

            # Update the status of the car in relevant tables
            query = "UPDATE Availability SET Available = 1 WHERE RegistrationNumber = (SELECT CarID FROM Car WHERE " \
                    "RegistrationNumber = ?)"
            self.cursor.execute(query, (registration_number,))

            query = "UPDATE Reservation SET DropoffDate = GETDATE() WHERE CustomerID = ? AND CarID = (SELECT CarID " \
                    "FROM Car WHERE RegistrationNumber = ?)"
            self.cursor.execute(query, (customer_id, registration_number))

            print("Car returned successfully.")

        except Exception as e:
            print("Error returning car:", str(e))

    def view_all_cars(self):
        query = "SELECT * FROM GetAllCars"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        print("----All Cars----\n\n")
        # Display the data using tabulate
        headers = ["CarID", "RegistrationNumber", "MakeName", "ModelName", "Year", "ColorName", "FuelTypeName",
                   "TransmissionTypeName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)

    def manage_admins(self):
        print("---- Manage Admins ----")
        admin_options = ["Add Admin", "Update Admin", "Delete Admin"]
        for i, option in enumerate(admin_options, start=1):
            print(f"{i}. {option}")

        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            self.add_admin()
        elif user_choice == "2":
            self.update_admin()
        elif user_choice == "3":
            self.delete_admin()
        else:
            print("Invalid choice. Please try again.")

    def add_admin(self):
        print("---- Add Admin ----")
        # Get input from the user
        admin_username = input("Enter the username of the admin: ")
        admin_password = input("Enter the password of the admin: ")

        try:
            # Implement the logic to add an admin
            query = "INSERT INTO Admin (Username, Password) VALUES (?, ?)"
            self.cursor.execute(query, (admin_username, admin_password))
            print("Admin added successfully.")
        except Exception as e:
            print("Error adding admin:", str(e))

    def update_admin(self):
        print("---- Update Admin ----")
        # Get input from the user
        admin_username = input("Enter the username of the admin to update: ")
        admin_password = input("Enter the new password for the admin: ")

        try:
            # Implement the logic to update an admin
            query = "UPDATE Admin SET Password = ? WHERE Username = ?"
            self.cursor.execute(query, (admin_password, admin_username))
            if self.cursor.rowcount > 0:
                print("Admin updated successfully.")
            else:
                print("Admin not found.")
        except Exception as e:
            print("Error updating admin:", str(e))

    def delete_admin(self):
        print("---- Delete Admin ----")
        # Get input from the user
        admin_username = input("Enter the username of the admin to delete: ")

        try:
            # Implement the logic to delete an admin
            query = "DELETE FROM Admin WHERE Username = ?"
            self.cursor.execute(query, (admin_username,))
            if self.cursor.rowcount > 0:
                print("Admin deleted successfully.")
            else:
                print("Admin not found.")
        except Exception as e:
            print("Error deleting admin:", str(e))

