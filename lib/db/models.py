import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

conn = sqlite3.connect('ExpenseTracker.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                starting_balance REAL
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                expense_name TEXT,
                amount REAL,
                date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''')

# Class for handling user operations
class User:
    def __init__(self, first_name, last_name, starting_balance):
        self.first_name = first_name
        self.last_name = last_name
        self.starting_balance = starting_balance

    def save_to_db(self):
        c.execute('''INSERT INTO users (first_name, last_name, starting_balance)
                    VALUES (?, ?, ?)''', (self.first_name, self.last_name, self.starting_balance))
        conn.commit()

# Class for handling expense operations
class Expense:
    def __init__(self, user_id, expense_name, amount):
        self.user_id = user_id
        self.expense_name = expense_name
        self.amount = amount
        self.date = datetime.now().strftime("%Y-%m-%d")

    def save_to_db(self):
        c.execute('''INSERT INTO expenses (user_id, expense_name, amount, date)
                    VALUES (?, ?, ?, ?)''', (self.user_id, self.expense_name, self.amount, self.date))
        conn.commit()

# Function to prompt user for input and validate
def get_valid_input(prompt, data_type):
    while True:
        user_input = input(prompt)
        try:
            return data_type(user_input)
        except ValueError:
            print("Invalid input. Please try again.")

# Function to generate detailed expense report
def generate_expense_report(user_id):
    c.execute('''SELECT expense_name, amount, date FROM expenses WHERE user_id=?''', (user_id,))
    expenses = c.fetchall()
    total_expense = sum(expense[1] for expense in expenses)
    return expenses, total_expense

# Function to plot budget vs. actual spending
def plot_budget_vs_actual(user_id, starting_balance):
    expenses, total_expense = generate_expense_report(user_id)
    labels = ['Starting Balance', 'Total Expense']
    values = ['Ksh{:.2f}'.format(starting_balance), 'Ksh{:.2f}'.format(total_expense)]

    plt.bar(labels, values, color=['blue', 'red'])
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Budget vs. Actual Spending')
    plt.show()

# Function to view all expenses
def view_expenses(user_id):
    expenses, total_expense = generate_expense_report(user_id)
    if not expenses:
        print("No expenses found.")
    else:
        print("\nExpense Report:")
        for expense in expenses:
            print("Expense: {}, Amount: Ksh{:.2f}, Date: {}".format(expense[0], expense[1], expense[2]))
        print("Total Expense: Ksh{:.2f}".format(total_expense))
# Function to edit expenses       
def edit_expense(user_id):
    view_expenses(user_id)
    expense_id = get_valid_input("\nEnter the ID of the expense you want to edit: ", int)

    new_expense_name = input("Enter the new expense name: ")
    new_amount = get_valid_input("Enter the new amount: ", float)

    Expense.edit_expense(expense_id, new_expense_name, new_amount)
    print("Expense edited successfully!")
    
def delete_expense(expense_id):
    c.execute('''DELETE FROM expenses WHERE expense_id=?''', (expense_id,))
    conn.commit()
    print("Expense deleted successfully!")

# Function to handle deletion of expenses
def delete_expense_option(user_id):
    view_expenses(user_id)
    expense_id = get_valid_input("\nEnter the ID of the expense you want to delete: ", int)
    confirm = input("Are you sure you want to delete this expense? (yes/no): ").lower()
    if confirm == "yes":
        delete_expense(expense_id)
    else:
        print("Deletion canceled.")
    
