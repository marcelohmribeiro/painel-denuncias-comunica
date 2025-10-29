import streamlit as st
from pages.reports import reports

if __name__ == "__main__":
    st.set_page_config(page_title="Comunica", layout="wide")
    reports()
