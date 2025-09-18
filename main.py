import streamlit as st
from google_spreadsheet_connection import conn,sheet_transactions,sheet_targets

st.title("💰 Personal Finance Tracker")

# -----------------------------
# Optional: Show existing data
# -----------------------------
st.header("All Transactions")
try:
    
    existing_data = conn.read(worksheet=sheet_transactions, usecols=list(range(7)),ttl=5)
    existing_data = existing_data.dropna(how="all")
    if not existing_data.empty:
        st.dataframe(existing_data)
    else:
        st.info("No transactions yet.")
except:
    st.warning("Cannot read transactions. Check connection.")

st.header("All Targets")
try:
    existing_data = conn.read(worksheet=sheet_targets, usecols=list(range(7)),ttl=5)
    existing_data = existing_data.dropna(how="all")
    if not existing_data.empty:
        st.dataframe(existing_data)
    else:
        st.info("No targets yet.")
except:
    st.warning("Cannot read targets. Check connection.")
    
