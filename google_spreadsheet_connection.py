import streamlit as st
from streamlit_gsheets import GSheetsConnection

# -----------------------------
# Google Sheets Connection
# -----------------------------
conn = st.connection("gsheets", type=GSheetsConnection)
sheet_transactions = "Transactions"
sheet_targets = "Targets"