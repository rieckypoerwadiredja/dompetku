import streamlit as st
from datetime import date
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from category import expense_categories, income_categories
# -----------------------------
# Google Sheets Connection
# -----------------------------
conn = st.connection("gsheets", type=GSheetsConnection)
sheet_transactions = "Transactions"
sheet_targets = "Targets"

st.title("💰 Personal Finance Tracker")

# -----------------------------
# Tabs: Transactions & Targets
# -----------------------------
tab1, tab2 = st.tabs(["Transaction Form", "Target Form"])



# -----------------------------
# 1. Transaction Form
# -----------------------------
with tab1:
    st.header("Add a Transaction")
    
    trans_date = st.date_input("Date", value=date.today())
    trans_type = st.selectbox("Type", ["Income", "Expense"])
    trans_nature = st.selectbox("Nature", [ "One-time","Recurring"])

    # Dropdown kategori dinamis
    if trans_type == "Expense":
        trans_category_label = st.selectbox("Category", list(expense_categories.keys()))
        trans_category = expense_categories[trans_category_label]  # value bersih
    else:
        trans_category_label = st.selectbox("Category", list(income_categories.keys()))
        trans_category = income_categories[trans_category_label]  # value bersih

    trans_amount = st.number_input("Amount", min_value=0,step=500)
    trans_desc = st.text_area("Description (optional)")

    if st.button("Save Transaction"):
        # Fetch existing transactions
        try:
            existing_trans = conn.read(worksheet=sheet_transactions).dropna(how="all")
        except:
            existing_trans = pd.DataFrame()  # Jika sheet kosong / tidak bisa dibaca

        # Validasi mandatory field
        if trans_amount <= 0 or not trans_category:
            st.warning("Please fill in the mandatory fields (Amount and Category).")
            st.stop()

        # Buat row baru
        new_trans = pd.DataFrame(
            [
                {
                    "Date": str(trans_date),
                    "Type": trans_type,
                    "Nature": trans_nature,
                    "Category": trans_category,
                    "Amount": trans_amount,
                    "Description": trans_desc
                }
            ]
        )

        # Gabungkan dengan data existing
        if existing_trans.empty:
            updated_trans = new_trans
        else:
            updated_trans = pd.concat([existing_trans, new_trans], ignore_index=True)

        # Update Google Sheets
        try:
            conn.update(worksheet=sheet_transactions, data=updated_trans)
            st.success("Transaction successfully saved!")
        except:
            st.error("Failed to save. Check your Google Sheets connection.")

# -----------------------------
# 2. Target Form
# -----------------------------
with tab2:
    st.header("Add a Financial Target")
    
    target_name = st.text_input("Target Name")
    target_amount = st.number_input("Target Amount", min_value=0,step=500)
    target_deadline = st.date_input("Deadline (optional)", value=None)
    
    submit_target = st.button("Save Target")
    if submit_target:
        # Fetch existing targets
        try:
            existing_targets = conn.read(worksheet=sheet_targets).dropna(how="all")
        except:
            existing_targets = pd.DataFrame()  # Jika sheet kosong / tidak bisa dibaca

        # Validasi mandatory field
        if not target_name or target_amount <= 0:
            st.warning("Please fill in Target Name and Target Amount > 0.")
            st.stop()

        # Cek apakah target name sudah ada
        if not existing_targets.empty and existing_targets.iloc[:,0].str.contains(target_name).any():
            st.warning("A target with this name already exists.")
            st.stop()

        # Buat row baru
        new_target = pd.DataFrame(
            [
                {
                    "TargetName": target_name,
                    "TargetAmount": target_amount,
                    "Deadline": str(target_deadline) if target_deadline else "",
                    "Progress": 0,
                    "Status": "On Track"
                }
            ]
        )

        # Gabungkan dengan data existing
        if existing_targets.empty:
            updated_targets = new_target
        else:
            updated_targets = pd.concat([existing_targets, new_target], ignore_index=True)

        # Update Google Sheets
        try:
            conn.update(worksheet=sheet_targets, data=updated_targets)
            st.success("Target successfully saved!")
        except:
            st.error("Failed to save. Check your Google Sheets connection.")

# -----------------------------
# Optional: Show existing data
# -----------------------------
st.header("All Transactions")
try:
    
    existing_data = conn.read(worksheet="Transactions", usecols=list(range(7)),ttl=5)
    existing_data = existing_data.dropna(how="all")
    if not existing_data.empty:
        st.dataframe(existing_data)
    else:
        st.info("No transactions yet.")
except:
    st.warning("Cannot read transactions. Check connection.")

st.header("All Targets")
try:
    existing_data = conn.read(worksheet="Targets", usecols=list(range(7)),ttl=5)
    existing_data = existing_data.dropna(how="all")
    if not existing_data.empty:
        st.dataframe(existing_data)
    else:
        st.info("No targets yet.")
except:
    st.warning("Cannot read targets. Check connection.")
    
