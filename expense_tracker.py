import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

# Set page config
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💸 Monthly Expense Tracker")

# File paths for persistence
EXPENSES_FILE = "expenses.json"
FIXED_CONTRIB_FILE = "fixed_contributions.json"

# Load or initialize data
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, default=str)

st.session_state.expenses = load_data(EXPENSES_FILE)
st.session_state.fixed_contributions = load_data(FIXED_CONTRIB_FILE)

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Add Expense", "Summary", "Fixed Contributions", "Settlements"])

# -------- Add Expense Page -------- #
if menu == "Add Expense":
    st.header("➕ Add Daily Expense")

    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", value=datetime.today())
            category = st.selectbox("Category", ["Market", "Utilities", "Rent", "Other", "Worker Payment"])
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        with col2:
            description = st.text_input("Description")

        submitted = st.form_submit_button("Add Expense")
        if submitted:
            st.session_state.expenses.append({
                "Date": str(date),
                "Category": category,
                "Description": description,
                "Amount": amount
            })
            save_data(EXPENSES_FILE, st.session_state.expenses)
            st.success("Expense added successfully!")

    if st.session_state.expenses:
        st.subheader("📋 All Expenses")
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df)

# -------- Summary Page -------- #
elif menu == "Summary":
    st.header("📊 Monthly Summary")

    if not st.session_state.expenses:
        st.info("No expenses added yet.")
    else:
        df = pd.DataFrame(st.session_state.expenses)
        st.subheader("Raw Data")
        st.dataframe(df)

# -------- Fixed Contributions Page -------- #
elif menu == "Fixed Contributions":
    st.header("💰 Monthly Fixed Contributions")

    with st.form("fixed_contrib_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Person Name")
        with col2:
            date = st.date_input("Contribution Date", value=datetime.today(), key="fc_date")
        amount = st.number_input("Contribution Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Save Contribution")
        if submitted:
            st.session_state.fixed_contributions.append({"Name": name, "Amount": amount, "Date": str(date)})
            save_data(FIXED_CONTRIB_FILE, st.session_state.fixed_contributions)
            st.success("Fixed contribution recorded.")

    if st.session_state.fixed_contributions:
        st.subheader("All Fixed Contributions")
        fixed_df = pd.DataFrame(st.session_state.fixed_contributions)
        st.dataframe(fixed_df)

        total_contributions = fixed_df["Amount"].sum()
        expense_df = pd.DataFrame(st.session_state.expenses)

        total_expenses = expense_df["Amount"].sum() if not expense_df.empty else 0.0
        worker_payments = expense_df[expense_df["Category"] == "Worker Payment"]["Amount"].sum() if not expense_df.empty else 0.0

        available_balance = total_contributions - total_expenses

        st.subheader("💼 Available Balance (Shared Only)")
        st.metric("Total Contributions", f"{total_contributions:.2f}")
        st.metric("All Expenses (incl. Worker Payments)", f"{total_expenses:.2f}")
        st.metric("Balance Left", f"{available_balance:.2f}")

        st.subheader("📅 Total Contributions Per Person")
        contrib_summary = fixed_df.groupby("Name")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
        contrib_summary.columns = ["Person", "Total Contributed"]
        st.dataframe(contrib_summary)

# -------- Settlements Page -------- #
elif menu == "Settlements":
    st.header("💵 Monthly Settlements")

    if not st.session_state.expenses:
        st.info("No expenses to settle.")
    else:
        expense_df = pd.DataFrame(st.session_state.expenses)
        fixed_df = pd.DataFrame(st.session_state.fixed_contributions)

        total_expense = expense_df["Amount"].sum() if not expense_df.empty else 0.0
        names = fixed_df["Name"].unique().tolist() if not fixed_df.empty else []
        num_people = len(names)

        st.write(f"Total Shared Expenses: {total_expense:.2f}")

        equal_share = total_expense / num_people if num_people else 0

        contrib_totals = fixed_df.groupby("Name")["Amount"].sum().to_dict()

        settlements = []
        for name in names:
            paid = contrib_totals.get(name, 0)
            balance = paid - equal_share
            settlements.append({"Name": name, "Contributed": paid, "Owes/Receives": round(balance, 2)})

        settlement_df = pd.DataFrame(settlements)
        st.dataframe(settlement_df)

        st.subheader("💵 Who Owes Whom")
        for entry in settlements:
            if entry["Owes/Receives"] < 0:
                st.markdown(f"🔴 {entry['Name']} should pay {abs(entry['Owes/Receives']):.2f}")
            elif entry["Owes/Receives"] > 0:
                st.markdown(f"🟢 {entry['Name']} should receive {entry['Owes/Receives']:.2f}")
