from database import Database
from datetime import datetime
from decimal import Decimal
from beautifultable import BeautifulTable

class Branch:

    def __init__(self, branch):
        self.db = Database()
        if self.first_run_check() == 1 or branch != 'smouha':
            self.db.create_branch(branch)

    def add_branch(self, branch):
        self.db.create_branch(branch)

    def add_user(self,first_name, last_name, username, password, privilege, branch):
        self.db.add_new_user(first_name)

    def add_car(self, branch, brand, model, car_type, color, price):
        self.db.add_car(branch, brand, model, car_type, color, price)

    def list_all_branch_cars(self):
        all_cars= self.db.get_all_branch_cars()
        table = self.display_cars_branches(all_cars)
        print(table)

    def purchase_car(self, branch, option=None):
        cars, car_table = self.display_cars(branch)

        if len(cars)>0:
            print(car_table)
            choice_id= int(input(f"Please input ID of car to {option}: "))
            car_index=self.find_car_index(choice_id, cars)
            if car_index>=0:
                chosen_car=cars[car_index]
                # print(f"\nChosen car was ID: {chosen_car[0]} with index of: {car_index}\n")

                # print(f"DATA TO SEND TO SQL QUERY IS:\n {(branch, current_time, chosen_car[1], chosen_car[2], chosen_car[5])}")
                if option=="purchase":
                    current_time = datetime.now()
                    self.db.remove_car(branch, chosen_car[0])
                    self.db.add_sales_record(branch, current_time, chosen_car[1], chosen_car[2], chosen_car[5])
                    print("Car was sold successfully!")
                elif option=="delete":
                    self.db.remove_car(branch, chosen_car[0])
                    print("Car was deleted successfully!")
            elif car_index==-1:
                print(f"\nInvalid ID, please try again!\n")
        else:
            print(f"The {branch} branch has no available cars!")

    def get_branch_sales(self, branch):
        sales = self.db.get_branch_sales(branch)
        # print(sales)
        if len(sales)>0:
            table = self.create_car_table(sales, 2)
            print(table)

        else:
            print(f"The {branch} branch has no sales record!")


    def search_car_model(self, branch):
        car_model = input(f"\nPlease input car model you wanna lookup at {branch}: ")

        result = self.db.search_car(branch, car_model)
        if len(result)>0:
            # print(f"result: {result}")
            table = self.create_car_table(result)
            print(table)
        else:
            print(f"{car_model} was not found at {branch} branch..")

    def find_car_index(self, chosen_car_id, cars):
        for i in range(len(cars)):
            if cars[i][0]==chosen_car_id:
                return i
        return -1

    def display_cars(self, branch):
        # return self.create_car_table(self.db.get_all_cars(branch))
        cars = self.db.get_all_cars(branch)
        if len(cars)>0:
            car_table=self.create_car_table(cars)
        else:
            car_table=[]

        return cars, car_table

    def display_cars_branches(self, branches):
        table = self.create_car_table(branches, 1)

        return table


    def create_car_table(self, car_list, choice=None):
        table = BeautifulTable()
        if choice is None:
            table.columns.header = ["ID", "Brand", "Model", "Category", "Color", "Price"]

            for car in car_list:
                car_id, brand, model, category, color, price = car
                table.rows.append([car_id, brand, model, category, color, price])

        elif choice == 1:
            table.columns.header = ["ID", "Brand", "Model", "Category", "Color", "Price","Branch"]

            print(f"before loop: {car_list}")
            for car_branch in car_list:
                print(f"outer loop: {car_branch}")
                for car in car_branch:
                    print(f"inner loop: {car}")
                    car_id, brand, model, category, color, price, branch = car
                    table.rows.append([car_id, brand, model, category, color, price, branch])

        elif choice==2:
            table.columns.header = ["Transaction ID", "Date Time", "Branch", "Brand", "Model", "Price"]
            for sale in car_list:
                print(f"inner loop: {len(sale)} {sale}")
                transaction_id, date_time, branch, brand, model, price = sale
                table.rows.append([transaction_id, date_time, branch, brand, model, price])

        return table

    def new_user_exists(self, first_name, last_name, username, password, privilege, branch):
        result = self.db.search_user(username)
        if result is False:
            self.db.add_new_user(first_name, last_name, username, password, privilege, branch)
            print(f"{username} was added successfully!\n")
        else:
            print("Sorry! Username exists, please try a different one..\n")

    def check_user(self,username, password):
        result = self.db.search_user(username, password)
        if result[0][0] == username and result[0][1] == password:
            print(f"Welcome back {username}\n")
            return (username, result[0][2], result[0][3])
        else:
            print(f"Wrong info please try again!{result}")
            return (result[0], result[1])

    def first_run_check(self):
        count = self.db.count_total_tables()
        return count
