
from db.models import (
plot_budget_vs_actual,
delete_expense_option,
edit_expense,
generate_expense_report,
view_expenses,
get_valid_input,
Expense,
User,
conn,
c
    
    
)
def main():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    # Check if user exists
    c.execute('''SELECT * FROM users WHERE first_name=? AND last_name=?''', (first_name, last_name))
    user = c.fetchone()

    if user:
        user_id = user[0]
        starting_balance = user[3]
        print("Welcome back, {} {}!".format(first_name, last_name))
    else:
        starting_balance = get_valid_input("Enter your starting balance: Ksh", float)
        new_user = User(first_name, last_name, starting_balance)
        new_user.save_to_db()
        user_id = c.lastrowid
        print("Welcome, {} {}!".format(first_name, last_name))

    while True:
        print("\nChoose an option:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Expense Report")
        print("4. Edit Expense")
        print("5. Delete Expense")
        print("6. Plot Budget vs. Actual Spending")
        print("7. Exit")

        option = get_valid_input("Enter your choice: ", int)

        if option == 1:
            expense_name = input("Enter the expense name: ")
            amount = get_valid_input("Enter the amount: Ksh", float)
            new_expense = Expense(user_id, expense_name, amount)
            new_expense.save_to_db()
            print("Expense added successfully!")

        elif option == 2:
            view_expenses(user_id)

        elif option == 3:
            expenses, total_expense = generate_expense_report(user_id)
            print("Total Expense: Ksh{:.2f}".format(total_expense))
            new_balance = starting_balance - total_expense
            print("New Balance: Ksh{:.2f}".format(new_balance))

        elif option == 4:
            edit_expense(user_id)
            
        elif option == 5:
            delete_expense_option(user_id)
            
        elif option == 6:
            plot_budget_vs_actual(user_id, starting_balance)

        elif option == 7:
            break

        else:
            print("Invalid option. Please choose again.")

    conn.close()

if __name__ == "__main__":
    main()
