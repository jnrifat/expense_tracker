💸 Shared Expense Tracker (Streamlit App)

A simple, clean, and efficient monthly shared expense tracking app built using Python and Streamlit. This tool is perfect for households, roommates, or shared accommodations where members contribute to a common pool and share all monthly costs equally.
🚀 Features

    📥 Add Shared Expenses (e.g., groceries, rent, utilities, worker payments)

    💰 Record Fixed Contributions from each person (supports multiple installments)

    📊 View Monthly Summary of expenses, contributions, and available balance

    📈 Automatic Settlement Calculation: who owes how much at the end of the month

    💾 Data Persistence using local JSON files (auto-saved)

🧠 How It Works

    Everyone contributes a fixed or variable amount to a shared pool.

    All expenses are assumed to be shared equally.

    Contributions and expenses are tracked by date.

    The app calculates how much each person owes or is owed at the end of the month based on their contributions.

🖥️ Tech Stack

    Streamlit – interactive UI

    Python (Pandas, JSON, datetime)

    Local storage (no database required)
    
🗂️ File Structure

📁 shared-expense-tracker/
├── app.py
├── expenses.json              # auto-created
├── fixed_contributions.json   # auto-created
└── README.md

🔐 Notes

    Data is stored locally in .json files — no cloud syncing.

    You can clear or back up data by editing or removing the JSON files.
