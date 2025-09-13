from expense import Expense
import calendar
import datetime


def main():
    print("🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 20000

    # Get user input for expense
    expense = get_user_expense()

    # Save expense to file
    save_expense_to_file(expense, expense_file_path)

    # Summarize expenses from file
    summarize_expenses(expense_file_path, budget)


def get_user_expense() -> Expense:
    """Prompt user for expense details and return an Expense object."""
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ").strip()

    # Handle invalid input for amount
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount < 0:
                raise ValueError
            break
        except ValueError:
            print("❌ Please enter a valid positive number for amount.")

    expense_categories = [
        "🍔 Food & Drinks",
    "🏠 Housing / Rent",
    "💼 Work / Office",
    "🎉 Entertainment / Fun",
    "✨ Miscellaneous",
    "🛒 Shopping",
    "🚗 Transport / Fuel",
    "🩺 Health / Medical",
    "📚 Education / Books",
    "💡 Utilities / Bills",
    "💳 Subscriptions / Services",
    "🏖️ Travel / Vacation",
    "👗 Clothing / Accessories",
    "🐶 Pets / Animal Care",
]
       

    while True:
        print("\nSelect a category: ")
        for i, category_name in enumerate(expense_categories, start=1):
            print(f"  {i}. {category_name}")

        try:
            selected_index = int(input(f"Enter a category number [1 - {len(expense_categories)}]: ")) - 1
            if 0 <= selected_index < len(expense_categories):
                selected_category = expense_categories[selected_index]
                return Expense(
                    name=expense_name,
                    category=selected_category,
                    amount=expense_amount,
                )
            else:
                print("❌ Invalid category number. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")


def save_expense_to_file(expense: Expense, expense_file_path: str) -> None:
    """Save an expense entry to the CSV file."""
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path: str, budget: float) -> None:
    """Read all expenses and show summary against budget."""
    print("🎯 Summarizing User Expenses")
    expenses: list[Expense] = []

    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    expense_name, expense_amount, expense_category = line.strip().split(",")
                    expenses.append(
                        Expense(
                            name=expense_name,
                            amount=float(expense_amount),
                            category=expense_category,
                        )
                    )
                except ValueError:
                    # Skip malformed lines
                    continue
    except FileNotFoundError:
        print("❌ No expenses found yet. Start by adding one!")
        return

    if not expenses:
        print("⚠️ No expenses recorded yet.")
        return

    # Calculate category-wise totals
    amount_by_category: dict[str, float] = {}
    for expense in expenses:
        amount_by_category[expense.category] = amount_by_category.get(expense.category, 0) + expense.amount

    print("\nExpenses By Category 📈:")
    for category, amount in amount_by_category.items():
        print(f"  {category}: ₹{amount:.2f}")

    total_spent = sum(exp.amount for exp in expenses)
    print(f"\n💵 Total Spent: ₹{total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ₹{remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = max(1, days_in_month - now.day)  # avoid division by zero

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ₹{daily_budget:.2f}"))


def green(text: str) -> str:
    """Return green-colored terminal text."""
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
