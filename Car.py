import datetime

from tabulate import tabulate


class Car:
    def __init__(self, cursor):
        self.cursor = cursor

    def view_all_cars(self):
        query = "SELECT * FROM GetAllCars"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Display the data using tabulate
        headers = ["CarID", "RegistrationNumber", "MakeName", "ModelName", "Year", "ColorName", "FuelTypeName",
                   "TransmissionTypeName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)

    def add_car(self):
        make_id = self.display_make_table()
        model_id = self.display_model_table()
        color_id = self.display_color_table()
        reg_num = input("Registration Number: ")
        fuel_type_id = self.display_fuel_type_table()
        transmission_type_id = self.display_transmission_type_table()

        query = """
            INSERT INTO Car (MakeID, ModelID, ColorID, RegistrationNumber, FuelTypeID, TransmissionTypeID)
            VALUES (?, ?, ?, ?, ?, ?)
            """
        self.cursor.execute(query, (make_id, model_id, color_id, reg_num, fuel_type_id, transmission_type_id))
        self.cursor.commit()
        print("Car added successfully!")

    def update_car(self):
        registration_number = input("Enter the Registration Number of the car to update: ")

        while True:
            column = input("Enter the column to update (ColorID, FuelTypeID, TransmissionTypeID), "
                           "or enter 'done' to finish updating: ")

            if column.lower() == 'done':
                break

            new_value = None

            if column.lower() == 'colorid':
                new_value = self.display_color_table()
            elif column.lower() == 'fueltypeid':
                new_value = self.display_fuel_type_table()
            elif column.lower() == 'transmissiontypeid':
                new_value = self.display_transmission_type_table()

            if new_value is not None:
                query = f"UPDATE Car SET {column} = ? WHERE RegistrationNumber = ?"

                try:
                    self.cursor.execute(query, (new_value, registration_number))
                    self.cursor.commit()
                    print(f"Column '{column}' updated successfully!")
                except Exception as e:
                    print(f"Error updating column '{column}': {str(e)}")
            else:
                print("Invalid column name. Please try again.")

    def delete_car(self):
        registration_number = input("Enter the Registration Number of the car to delete: ")

        query = "DELETE FROM Car WHERE RegistrationNumber = ?"

        try:
            self.cursor.execute(query, registration_number)
            self.cursor.commit()
            print("Car deleted successfully!")
        except Exception as e:
            print(f"Error deleting car: {str(e)}")

    def display_transmission_type_table(self) -> int:
        query = "SELECT * FROM TransmissionType ORDER BY TransmissionTypeName"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        headers = ["TransmissionTypeID", "TransmissionTypeName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
        print("\n\n")
        user_choice = input("If you wish to choose a Transmission Type from the table, enter its respective "
                            "TransmissionTypeID. If you want to add a new Transmission Type, enter '0': ")

        if user_choice == "0":
            user_transmission_type_name = input("Enter TransmissionTypeName: ")

            # Check if the TransmissionTypeName already exists in the database
            query = "SELECT TransmissionTypeID FROM TransmissionType WHERE TransmissionTypeName = ?"
            self.cursor.execute(query, (user_transmission_type_name,))
            existing_transmission_type = self.cursor.fetchone()

            if existing_transmission_type:
                print(f"The TransmissionTypeName '{user_transmission_type_name}' already exists in the database.")
                transmission_type_id = existing_transmission_type.TransmissionTypeID
                print("Automatically getting its TransmissionTypeID and adding to Car Table")
                return transmission_type_id

            # Insert the new TransmissionTypeName into the TransmissionType table
            query = "INSERT INTO TransmissionType (TransmissionTypeName) OUTPUT INSERTED.TransmissionTypeID VALUES (?)"
            self.cursor.execute(query, (user_transmission_type_name,))
            self.cursor.commit()

            # Retrieve the generated TransmissionTypeID
            transmission_type_id = self.cursor.fetchone().TransmissionTypeID
            print(f"TransmissionTypeID: {transmission_type_id}")

        else:
            transmission_type_id = int(user_choice)

        return transmission_type_id

    def display_fuel_type_table(self) -> int:
        query = "SELECT * FROM FuelType ORDER BY FuelTypeName"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        headers = ["FuelTypeID", "FuelTypeName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
        print("\n\n")
        user_choice = input("If you wish to choose a FuelType from the table, enter its respective FuelTypeID. "
                            "If you want to add a new Fuel Type, enter '0': ")

        if user_choice == "0":
            user_fuel_type_name = input("Enter FuelTypeName: ")

            # Check if the FuelTypeName already exists in the database
            query = "SELECT FuelTypeID FROM FuelType WHERE FuelTypeName = ?"
            self.cursor.execute(query, (user_fuel_type_name,))
            existing_fuel_type = self.cursor.fetchone()

            if existing_fuel_type:
                print(f"The FuelTypeName '{user_fuel_type_name}' already exists in the database.")
                fuel_type_id = existing_fuel_type.FuelTypeID
                print("Automatically getting its FuelTypeID and adding to Car Table")
                return fuel_type_id

            # Insert the new FuelTypeName into the FuelType table
            query = "INSERT INTO FuelType (FuelTypeName) OUTPUT INSERTED.FuelTypeID VALUES (?)"
            self.cursor.execute(query, (user_fuel_type_name,))
            self.cursor.commit()

            # Retrieve the generated FuelTypeID
            fuel_type_id = self.cursor.fetchone().FuelTypeID
            print(f"FuelTypeID: {fuel_type_id}")

        else:
            fuel_type_id = int(user_choice)

        return fuel_type_id

    def display_color_table(self) -> int:
        query = "SELECT * FROM Color ORDER BY ColorName"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        headers = ["ColorID", "ColorName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
        print("\n\n")
        user_choice = input("If you wish to choose a Color from the table, enter its respective ColorID. "
                            "If you want to add a new Color, enter '0': ")

        if user_choice == "0":
            user_color_name = input("Enter ColorName: ")
            # Check if the ColorName already exists in the database
            query = "SELECT ColorID FROM Color WHERE ColorName = ?"
            self.cursor.execute(query, (user_color_name,))
            existing_color = self.cursor.fetchone()

            if existing_color:
                print(f"The ColorName '{user_color_name}' already exists in the database.")
                color_id = existing_color.ColorID
                print("Automatically getting its ColorID and adding to Car Table")
                return color_id

                # Insert the new Color into the Color table
            query = "INSERT INTO Color (ColorName) OUTPUT INSERTED.ColorID VALUES (?)"
            self.cursor.execute(query, (user_color_name,))
            self.cursor.commit()

            # Retrieve the generated MakeID
            color_id = self.cursor.fetchone().ColorID
            print(f"ColorID: {color_id}")
        else:
            color_id = int(user_choice)

        return color_id

    def display_model_table(self) -> int:
        query = "SELECT * FROM Model ORDER BY ModelName"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        headers = ["ModelID", "ModelName", "Year"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
        print("\n\n")
        user_choice = input("If you wish to choose a Model from the table, enter its respective ModelID. "
                            "If you want to add a new model, enter '0': ")

        if user_choice == "0":
            user_model_name = input("Enter ModelName: ")
            user_model_year = input("Enter ModelYear: ")

            # Check if the ModelName and ModelYear already exist in the database
            query = "SELECT ModelID FROM Model WHERE ModelName = ? AND Year = ?"
            self.cursor.execute(query, (user_model_name, user_model_year))
            existing_model = self.cursor.fetchone()

            if existing_model:
                print(f"The ModelName '{user_model_name}' and ModelYear '{user_model_year}' already exist in the "
                      f"database.")
                model_id = existing_model.ModelID
                print("Automatically getting the ModelID and adding to Car Table")
                return model_id

                # Insert the new MakeName into the Make table
            query = "INSERT INTO Model (ModelName, Year) OUTPUT INSERTED.ModelID VALUES (?, ?)"
            self.cursor.execute(query, (user_model_name, user_model_year))
            self.cursor.commit()

            # Retrieve the generated ModelID
            model_id = self.cursor.fetchone().ModelID
            print(f"ModelID: {model_id}")

        else:
            model_id = int(user_choice)

        return model_id

    def display_make_table(self) -> int:
        query = "SELECT * FROM Make ORDER BY MakeName"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        headers = ["MakeID", "MakeName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
        print("\n\n")
        user_choice = input("If you wish to choose a Make from the table, enter its respective MakeID. "
                            "If you want to add a new make, enter '0': ")

        if user_choice == "0":
            user_make_name = input("Enter MakeName: ")
            # Check if the MakeName already exists in the database
            query = "SELECT MakeID FROM Make WHERE MakeName = ?"
            self.cursor.execute(query, (user_make_name,))
            existing_make = self.cursor.fetchone()

            if existing_make:
                print(f"The MakeName '{user_make_name}' already exists in the database.")
                make_id = existing_make.MakeID
                print("Automatically getting its MakeID and adding to Car Table")
                return make_id

                # Insert the new MakeName into the Make table
            query = "INSERT INTO Make (MakeName) OUTPUT INSERTED.MakeID VALUES (?)"
            self.cursor.execute(query, (user_make_name,))
            self.cursor.commit()

            # Retrieve the generated MakeID
            make_id = self.cursor.fetchone().MakeID
            print(f"MakeID: {make_id}")

        else:
            make_id = int(user_choice)

        return make_id

    def send_car_for_maintenance(self):
        print("----Available Cars----")
        query = "SELECT * FROM ViewAvailableCars"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Display the data using tabulate
        headers = ["CarID", "RegistrationNumber", "MakeID", "MakeName", "ModelID", "ModelName", "Year", "ColorID",
                   "ColorName", "FuelTypeID", "FuelTypeName", "TransmissionTypeID", "TransmissionTypeName"]
        table = tabulate(data, headers=headers, tablefmt="pretty")
        print(table)
        print("\n\n")
        while True:
            reg_num = input("Enter the car's registration number (or 'exit' to cancel): ")
            if reg_num.lower() == 'exit':
                print("Maintenance request cancelled.")
                return
            try:
                # Check if the car registration number exists in the Car table
                check_query = "SELECT COUNT(*) FROM Car WHERE RegistrationNumber = ?"
                self.cursor.execute(check_query, reg_num)
                count = self.cursor.fetchone()[0]
                if count == 0:
                    print("Car registration number not found. Please try again or enter 'exit' to cancel.")
                    continue

                description = input("Enter the maintenance description: ")
                maintenance_date = datetime.date.today().isoformat()

                # Update Availability table
                update_query = "UPDATE Availability SET Available = 0 WHERE RegistrationNumber = ?"
                self.cursor.execute(update_query, reg_num)
                self.cursor.commit()

                if self.cursor.rowcount > 0:
                    print("Car marked as unavailable for maintenance.")
                    # Insert into Maintenance table
                    insert_query = """
                    INSERT INTO Maintenance (RegistrationNumber, Description, MaintenanceDate) VALUES (?,?,?)
                    """
                    self.cursor.execute(insert_query, reg_num, description, maintenance_date)
                    self.cursor.commit()
                    print("Maintenance record inserted successfully.")
                else:
                    print("Car is already marked as unavailable for maintenance.")

                break
            except Exception as e:
                print("An error occurred:", str(e))
